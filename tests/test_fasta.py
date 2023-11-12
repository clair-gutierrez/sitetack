from pathlib import Path
from sitetack.fasta import Fasta
from sitetack.sequence import Sequence


class TestFasta:

    @classmethod
    def setup_class(cls):
        cls.empty_path = Path(__file__).parent / 'resources' / 'empty.fasta'

        cls.one_sequence_path = Path(__file__).parent / 'resources' / 'one_sequence.fasta'
        cls.one_sequences_sequences = [
            Sequence(uniprot_id="RNase_3", sequence="MVPKLFTSQICLLLLLGLMGVEGSLHARPPQFTRAQWFAIQHISLNPPRCTIAMRAINNYRWRCKNQNTFLRTTFANVVNVCGNQSIRCPHNRTLNNCHRSRFRVPLLHCDLINPGAQNISNCTYADRPGRRFYVVACDNRDPRDSPRYPVVPVHLDTTI")
        ]

        cls.two_sequences_path = Path(__file__).parent / 'resources' / 'two_sequences.fasta'
        cls.two_sequences_sequences = [
            Sequence(uniprot_id='RNase_1', sequence='MALEKSLVRLLLLVLILLVLGWVQPSLGKESRAKKFQRQHMDSDSSPSSSSTYCNQMMRRRNMTQGRCKPVNTFVHEPLVDVQNVCFQEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRYPNCAYRTSPKERHIIVACEGSPYVPVHFDASVEDST'),
            Sequence(uniprot_id='RNase_2', sequence='MVPKLFTSQICLLLLLGLLAVEGSLHVKPPQFTWAQWFETQHINMTSQQCTNAMQVINNYQRRCKNQNTFLLTTFANVVNVCGNPNMTCPSNKTRKNCHHSGSQVPLIHCNLTTPSPQNISNCRYAQTPANMFYIVACDNRDQRRDPPQYPVVPVHLDRII')
        ]
    
    def test_read_sequences_returns_two_sequences_when_two_sequences(self):
        sequences = Fasta.read_sequences(self.two_sequences_path)
        assert len(sequences) == 2

    def test_read_sequences_correct_sequences_when_two_sequences(self):
        sequences = Fasta.read_sequences(self.two_sequences_path)
        assert set(sequences) == set(self.two_sequences_sequences)

    def test_read_sequences_returns_one_sequence_when_one_sequence(self):
        sequences = Fasta.read_sequences(self.one_sequence_path)
        assert len(sequences) == 1

    def test_read_sequences_correct_sequence_when_one_sequence(self):
        sequences = Fasta.read_sequences(self.one_sequence_path)
        assert set(sequences) == set(self.one_sequences_sequences)
    
    def test_read_sequences_returns_empty_list_when_empty_file(self):
        sequences = Fasta.read_sequences(self.empty_path)
        assert sequences == []
