from fastapi import FastAPI
from pydantic.main import BaseModel  # Updated import for BaseModel
from pydantic.class_validators import validator  # Updated import for validator
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind, kind_to_dict
from sitetack.app.fasta import Fasta
from sitetack.app.model import Model
from sitetack.app.predict import Predict
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

import importlib.resources
from pathlib import Path

# Assuming PtmKind, OrganismKind, and LabelKind are defined elsewhere as Enum classes.




class RequestModel(BaseModel):
    ptm: str
    organism: str
    label: str
    text: str

    @validator('ptm', always=True)
    def ptm_must_be_valid(cls, value):
        if value not in PtmKind.__members__:
            raise ValueError('Invalid PTM kind')
        return value
    
    @validator('organism', always=True)
    def organism_must_be_valid(cls, value):
        if value not in OrganismKind.__members__:
            raise ValueError('Invalid organism kind')
        return value
    
    @validator('label', always=True)
    def label_must_be_valid(cls, value):
        if value not in LabelKind.__members__:
            raise ValueError('Invalid label kind')
        return value

    @validator('text', pre=False, always=True)  # Ensures this runs after the other validators
    def validate_text(cls, value, values):
        ptm_kind = values.get('ptm')
        organism_kind = values.get('organism')
        label_kind = values.get('label')
        if ptm_kind and organism_kind and label_kind:
            ptm = PtmKind[ptm_kind]
            organism = OrganismKind[organism_kind]
            label = LabelKind[label_kind]
            alphabet = Model.get_alphabet(ptm, organism, label) 
            is_valid, error_message = Fasta.validate_fasta_text(value, alphabet=alphabet)
            if not is_valid:
                raise ValueError(error_message)
        return value

app = FastAPI()

with importlib.resources.path('sitetack.frontend', '') as frontend_path:
    app.mount("/frontend", StaticFiles(directory=str(frontend_path)), name="frontend")

@app.post("/submit/")
async def submit_data(request: RequestModel):
    # Here you can process the validated data
    ptm = PtmKind[request.ptm]
    organism = OrganismKind[request.organism]
    label = LabelKind[request.label]
    text = request.text
    sequence_predictions = Predict.on_fasta(text, ptm, organism, label)
    return sequence_predictions.to_dict()

@app.get("/")
async def get_form():
    with importlib.resources.path('sitetack.frontend', 'index.html') as import_path:
            filepath = Path(import_path)
    with open(filepath, 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/ptms")
async def get_ptms():
    return kind_to_dict(PtmKind)

@app.get("/organisms")
async def get_organisms():
    return kind_to_dict(OrganismKind)

@app.get("/labels")
async def get_labels():
    return kind_to_dict(LabelKind)