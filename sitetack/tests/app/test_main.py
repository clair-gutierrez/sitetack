# class RequestModel(BaseModel):
#     model_name: str
#     ptms: List[str]
#     sequence: str

#     @root_validator(pre=True)
#     def convert_to_uppercase(cls, values):
#         for field in ['model_name', 'sequence']:
#             if field in values and isinstance(values[field], str):
#                 values[field] = values[field].upper()

#         # make ptms uppercase and remove duplicates
#         if 'ptms' in values and isinstance(values['ptms'], list):
#             values['ptms'] = list(set([ptm.upper() for ptm in values['ptms']]))
#         return values
    
#     @validator('sequence')
#     def sequence_must_be_alphabetic(cls, v):
#         if not v.isalpha():
#             raise ValueError('Sequence must be alphabetic')
#         return v

#     @validator('ptms', each_item=True)
#     def ptm_must_exist_in_ptm_kind(cls, v):
#         ptm_kinds = [ptm.name for ptm in PtmKind]
#         if v not in ptm_kinds:  # type: ignore
#             raise ValueError(f'{v} is not a valid PTM')

from sitetack.app.main import RequestModel, PTMModel, app

class TestRequestModel:

    def test_model_name_is_uppercase_when_given_as_lowercase(self):
        request = RequestModel(model_name="model_name", ptms=[], sequence="")
        assert request.model_name == "MODEL_NAME"
    
    def test_sequence_is_uppercase_when_given_as_lowercase(self):
        request = RequestModel(model_name="", ptms=[], sequence="sequence")
        assert request.sequence == "SEQUENCE"

    def test_ptms_are_uppercase_when_given_as_lowercase(self):
        request = RequestModel(model_name="", ptms=["ptm1", "ptm2"], sequence="")
        assert request.ptms == ["PTM1", "PTM2"]