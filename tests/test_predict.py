import tensorflow as tf
import numpy as np
from sitetack.predict import Predict

class TestPredict:

    def setup_class(cls):
        cls.alphabet_22  = Alphabet("ARNDCEQGHILKMFPSTWYVXZ-U")

    def test_to_indices_three_characters(self):
        assert Predict._to_indices('ARN') == [0, 1, 2]
    
    def test_to_indices_no_characters(self):
        assert Predict._to_indices('') == []

    def test_to_one_hot_three_characters_has_three_tensors(self):
        depth = len(Predict._ALPHABET)
        # Expected one-hot encoded tensors
        expected = [
            np.eye(depth, dtype=np.float32)[[0]],
            np.eye(depth, dtype=np.float32)[[1]],
            np.eye(depth, dtype=np.float32)[[2]],
        ]
        
        # Call the method under test.
        result = Predict._to_one_hot('ARN')
        
        # Now, use TensorFlow's assert_equal to compare tensors.
        for res_tensor, exp_tensor in zip(result, expected):
            tf.debugging.assert_equal(res_tensor, exp_tensor)
    
    def test_to_one_hot_no_characters_returns_empty(self):
        assert Predict._to_one_hot('') == []