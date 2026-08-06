import pytest
import tensorflow as tf
from starlette.testclient import TestClient

from sitetack.app.main import app
from sitetack.app import pyrophos
from sitetack.app.pyrophos import CohortKind, PyrophosModelKind, PYROPHOS_PREFIX

client = TestClient(app)

# All four label variants, by enum member name (what the API expects).
MODEL_NAMES = [k.name for k in PyrophosModelKind]

# The three cohort models run for every submission.
COHORT_KEYS = [c.value.key for c in CohortKind]


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
    @pytest.mark.parametrize("cohort", list(CohortKind))
    def test_h5_file_exists(self, model, cohort):
        assert pyrophos.get_h5_file(model, cohort).exists()

    def test_twelve_distinct_model_files(self):
        paths = {
            pyrophos.get_h5_file(model, cohort)
            for model in PyrophosModelKind
            for cohort in CohortKind
        }
        assert len(paths) == 12

    @pytest.mark.parametrize("model", list(PyrophosModelKind))
    @pytest.mark.parametrize("cohort", list(CohortKind))
    def test_h5_file_is_valid_model(self, model, cohort):
        h5_file = pyrophos.get_h5_file(model, cohort)
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
        assert set(data["models"].keys()) == set(MODEL_NAMES)
        for value in data["models"].values():
            assert "name" in value
            assert "description" in value

    def test_models_endpoint_lists_cohorts(self):
        data = client.get(f"{PYROPHOS_PREFIX}/models").json()
        assert [c["key"] for c in data["cohorts"]] == COHORT_KEYS
        for cohort in data["cohorts"]:
            assert cohort["name"]
            assert cohort["description"]

    def test_submit_valid_data(self):
        response = client.post(
            f"{PYROPHOS_PREFIX}/submit/", json=self.valid_data_one_sequence
        )
        assert response.status_code == 200
        payload = response.json()
        assert "sequences" in payload
        assert len(payload["sequences"]) == 1

        sequence = payload["sequences"][0]
        assert "sequence_name" in sequence
        assert "sequence" in sequence
        # STAAS -> S(1), T(2), S(5)
        sites = sequence["sites"]
        assert [site["site"] for site in sites] == [1, 2, 5]
        for site in sites:
            assert site["amino_acid"] in ("S", "T")
            assert set(site["scores"].keys()) == set(COHORT_KEYS)
            for probability in site["scores"].values():
                assert 0 <= probability <= 1
            assert isinstance(site["is_ck2_motif"], bool)
            assert 0 <= site["routed"] <= 1

    def test_routed_score_follows_the_motif_call(self):
        payload = client.post(
            f"{PYROPHOS_PREFIX}/submit/", json=self.valid_data_one_sequence
        ).json()
        for site in payload["sequences"][0]["sites"]:
            expected = site["scores"]["ck2" if site["is_ck2_motif"] else "other"]
            assert site["routed"] == expected

    def test_cohorts_give_different_scores(self):
        # Three separately trained models should not agree exactly; if they do,
        # the same file is being loaded three times.
        payload = client.post(
            f"{PYROPHOS_PREFIX}/submit/", json=self.valid_data_one_sequence
        ).json()
        for site in payload["sequences"][0]["sites"]:
            assert len(set(site["scores"].values())) > 1

    @pytest.mark.parametrize("model_name", MODEL_NAMES)
    def test_submit_runs_for_every_model(self, model_name):
        data = dict(self.valid_data_one_sequence, model=model_name)
        response = client.post(f"{PYROPHOS_PREFIX}/submit/", json=data)
        assert response.status_code == 200
        assert "sequences" in response.json()

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


class TestCk2Motif:
    """The +3 rule, mirrored from pyrophos.motif in the training repo."""

    @pytest.mark.parametrize("residue", ["E", "D", "S", "T"])
    def test_acidic_and_hydroxyl_match(self, residue):
        assert pyrophos.is_ck2_motif("MAS" + "AA" + residue, 3) is True

    @pytest.mark.parametrize("residue", ["A", "K", "R", "P", "G"])
    def test_other_residues_do_not(self, residue):
        assert pyrophos.is_ck2_motif("MAS" + "AA" + residue, 3) is False

    @pytest.mark.parametrize("symbol", ["@", "&", "$", "%"])
    def test_label_symbols_count_as_their_residue(self, symbol):
        assert pyrophos.is_ck2_motif("MAS" + "AA" + symbol, 3) is True

    def test_site_without_a_plus3_residue_is_not_ck2(self):
        assert pyrophos.is_ck2_motif("MAST", 3) is False


class TestCohortFilenames:
    def test_general_keeps_the_historical_name(self):
        for model in PyrophosModelKind:
            path = pyrophos.get_h5_file(model, CohortKind.GENERAL)
            assert path.name == model.value.h5_filename

    @pytest.mark.parametrize("cohort", [CohortKind.CK2, CohortKind.OTHER])
    def test_cohorts_are_suffixed(self, cohort):
        for model in PyrophosModelKind:
            path = pyrophos.get_h5_file(model, cohort)
            assert path.name.endswith(cohort.value.suffix + ".h5")

    def test_model_cards_agree_with_the_hardcoded_alphabets(self):
        """The alphabet a model was trained with must match what we encode with."""
        import json

        for model in PyrophosModelKind:
            for cohort in CohortKind:
                card_path = pyrophos.get_h5_file(model, cohort).with_suffix("")
                card_path = card_path.parent / (card_path.name + ".model_card.json")
                if not card_path.exists():
                    continue
                card = json.loads(card_path.read_text())
                assert card["contract"]["alphabet"] == model.value.alphabet
                assert card["contract"]["kmer_length"] == 53
                assert card["contract"]["target_residues"] == model.value.amino_acids
