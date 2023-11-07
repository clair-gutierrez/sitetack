from dataclasses import dataclass, field

@dataclass(frozen=True)
class Kmer:
    """ A kmer of length k around a site. """


    """ The character used to pad the kmer if it extends past the start or end of the sequence. """
    padding: str = field(default='-', init=False) 

    """ The length of the kmer, must be odd. """
    length: int 

    """ The position of the site in the sequence. """
    site: int

    """ The amino acid that kmer is centered about, such as 'S' or 'T'. Must be a single character. """
    amino_acid: str

    """ The kmer sequence, such as 'MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRLAAEG' """
    subsequence: str

    def __post_init__(self):
        """ Checks that 
                the length is odd
                the amino acid is in the middle of the subsequence
                the length of the subsequence is the same as the length of the kmer
        """
        print(f"Length: {self.length}, Site: {self.site}, Amino Acid: {self.amino_acid}, Subsequence: {self.subsequence}")
        if self.length % 2 != 1:
            raise ValueError("Length must be odd")
        if self.amino_acid != self.subsequence[self.length // 2]:
            raise ValueError("Amino acid must be in the middle of the subsequence")
        if len(self.subsequence) != self.length:
            raise ValueError("Length of subsequence must be the same as the length of the kmer")
        


    @staticmethod
    def site_to_kmer(sequence: str, site: int, length: int) -> 'Kmer':
        """ Returns a kmer of length length around the given site in the sequence.
            Pads with '-' if the kmer is extends past the start or end of the sequence.

            Parameters:
                sequence: The sequence to get the kmer from.
                site: The site to kmer is centered about, such as 'S' or 'T'. Must be a single character.
                length: The length of the kmer, must be odd 
        """
        subsequence = ""
        if length // 2 > site: # site is too close to the start of the sequence
            subsequence = sequence[:site + length // 2 + 1]
            subsequence = Kmer.padding * (length // 2 - site) + subsequence

        elif length // 2 + site > len(sequence): # site is too close to the end of the sequence
            subsequence = sequence[site - length // 2:]
            subsequence = subsequence + Kmer.padding * (length // 2 + site - len(sequence) + 1)
            
        else: # site is near the middle of the sequence
            subsequence = sequence[site - length // 2:site + length // 2 + 1]

        return Kmer(length=length, site=site, amino_acid=sequence[site], subsequence=subsequence)
