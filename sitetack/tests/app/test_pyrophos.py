import pytest
import tensorflow as tf
from starlette.testclient import TestClient

from sitetack.app.main import app
from sitetack.app import pyrophos
from sitetack.app.pyrophos import PyrophosModelKind, PYROPHOS_PREFIX

client = TestClient(app)

# All four models, by enum member name (what the API expects).
MODEL_NAMES = [k.name for k in PyrophosModelKind]


class TestPyrophosConfig:
    """Pure-config invariants for the four in-development pyrophos models."""

    def test_four_models(self):
        assert MODEL_NAMES == [
            "NO_LABELS",
            "WITH_PHOS_LABELS",
            "WITH_PYROPHOS_LABELS",
            "WITH_BOTH",
        ]

    def test_alphabets_match_training_pipeline(self):
        # Exact strings from Processing_kmers.ipynb; order + membership matter
        # because encoding indices come from enumerate(alphabet).
        no_labels = "ARNDCEQGHILKMFPSTWYV@&-UX"
        with_labels = "ARNDCEQGHILKMFPSTWYV@&$%-UX"
        assert PyrophosModelKind.NO_LABELS.value.alphabet == no_labels
        assert PyrophosModelKind.WITH_PHOS_LABELS.value.alphabet == no_labels
        assert PyrophosModelKind.WITH_PYROPHOS_LABELS.value.alphabet == with_labels
        assert PyrophosModelKind.WITH_BOTH.value.alphabet == with_labels

    @pytest.mark.parametrize("model", list(PyrophosModelKind))
    def test_alphabet_has_no_duplicate_chars(self, model):
        alphabet = model.value.alphabet
        assert len(alphabet) == len(set(alphabet))

    @pytest.mark.parametrize("model", list(PyrophosModelKind))
    def test_target_residues_present_in_alphabet(self, model):
        for amino_acid in model.value.amino_acids:
            assert amino_acid in model.value.alphabet

    def test_targets_are_serine_and_threonine(self):
        for model in PyrophosModelKind:
            assert model.value.amino_acids == ["S", "T"]


class TestPyrophosModelFiles:
    """The four .h5 files must exist and be loadable Keras models."""

    @pytest.mark.parametrize("model", list(PyrophosModelKind))
    def test_h5_file_exists(self, model):
        assert pyrophos.get_h5_file(model).exists()

    @pytest.mark.parametrize("model", list(PyrophosModelKind))
    def test_h5_file_is_valid_model(self, model):
        h5_file = pyrophos.get_h5_file(model)
        assert tf.keras.models.load_model(h5_file) is not None


class TestPyrophosPage:
    def setup_method(self):
        self.valid_data_one_sequence = {
            "model": "NO_LABELS",
            "text": """
    >mock_sequence_name
    STAAS
    """,
        }

    def test_root(self):
        response = client.get(f"{PYROPHOS_PREFIX}/")
        assert response.status_code == 200

    def test_models_endpoint(self):
        response = client.get(f"{PYROPHOS_PREFIX}/models")
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == set(MODEL_NAMES)
        for value in data.values():
            assert "name" in value
            assert "description" in value

    def test_submit_valid_data(self):
        response = client.post(
            f"{PYROPHOS_PREFIX}/submit/", json=self.valid_data_one_sequence
        )
        assert response.status_code == 200
        assert "sequence_predictions" in response.json()
        sequence_predictions = response.json()["sequence_predictions"]
        assert len(sequence_predictions) == 1
        sequence_prediction = sequence_predictions[0]
        assert "sequence_name" in sequence_prediction
        assert "site_predictions" in sequence_prediction
        site_predictions = sequence_prediction["site_predictions"]
        # STAAS -> S(1), T(2), S(5)
        assert len(site_predictions) == 3
        for site_prediction in site_predictions:
            assert "site" in site_prediction
            assert "amino_acid" in site_prediction
            assert site_prediction["amino_acid"] in ("S", "T")
            assert "probability" in site_prediction
            assert 0 <= site_prediction["probability"] <= 1

    @pytest.mark.parametrize("model_name", MODEL_NAMES)
    def test_submit_runs_for_every_model(self, model_name):
        data = dict(self.valid_data_one_sequence, model=model_name)
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 200
        assert "sequence_predictions" in response.json()

    def test_pyrophos_label_symbols_valid_for_with_labels_model(self):
        # $ and % (pyrophos labels) are in the with-labels alphabet.
        data = {
            "model": "WITH_PYROPHOS_LABELS",
            "text": ">m\nST$%STS",
        }
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 200

    def test_pyrophos_label_symbols_invalid_for_no_labels_model(self):
        # $ and % are NOT in the no-labels alphabet -> validation error.
        data = {
            "model": "NO_LABELS",
            "text": ">m\nST$%STS",
        }
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 422

    def test_submit_with_invalid_model(self):
        data = dict(self.valid_data_one_sequence, model="INVALID_MODEL_KIND")
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 422

    def test_submit_with_blank_text(self):
        data = dict(self.valid_data_one_sequence, text="   ")
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 422

    def test_submit_with_invalid_characters(self):
        data = dict(
            self.valid_data_one_sequence,
            text="""
    >RNase_3
    ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!^*()
    """,
        )
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 422

    @pytest.mark.parametrize("missing_field", ["model", "text"])
    def test_submit_with_missing_field(self, missing_field):
        data = self.valid_data_one_sequence.copy()
        del data[missing_field]
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 422
