import importlib
import tensorflow as tf
import numpy as np
from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer
from sitetack.app.predict import Predict
from pathlib import Path

class TestPredict:

    @classmethod
    def setup_class(cls):
        cls.alphabet_22  = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")

        cls.kmer_arn = Kmer(site=42, subsequence="ARN")

        with importlib.resources.path('sitetack.tests.resources', 'cnn.h5') as file_path:
            cls.model_file = Path(file_path)


        


    def test_to_indices_three_characters(self):
        assert Predict.to_indices(self.kmer_arn, self.alphabet_22) == [0, 1, 2]

    def test_to_one_hot_three_characters_has_three_tensors(self):
        depth = len(self.alphabet_22)
        # Expected one-hot encoded tensors
        expected = [
            np.eye(depth, dtype=np.float32)[[0]], # pyright: ignore [reportGeneralTypeIssues]
            np.eye(depth, dtype=np.float32)[[1]], # pyright: ignore [reportGeneralTypeIssues]
            np.eye(depth, dtype=np.float32)[[2]], # pyright: ignore [reportGeneralTypeIssues]
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
    