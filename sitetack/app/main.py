from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from sitetack.app.ptm_kind import PtmKind

class RequestModel(BaseModel):
    model_name: str
    ptms: List[str]
    sequence: str

    def __init__(self, **data):
        super().__init__(**data)
        self.model_name = self.model_name.upper()
        self.sequence = self.sequence.upper()
        self.ptms = list(set(ptm.upper() for ptm in self.ptms))

    @validator('sequence')
    def sequence_must_be_alphabetic(cls, v):
        if not v.isalpha():
            raise ValueError('Sequence must be alphabetic')
        return v

    @validator('ptms')
    def ptm_must_exist_in_ptm_kind(cls, v):
        ptm_kinds = [ptm.name for ptm in PtmKind]
        for ptm in v:
            if ptm not in ptm_kinds:
                raise ValueError(f'{ptm} is not a valid PTM')
        return v


# Define a Pydantic model for the PTM object in the response
class PTMModel(BaseModel):
    ptm: str
    index: int
    probability: str

# Initialize the FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define the POST endpoint
@app.post("/process_ptms/")
async def process_ptms(request: RequestModel):
    # You can process the ptms here. As an example, I'm just returning them with index and a dummy probability
    response = {
        "ptms": [{"ptm": ptm, "index": index, "probability": "0.99"} for index, ptm in enumerate(request.ptms)]
    }
    return response

# Run the app with uvicorn in the command line: uvicorn script_name:app --reload
