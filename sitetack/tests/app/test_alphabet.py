from sitetack.app.alphabet import Alphabet


class TestAlphabet:
    def test_alphabet_has_correct_length(self):
        alphabet_str = "ARNDCEQGHILKMFPSTWYVXZ-U"
        alphabet = Alphabet(alphabet_str)
        assert len(alphabet) == len(alphabet_str)

    def test_alphabet_has_correct_str(self):
        alphabet_str = "ARNDCEQGHILKMFPSTWYVXZ-U"
        alphabet = Alphabet(alphabet_str)
        assert alphabet.str == alphabet_str
