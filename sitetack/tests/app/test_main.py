import pytest
from starlette.testclient import TestClient

from sitetack.app.main import app

client = TestClient(app)

class TestMain:
    def setup_method(self):
        self.valid_data_one_sequence = {
            "ptm": "PHOSPHORYLATION_ST",
            "label": "NO_LABELS",
            "organism": "HUMAN",
            "text": """
    >mock_sequence_name
    STAAS
    """
        }

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_submit_valid_data(self):
        response = client.post("/submit/", json=self.valid_data_one_sequence)
        assert response.status_code == 200
        assert "sequence_predictions" in response.json()
        sequence_predictions = response.json()["sequence_predictions"]
        assert len(sequence_predictions) == 1
        sequence_prediction = sequence_predictions[0]
        assert "sequence_name" in sequence_prediction
        assert "site_predictions" in sequence_prediction
        site_predictions = sequence_prediction["site_predictions"]
        assert len(site_predictions) == 3
        for site_prediction in site_predictions:
            assert "site" in site_prediction
            assert "amino_acid" in site_prediction
            assert "probability" in site_prediction
            assert 0 <= site_prediction["probability"] <= 1
        

    @pytest.mark.parametrize(
        "field_name,invalid_value",
        [
            ("ptm", "INVALID_PTM_KIND"),
            ("organism", "INVALID_ORGANISM_KIND"),
            ("label", "INVALID_LABEL_KIND"),
        ]
    )
    def test_submit_with_invalid_input(self,field_name, invalid_value):
        # Assuming 'valid_data_one_sequence' is a fixture or globally available dict
        invalid_data = self.valid_data_one_sequence  # Make a copy of the valid data
        invalid_data[field_name] = invalid_value  # Set the invalid value for the specified field
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422

    def test_submit_with_blank_text(self):
        invalid_data = self.valid_data_one_sequence
        invalid_data["text"] = "   "
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422  # Assuming 422 Unprocessable Entity for validation errors
    
    def test_submit_with_text_invalid_characters(self):
        invalid_data = self.valid_data_one_sequence
        invalid_data["text"] = """
    >RNase_3
    ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()
    """
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422

    def test_submit_with_invalid_ptm_and_invalid_characters(self):
        invalid_data = self.valid_data_one_sequence
        invalid_data["ptm"] = "INVALID_PTM_KIND"
        invalid_data["text"] = """
    >RNase_3
    ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()
    """
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422

    def test_submit_with_invalid_organism_and_invalid_characters(self):
        invalid_data = self.valid_data_one_sequence
        invalid_data["organism"] = "INVALID_ORGANISM_KIND"
        invalid_data["text"] = """
    >RNase_3
    ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()
    """
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422

    def test_submit_with_invalid_label_and_invalid_characters(self):
        invalid_data = self.valid_data_one_sequence
        invalid_data["label"] = "INVALID_LABEL_KIND"
        invalid_data["text"] = """
    >RNase_3
    ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()
    """
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422
    
    @pytest.mark.parametrize("missing_field", [
    ("ptm"),
    ("organism"),
    ("label"),
    ("text")
    ])
    def test_submit_with_missing_field(self, missing_field):
        invalid_data = self.valid_data_one_sequence.copy()
        del invalid_data[missing_field]
        response = client.post("/submit/", json=invalid_data)
        assert response.status_code == 422

