from sitetack.kmer import Kmer    

class TestKmer:

    def test_site_to_kmer_site_in_middle_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = 5
        length = 5
        expected = Kmer(length=length, site=site, amino_acid=sequence[site], subsequence="DEFGH")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual
    
    def test_site_to_kmer_site_in_front_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = 0
        length = 5
        expected = Kmer(length=length, site=site, amino_acid=sequence[site], subsequence="--ABC")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual
    
    def test_site_to_kmer_site_in_back_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = len(sequence) - 1
        length = 5
        expected = Kmer(length=length, site=site, amino_acid=sequence[site], subsequence="IJK--")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual
    