import importlib
import tensorflow as tf
import numpy as np
from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer
from sitetack.app.predict import Predict, SitePrediction, SequencePrediction, SequencePredictions
from pathlib import Path
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.sequence import Sequence
from sitetack.app.model import Model
from sitetack.app.fasta import Fasta

class TestPredict:

    @classmethod
    def setup_class(cls):
        with importlib.resources.path('sitetack.tests.resources', 'empty.fasta') as empty_path:
            cls.empty_path = Path(empty_path)

        with importlib.resources.path('sitetack.tests.resources', 'one_sequence.fasta') as one_sequence_path:
            cls.one_sequence_path = Path(one_sequence_path)
        cls.one_sequences_sequences = [
            Sequence(sequence_name="RNase_3", sequence="MVPKLFTSQICLLLLLGLMGVEGSLHARPPQFTRAQWFAIQHISLNPPRCTIAMRAINNYRWRCKNQNTFLRTTFANVVNVCGNQSIRCPHNRTLNNCHRSRFRVPLLHCDLINPGAQNISNCTYADRPGRRFYVVACDNRDPRDSPRYPVVPVHLDTTI")
        ]

        with importlib.resources.path('sitetack.tests.resources', 'two_sequences.fasta') as two_sequences_path:
            cls.two_sequences_path = Path(two_sequences_path)
        cls.two_sequences_sequences = [
            Sequence(sequence_name='RNase_1', sequence='MALEKSLVRLLLLVLILLVLGWVQPSLGKESRAKKFQRQHMDSDSSPSSSSTYCNQMMRRRNMTQGRCKPVNTFVHEPLVDVQNVCFQEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRYPNCAYRTSPKERHIIVACEGSPYVPVHFDASVEDST'),
            Sequence(sequence_name='RNase_2', sequence='MVPKLFTSQICLLLLLGLLAVEGSLHVKPPQFTWAQWFETQHINMTSQQCTNAMQVINNYQRRCKNQNTFLLTTFANVVNVCGNPNMTCPSNKTRKNCHHSGSQVPLIHCNLTTPSPQNISNCRYAQTPANMFYIVACDNRDQRRDPPQYPVVPVHLDRII')
        ]

    def test_to_one_hot_three_characters_has_three_tensors(self):
        alphabet_22  = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")
        kmer_arn = Kmer(site=42, subsequence="ARN")
        result = Predict.to_one_hot(kmer_arn, alphabet_22)
        assert result == [0, 1, 2]

    def test_on_kmers_returns_valid_probability(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.ALL_ORGANISM
        label = LabelKind.WITH_LABELS
        h5_file = Model.get_h5_file(ptm, organism, label)
        alphabet = Model.get_alphabet(ptm, organism, label)

        kmer_length = 53
        sequence_1 = "MTM"
        site_1 = 2
        kmer_1 = Kmer.site_to_kmer(sequence_1, site_1, kmer_length)

        sequence_2 = "TMM"
        site_2 = 1
        kmer_2 = Kmer.site_to_kmer(sequence_2, site_2, kmer_length)

        kmers = [kmer_1, kmer_2]
        probabilities = Predict.on_kmers(kmers, alphabet, h5_file)

        for probability in probabilities:
            assert 0 <= probability <= 1
    
    def test_on_fasta_returns_valid_sequence_predictions_one_sequence(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.ALL_ORGANISM
        label = LabelKind.WITH_LABELS
        with open(self.one_sequence_path, 'r') as f:
            text = f.read()
        
        sequence_predictions = Predict.on_fasta(text, ptm, organism, label)
        sequence_predictions = sequence_predictions.sequence_predictions

        assert len(sequence_predictions) == 1
        sequence_prediction = sequence_predictions[0]
        assert sequence_prediction.sequence_name == self.one_sequences_sequences[0].sequence_name
        for site_prediction in sequence_prediction.site_predictions:
            assert site_prediction.amino_acid in ptm.value.amino_acids
            assert 0 <= site_prediction.probability <= 1
        
        # Check that the number of sites is correct
        sequences = Fasta.read_sequences_from_text(text)
        expected_num_sites = sum([sequence.sequence.count(amino_acid) for amino_acid in ptm.value.amino_acids for sequence in sequences])
        actual_num_sites = len(sequence_prediction.site_predictions)
        assert expected_num_sites == actual_num_sites
    
    def test_on_fasta_returns_valid_sequences_predictions_two_sequences(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.ALL_ORGANISM
        label = LabelKind.WITH_LABELS
        with open(self.two_sequences_path, 'r') as f:
            text = f.read()
        sequence_predictions = Predict.on_fasta(text, ptm, organism, label)
        sequence_predictions = sequence_predictions.sequence_predictions

        assert len(sequence_predictions) == 2
        valid_sequence_names = [sequence.sequence_name for sequence in self.two_sequences_sequences]
        for sequence_prediction in sequence_predictions:
            assert sequence_prediction.sequence_name in valid_sequence_names
            for site_prediction in sequence_prediction.site_predictions:
                assert site_prediction.amino_acid in ptm.value.amino_acids
                assert 0 <= site_prediction.probability <= 1
        
        # Check that the number of sites is correct
        sequences = Fasta.read_sequences_from_text(text)
        for i, sequence in enumerate(sequences):
            expected_num_sites = sum([sequence.sequence.count(amino_acid) for amino_acid in ptm.value.amino_acids])
            actual_num_sites = len(sequence_predictions[i].site_predictions)
            assert expected_num_sites == actual_num_sites



class TestSequencePredictions:
    def test_to_dict(self):
        sequence_prediction = SequencePrediction(
            sequence_name='sequence_name', 
            sequence='STAAS',
            site_predictions=[
                SitePrediction(site=1, amino_acid='S', probability=0.2366819679737091), 
                SitePrediction(site=5, amino_acid='S', probability=0.3237350881099701), 
                SitePrediction(site=2, amino_acid='T', probability=0.1932818591594696),
            ])
        sequence_predictions = SequencePredictions([sequence_prediction])

        expected_to_dict = {
            'sequence_predictions': [
                {
                    'sequence_name': 'sequence_name',
                    'sequence': 'STAAS',
                    'site_predictions': [
                        {'site': 1, 'amino_acid': 'S', 'probability': 0.2366819679737091},
                        {'site': 5, 'amino_acid': 'S', 'probability': 0.3237350881099701},
                        {'site': 2, 'amino_acid': 'T', 'probability': 0.1932818591594696}
                    ]
                }
            ]
        }
        
        assert sequence_predictions.to_dict() == expected_to_dict