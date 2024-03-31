import importlib.resources
from pathlib import Path
from sitetack.app.fasta import Fasta
from sitetack.app.sequence import Sequence
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.model import Model


class TestFasta:
    @classmethod
    def setup_class(cls):
        with importlib.resources.path(
            "sitetack.tests.resources", "empty.fasta"
        ) as empty_path:
            cls.empty_path = Path(empty_path)

        with importlib.resources.path(
            "sitetack.tests.resources", "one_sequence.fasta"
        ) as one_sequence_path:
            cls.one_sequence_path = Path(one_sequence_path)
        cls.one_sequences_sequences = [
            Sequence(sequence_name="RNase_3", sequence="MVPKLFTSQICLLLLLGLMGVEGSLHARPPQFTRAQWFAIQHISLNPPRCTIAMRAINNYRWRCKNQNTFLRTTFANVVNVCGNQSIRCPHNRTLNNCHRSRFRVPLLHCDLINPGAQNISNCTYADRPGRRFYVVACDNRDPRDSPRYPVVPVHLDTTI")
        ]

        with importlib.resources.path(
            "sitetack.tests.resources", "two_sequences.fasta"
        ) as two_sequences_path:
            cls.two_sequences_path = Path(two_sequences_path)
        cls.two_sequences_sequences = [
            Sequence(sequence_name='RNase_1', sequence='MALEKSLVRLLLLVLILLVLGWVQPSLGKESRAKKFQRQHMDSDSSPSSSSTYCNQMMRRRNMTQGRCKPVNTFVHEPLVDVQNVCFQEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRYPNCAYRTSPKERHIIVACEGSPYVPVHFDASVEDST'),
            Sequence(sequence_name='RNase_2', sequence='MVPKLFTSQICLLLLLGLLAVEGSLHVKPPQFTWAQWFETQHINMTSQQCTNAMQVINNYQRRCKNQNTFLLTTFANVVNVCGNPNMTCPSNKTRKNCHHSGSQVPLIHCNLTTPSPQNISNCRYAQTPANMFYIVACDNRDQRRDPPQYPVVPVHLDRII')
        ]

        # Used for validate_fasta_text
        cls.alphabet = Model.get_alphabet(PtmKind.PHOSPHORYLATION_ST, OrganismKind.HUMAN, LabelKind.WITH_LABELS)
    
    def test_read_sequences_from_file_returns_two_sequences_when_two_sequences(self):
        sequences = Fasta.read_sequences_from_file(self.two_sequences_path)
        assert len(sequences) == 2

    def test_read_sequences_from_file_correct_sequences_when_two_sequences(self):
        sequences = Fasta.read_sequences_from_file(self.two_sequences_path)
        assert set(sequences) == set(self.two_sequences_sequences)

    def test_read_sequences_from_file_returns_one_sequence_when_one_sequence(self):
        sequences = Fasta.read_sequences_from_file(self.one_sequence_path)
        assert len(sequences) == 1

    def test_read_sequences_from_file_correct_sequence_when_one_sequence(self):
        sequences = Fasta.read_sequences_from_file(self.one_sequence_path)
        assert set(sequences) == set(self.one_sequences_sequences)
    
    def test_read_sequences_from_file_returns_empty_list_when_empty_file(self):
        sequences = Fasta.read_sequences_from_file(self.empty_path)
        assert sequences == []

    def test_read_sequences_from_text_returns_two_sequences_when_two_sequences(self):
        with open(self.two_sequences_path, 'r') as f:
            text = f.read()
        sequences = Fasta.read_sequences_from_text(text)
        assert len(sequences) == 2

    def test_read_sequences_from_text_correct_sequences_when_two_sequences(self):
        with open(self.two_sequences_path, 'r') as f:
            text = f.read()
        sequences = Fasta.read_sequences_from_text(text)
        assert set(sequences) == set(self.two_sequences_sequences)

    def test_read_sequences_from_text_returns_one_sequence_when_one_sequence(self):
        with open(self.one_sequence_path, 'r') as f:
            text = f.read()
        sequences = Fasta.read_sequences_from_text(text)
        assert len(sequences) == 1

    def test_read_sequences_from_text_correct_sequence_when_one_sequence(self):
        with open(self.one_sequence_path, 'r') as f:
            text = f.read()
        sequences = Fasta.read_sequences_from_text(text)
        assert set(sequences) == set(self.one_sequences_sequences)

    def test_read_sequences_from_text_returns_empty_list_when_empty_text(self):
        with open(self.empty_path, 'r') as f:
            text = f.read()
        sequences = Fasta.read_sequences_from_text(text)
        assert sequences == []

    def test_validate_fasta_text_returns_true_when_valid_one_sequence(self):
        with open(self.one_sequence_path, 'r') as f:
            text = f.read()
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (True, "The FASTA text is valid.")
    
    def test_validate_fasta_text_returns_true_when_valid_two_sequences(self):
        with open(self.two_sequences_path, 'r') as f:
            text = f.read()
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (True, "The FASTA text is valid.")
    
    def test_validate_fasta_text_returns_false_when_empty(self):
        text = ""
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (False, "The FASTA text is empty.")
    
    def test_validate_fasta_text_returns_false_when_missing_initial_header(self):
        text = "AGCT\n>header2\nATGC"
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (False, "The FASTA text must start with a header line (>).")

    def test_validate_fasta_text_returns_false_when_invalid_characters(self):
        text = """>header1
        A*TGCB"""
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (False, f"Invalid character found in sequence. Valid characters are: {self.alphabet.str}")

    def test_validate_fasta_text_returns_false_when_no_sequence_data_after_header(self):
        text = """>header1\n>header2"""
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (False, "No sequence data found after header lines.")

    def test_validate_fasta_text_returns_false_when_duplicate_headers(self):
        text = """>header1\nAGCT\n>header1\nATGC"""
        assert Fasta.validate_fasta_text(text, alphabet=self.alphabet) == (False, "Duplicate sequence name found: header1")