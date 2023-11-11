from typing import List
from dataclasses import dataclass
from sitetack.kmer import Kmer



@dataclass(frozen=True)
class Sequence:
    """ Represents a sequence in a fasta file."""

    """ UniProtID, such as 'RNase_1' """
    uniprot_id: str

    """ The sequence, such as 'MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRLAAEG' """
    sequence: str

    def get_phosporylation_sites(self, amino_acid: str) -> List[int]:
        """ Returns a numpy array of the positions of the given site in the sequence. 

            Parameters:
                amino_acid: The amino_acid to find, such as 'S' or 'T'. Must be a single character.
        """
        return [i for i, char in enumerate(self.sequence) if char == amino_acid]
    
    def get_kmers(self, length: int, site: str) -> List[Kmer]:
        """ Returns a list of kmers of length k around the given site
            Pads with '-' if the kmer is extends past the start or end of the sequence.

            Parameters:
                length: The length of the kmer, must be odd
                site: The site to kmer is centered about, such as 'S' or 'T'. Must be a single character.
        """
        return [Kmer.site_to_kmer(self.sequence, s, length) for s in self.get_phosporylation_sites(site)]
    
    def __post_init__(self):
        """ Verify that sequence is capitalized """
        if self.sequence != self.sequence.upper():
            raise ValueError("Sequence must be capitalized")

