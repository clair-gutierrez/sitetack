

# from sitetack.app.main import RequestModel, PTMModel, app

# class TestRequestModel:

#     def test_model_name_is_uppercase_when_given_as_lowercase(self):
#         request = RequestModel(model_name="model_name", ptms=[], sequence="")
#         assert request.model_name == "MODEL_NAME"
    
#     def test_sequence_is_uppercase_when_given_as_lowercase(self):
#         request = RequestModel(model_name="", ptms=[], sequence="sequence")
#         assert request.sequence == "SEQUENCE"

#     def test_ptms_are_uppercase_when_given_as_lowercase(self):
#         request = RequestModel(model_name="", ptms=["ptm1", "ptm2"], sequence="")
#         assert request.ptms == ["PTM1", "PTM2"]