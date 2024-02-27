from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from enum import Enum
from typing import List, Optional
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind

# Assuming PtmKind, OrganismKind, and LabelKind are defined elsewhere as Enum classes.



class RequestModel(BaseModel):
    ptm: str
    organism: str
    label: str
    text: str

    @validator('text')
    def text_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError('Text field must not be blank')
        return value
    
    @validator('ptm')
    def ptm_must_be_valid(cls, value):
        if value not in PtmKind.__members__:
            raise ValueError('Invalid PTM kind')
        return value
    
    @validator('organism')
    def organism_must_be_valid(cls, value):
        if value not in OrganismKind.__members__:
            raise ValueError('Invalid organism kind')
        return value
    
    @validator('label')
    def label_must_be_valid(cls, value):
        if value not in LabelKind.__members__:
            raise ValueError('Invalid label kind')
        return value

app = FastAPI()

@app.post("/submit/")
async def submit_data(request: RequestModel):
    # Here you can process the validated data
    ptm = PtmKind[request.ptm]
    organism = OrganismKind[request.organism]
    label = LabelKind[request.label]

    return {"message": "Data received", "data": request.dict()}
