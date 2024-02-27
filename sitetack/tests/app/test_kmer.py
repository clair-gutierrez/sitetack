from sitetack.app.kmer import Kmer


class TestKmer:
    def test_site_to_kmer_site_in_middle_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = 5
        length = 5
        expected = Kmer(site=site, subsequence="DEFGH")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_site_in_front_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = 0
        length = 5
        expected = Kmer(site=site, subsequence="--ABC")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_site_in_front_has_correct_amino_acid(self):
        sequence = "ABCDEFGHIJK"
        site = 0
        length = 5
        kmer = Kmer.site_to_kmer(sequence, site, length)
        assert kmer.amino_acid == sequence[site]

    def test_site_to_kmer_site_in_back_generates_correctly(self):
        sequence = "ABCDEFGHIJK"
        site = len(sequence) - 1
        length = 5
        expected = Kmer(site=site, subsequence="IJK--")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_equal_padding_on_both_sides(self):
        sequence = "AKA"
        site = 1  # K
        length = 7
        expected = Kmer(site=site, subsequence="--AKA--")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_more_padding_on_left_side(self):
        sequence = "AKB"
        site = 0  # A
        length = 7
        expected = Kmer(site=site, subsequence="---AKB-")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_more_padding_on_right_side(self):
        sequence = "AKB"
        site = 2  # B
        length = 7
        expected = Kmer(site=site, subsequence="-AKB---")
        actual = Kmer.site_to_kmer(sequence, site, length)
        assert expected == actual

    def test_site_to_kmer_site_in_back_has_correct_amino_acid(self):
        sequence = "ABCDEFGHIJK"
        site = len(sequence) - 1
        length = 5
        kmer = Kmer.site_to_kmer(sequence, site, length)
        assert kmer.amino_acid == sequence[site]

    def test_init_has_correct_length(self):
        subsequence = "ABCDEFGHIJK"
        site = 5
        kmer = Kmer(site=site, subsequence=subsequence)
        assert len(kmer) == len(subsequence)

    def test_init_has_correct_amino_acid(self):
        amino_acid = "F"
        subsequence = "ABCDE" + amino_acid + "GHIJK"
        site = 5
        kmer = Kmer(site=site, subsequence=subsequence)
        assert kmer.amino_acid == amino_acid
