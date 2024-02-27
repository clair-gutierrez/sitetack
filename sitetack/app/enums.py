from enum import Enum
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class PtmKindMetadata:
    """ Describes a PTM kind """

    name: str  # directory name = display name
    sites: List[str]
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

    HYDROXYLYSINE_K = PtmKindMetadata(
        name="Hydroxylysine (K)",
        sites=["K"],
        description="Hydroxylysine is a derivative of the amino acid lysine, which is used to form cross-links in collagen.",
    )
    HYDROXYPROLINE_P = PtmKindMetadata(
        name="Hydroxyproline (P)",
        sites=["P"],
        description="Hydroxyproline is a derivative of the amino acid proline, which helps stabilize the triple helix of collagen.",
    )
    METHYLATION_K = PtmKindMetadata(
        name="Methylation (K)",
        sites=["K"],
        description="Methylation is the addition of a methyl group to the amino acid lysine, which can affect gene expression and protein function.",
    )
    METHYLATION_R = PtmKindMetadata(
        name="Methylation (R)",
        sites=["R"],
        description="Methylation is the addition of a methyl group to the amino acid arginine, which can affect gene expression and protein function.",
    )
    N_LINKED_GLYCOSYLATION_N = PtmKindMetadata(
        name="N-linked glycosylation (N)",
        sites=["N"],
        description="N-linked glycosylation is the attachment of sugar molecules to the amino acid asparagine, which is important for protein folding and stability.",
    )
    N6_ACETYLATION_K = PtmKindMetadata(
        name="N6-acetylation (K)",
        sites=["K"],
        description="N6-acetylation is the addition of an acetyl group to the amino acid lysine, which can regulate protein function and stability.",
    )
    O_LINKED_GLYCOSYLATION_ST = PtmKindMetadata(
        name="O-linked glycosylation (S,T)",
        sites=["S", "T"],
        description="O-linked glycosylation is the attachment of sugar molecules to the amino acids serine and threonine, which is important for protein folding and stability.",
    )
    PHOSPHORYLATION_ST = PtmKindMetadata(
        name="Phosphorylation (S,T)",
        sites=["S", "T"],
        description="Phosphorylation is the addition of a phosphate group to the amino acids serine and threonine, which is important for protein function and regulation.",
    )
    PHOSPHORYLATION_Y = PtmKindMetadata(
        name="Phosphorylation (Y)",
        sites=["Y"],
        description="Phosphorylation is the addition of a phosphate group to the amino acid tyrosine, which is important for protein function and regulation.",
    )
    PYRROLIDONE_CARBOXYLIC_ACID_Q = PtmKindMetadata(
        name="Pyrrolidone-carboxylic-acid (Q)",
        sites=["Q"],
        description="Pyrrolidone carboxylic acid is a derivative of the amino acid glutamine, which is important for protein folding and stability.",
    )
    S_PALMITOYLATION_C = PtmKindMetadata(
        name="S-Palmitoylation (C)",
        sites=["C"],
        description="S-palmitoylation is the addition of a palmitoyl group to the amino acid cysteine, which is important for protein function and stability.",
    )
    SUMOYLATION_K = PtmKindMetadata(
        name="SUMOylation (K)",
        sites=["K"],
        description="SUMOylation is the addition of a small ubiquitin-like modifier (SUMO) to the amino acid lysine, which is important for protein function and stability.",
    )
    UBIQUITINATION_K = PtmKindMetadata(
        name="Ubiquitination (K)",
        sites=["K"],
        description="Ubiquitination is the addition of a ubiquitin protein to the amino acid lysine, which is important for protein function and stability.",
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
        description="With labels encodes known PTM locations as a separate amino acid.",
    )
