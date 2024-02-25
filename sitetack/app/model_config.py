""" Keeps track of the model configurations """

from dataclasses import dataclass
from sitetack.app.ptm_kind import PtmKind


@dataclass(frozen=True)
class ModelConfig:

    """ Describes what the model does"""
    description: str

    """ The name of the model
        Must be unique, lowercase, and correspond to a base filename in the models directory 
    """
    name: str

    """ The kind of phosphorylation the model predicts """
    ptm_kind: PtmKind
