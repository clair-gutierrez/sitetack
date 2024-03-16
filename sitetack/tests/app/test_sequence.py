from sitetack.app.sequence import Sequence
from sitetack.app.kmer import Kmer

class TestSequence:
    
    @classmethod
    def setup_class(cls):
        cls.multiple_s = Sequence(sequence_name='RNase_1', sequence='SMASLEKS')
        cls.no_s = Sequence(sequence_name='RNase_1', sequence='MALEK')
    
    def test_get_phosporylation_sites_returns_empty_array_when_no_sites(self):
        assert len(self.no_s.get_phosporylation_sites('S')) == 0

    def test_get_phosporylation_sites_returns_correct_array_when_has_sites(self):
        assert self.multiple_s.get_phosporylation_sites('S') ==  [1,4,8]

    def test_get_kmers_returns_empty_array_when_no_sites(self):
        assert self.no_s.get_kmers(3, 'S') == []
    
    def test_get_kmers_returns_correct_array_when_has_sites(self):
        length = 7
        amino_acid = 'S'
        expected = [
            Kmer(site=1, subsequence='---SMAS'), 
            Kmer(site=4, subsequence='SMASLEK'), 
            Kmer(site=8, subsequence='LEKS---')
        ]
        assert self.multiple_s.get_kmers(length, amino_acid) == expected