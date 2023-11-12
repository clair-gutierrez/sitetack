from dataclasses import dataclass, field

@dataclass(frozen=True)
class Kmer:
    """ A kmer of length k around a site. """


    """ The character used to pad the kmer if it extends past the start or end of the sequence. """
    padding: str = field(default='-', init=False) 

    """ The amino acid that kmer is centered about, such as 'S' or 'T'. Must be a single character. """
    amino_acid: str = field(init=False)

    """ The position of the site in the sequence. """
    site: int

    """ The kmer sequence, such as 'MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRLAAEG' """
    subsequence: str

    def __post_init__(self):
        """ Checks that 
                the length is odd
                the amino acid is in the middle of the subsequence
        """
        # Set the amino acid
        object.__setattr__(self, 'amino_acid', self.subsequence[len(self) // 2])

        if len(self) % 2 != 1:
            raise ValueError("Length must be odd")
        if self.amino_acid != self.subsequence[len(self) // 2]:
            raise ValueError("Amino acid must be in the middle of the subsequence")
    

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

        return Kmer(site=site, subsequence=subsequence)

    def __len__(self):
        """ The length of the kmer, must be odd. """
        return len(self.subsequence)
    
    def __iter__(self):
        """ Returns an iterator over the kmer. """
        return iter(self.subsequence)