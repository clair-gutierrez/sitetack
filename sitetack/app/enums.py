from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Type, Dict



def kind_to_dict(enum_class: Type[Enum]) -> Dict[str, Dict]:
    """Converts an enum class to a dictionary of its members and their metadata."""
    d = {}
    for kind in enum_class:
        d[kind.name] = asdict(kind.value)
    return d


@dataclass(frozen=True)
class PtmKindMetadata:
    """ Describes a PTM kind """
    name: str # directory name = display name
    amino_acids: List[str]   
    description: str
    directory_name: str = field(default_factory=str)  # directory name = display name

    def __post_init__(self):
        if not self.directory_name:
            object.__setattr__(self, "directory_name", self.name)


@dataclass(frozen=True)
class OrganismKindMetadata:
    """ Describes a kind """

    name: str
    directory_name: str
    description: str


@dataclass(frozen=True)
class LabelKindMetadata:
    """ Describes a kind """

    name: str
    filename_query: str
    description: str


class PtmKind(Enum):
    """
    An enumeration of Post-Translational Modification (PTM) types.

    This enum classifies various common PTMs that proteins can undergo after translation. 
    Each member of the enum represents a distinct type of PTM, which are critical for understanding 
    the functional modifications and regulatory mechanisms affecting proteins.
    """
    PHOSPHORYLATION_ST = PtmKindMetadata(
        name="Phosphorylation (S,T)",
        amino_acids=["S", "T"],
        description="Phosphorylation (S,T) is the addition of a phosphoryl group to Oγ of serine or threonine.",
    )
    PHOSPHORYLATION_Y = PtmKindMetadata(
        name="Phosphorylation (Y)",
        amino_acids=["Y"],
        description="Phosphorylation (Y) is the addition of a phosphoryl group to Oη of tyrosine.",
    ) 
    N_LINKED_GLYCOSYLATION_N = PtmKindMetadata(
        name="N-Linked glycosylation (N)",
        amino_acids=["N"],
        description="N-Linked glycosylation (N) is the addition of a glycan to Nδ of the amino acid asparagine.",
    )
    O_LINKED_GLYCOSYLATION_ST = PtmKindMetadata(
        name="O-Linked glycosylation (S,T)",
        amino_acids=["S", "T"],
        description="O-Linked glycosylation (S,T) is the addition of a glycan to Oγ of serine or threonine.",
    )
    UBIQUITINATION_K = PtmKindMetadata(
        name="Ubiquitination (K)",
        amino_acids=["K"],
        description="Ubiquitination (K) is the addition of ubiquitin to Nε of lysine.",
    )
    SUMOYLATION_K = PtmKindMetadata(
        name="SUMOylation (K)",
        amino_acids=["K"],
        description="SUMOylation (K) is the addition of SUMO to Nε of lysine.",
    )
    N6_ACETYLATION_K = PtmKindMetadata(
        name="Acetylation (K)",
        amino_acids=["K"],
        description="Acetylation (K) is the addition of an acetyl group to Nε of lysine.",
    )
    METHYLATION_K = PtmKindMetadata(
        name="Methylation (K)",
        amino_acids=["K"],
        description="Methylation (K) is the addition of one, two, or three methyl groups to Nε of lysine.",
    )
    METHYLATION_R = PtmKindMetadata(
        name="Methylation (R)",
        amino_acids=["R"],
        description="Methylation (R) is the addition of one or two methyl groups to the Nζ's of arginine.",
    )
    PYRROLIDONE_CARBOXYLIC_ACID_Q = PtmKindMetadata(
        name="Pyroglutamylation (Q)",
        amino_acids=["Q"],
        description="Pyroglutamylation (Q) is the cyclization of the amino and amido groups of an N-terminal glutamine.",
    )
    S_PALMITOYLATION_C = PtmKindMetadata(
        name="Palmitoylation (C)",
        amino_acids=["C"],
        description="Palmitoylation (C) is the addition of a palmitoyl group to Sγ of the amino acid cysteine.",
    )
    HYDROXYPROLINE_P = PtmKindMetadata(
        name="Hydroxylation (P)",
        amino_acids=["P"],
        description="Hydroxylation (P) is the addition with R stereochemistry of a hydroxyl group to Cδ of the amino acid proline.",
    )
    HYDROXYLYSINE_K = PtmKindMetadata(
        name="Hydroxylation (K)",
        amino_acids=["K"],
        description="Hydroxylation (K) is the addition with R stereochemistry of a hydroxyl group to Cγ of the amino acid proline.",
    )
     
    


class OrganismKind(Enum):
    """
    An enumeration of the different types of organisms
    """

    HUMAN = OrganismKindMetadata(
        name="Human",
        directory_name="Human",
        description="Model trained on only human proteins",
    )
    ALL_ORGANISM = OrganismKindMetadata(
        name="All Organisms",
        directory_name="All organism",
        description="Model trained on proteins from all organisms",
    )


class LabelKind(Enum):
    """
    An enumeration of the different types of labeled data
    """

    NO_LABELS = LabelKindMetadata(
        name="No Labels",
        filename_query="no_labels",
        description="No labels does not encode known PTM locations.",
    )
    WITH_LABELS = LabelKindMetadata(
        name="With Labels",
        filename_query="with_labels",
        description="With labels encodes known PTM locations as a separate amino acid. Previously known PTM locations can be encoded with the @ symbol (and/or the & symbol for models with a second amino acid that can be post-translationally modified) in submission sequences",
    )
