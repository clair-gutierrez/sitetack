import importlib
import tensorflow as tf
import numpy as np
from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer
from sitetack.app.predict import Predict
from pathlib import Path
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.model import Model

class TestPredict:

    def test_to_one_hot_three_characters_has_three_tensors(self):
        alphabet_22  = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")
        kmer_arn = Kmer(site=42, subsequence="ARN")
        result = Predict.to_one_hot(kmer_arn, alphabet_22)
        assert result == [0, 1, 2]

    def test_on_kmer_returns_valid_probability(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.ALL_ORGANISM
        label = LabelKind.WITH_LABELS
        h5_file = Model.get_h5_file(ptm, organism, label)
        alphabet = Model.get_alphabet(ptm, organism, label)

        kmer_length = 53
        sequence_1 = "MTM"
        site_1 = 1
        kmer_1 = Kmer.site_to_kmer(sequence_1, site_1, kmer_length)

        sequence_2 = "TMM"
        site_2 = 0
        kmer_2 = Kmer.site_to_kmer(sequence_2, site_2, kmer_length)

        kmers = [kmer_1, kmer_2]
        probabilities = Predict.on_kmer(kmers, alphabet, h5_file)

        for probability in probabilities:
            assert 0 <= probability <= 1
    