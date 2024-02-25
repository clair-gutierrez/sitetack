from enum import Enum, auto

class PtmKind(Enum):
    """
    An enumeration of Post-Translational Modification (PTM) types.

    This enum classifies various common PTMs that proteins can undergo after translation. 
    Each member of the enum represents a distinct type of PTM, which are critical for understanding 
    the functional modifications and regulatory mechanisms affecting proteins.
    """
    ACETYLATION = auto()
    METHYLATION = auto()
    PHOSPHORYLATION = auto()
    SUMOYLATION = auto()
    UBIQUITINATION = auto()
    GLYCOSYLATION = auto()
    HYDROXYLATION = auto()
    PALMITOYLATION = auto()
    S_NITROSYLATION = auto()
    SULFATION = auto()
    NEDDYLATION = auto()
    DEAMIDATION = auto()
    DEIMINATION = auto()
    FORMYLATION = auto()
    MYRISTOYLATION = auto()
    PYRROLIDONE_CARBOXYLIC_ACID = auto()

