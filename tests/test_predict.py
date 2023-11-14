import tensorflow as tf
import numpy as np
from sitetack.alphabet import Alphabet
from sitetack.kmer import Kmer
from sitetack.predict import Predict
from pathlib import Path

class TestPredict:

    @classmethod
    def setup_class(cls):
        cls.alphabet_22  = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")

        cls.kmer_arn = Kmer(site=42, subsequence="ARN")
        
        cls.model_file = Path(__file__).parent / 'resources' / 'cnn.h5'


    def test_to_indices_three_characters(self):
        assert Predict.to_indices(self.kmer_arn, self.alphabet_22) == [0, 1, 2]

    def test_to_one_hot_three_characters_has_three_tensors(self):
        depth = len(self.alphabet_22)
        # Expected one-hot encoded tensors
        expected = [
            np.eye(depth, dtype=np.float)[[0]],
            np.eye(depth, dtype=np.float)[[1]],
            np.eye(depth, dtype=np.float)[[2]],
        ]
        
        # Call the method under test.
        result = Predict.to_one_hot(self.kmer_arn, self.alphabet_22)
        
        # Now, use TensorFlow's assert_equal to compare tensors.
        for res_tensor, exp_tensor in zip(result, expected):
            tf.debugging.assert_equal(res_tensor, exp_tensor)

    def test_on_kmer_returns_valid_probability(self):
        kmer = Kmer(site=7, subsequence='----------MVPKLFTSQICLLLLLGLMGVEGSL')
        alphabet_24 = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")
        probability = Predict.on_kmer(kmer, alphabet_24, self.model_file)
        assert 0 <= probability <= 1
    