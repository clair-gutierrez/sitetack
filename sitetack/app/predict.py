import numpy as np
from typing import List
import tensorflow as tf

from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer


class Predict:
    """ Contains methods for making predictions on sequences """

    KMER_LENGTH = 53

    @staticmethod
    def to_one_hot(kmer: Kmer, alphabet) -> List[int]:
        """
      Converts a kmer into a one-hot list of integers.

      Parameters:
      - kmer: A kmer to be converted into one-hot format
      - alphabet: alphabet for amino acid sequences

      Returns:
      - A list of one-hot encoded integers corresponding to the input kmer
      """
        # Creates a dict, that maps to every char of alphabet an unique int based on position
        char_to_int = {c: i for i, c in enumerate(alphabet)}
        return [char_to_int[char] for char in kmer.subsequence]

    @staticmethod
    def _tensor_encoding(kmers: List[Kmer], alphabet: Alphabet) -> np.ndarray:
        """
      Encodes a list of kmers into a np.ndarray of one-hot encoded tensors.
      
      Parameters:
      - kmers: A list of kmers to be encoded
      - alphabet: alphabet for amino acid sequences
      Returns:
      - A np.ndarray of one-hot encoded tensors
      """
        indices = [Predict.to_one_hot(kmer, alphabet) for kmer in kmers]
        assert all(
            len(one_hot) == Predict.KMER_LENGTH for one_hot in indices
        ), "All one-hot encodings must have the correct length"
        return np.stack(indices, axis=0)

    @staticmethod
    def on_kmer(kmers: List[Kmer], alphabet: Alphabet, model_file) -> np.ndarray:
        """
      Predicts the probability that the amino acid centered in the kmer is a phosphorylation site. 

      Parameters:
          kmer: The kmer to predict on
          alphabet: The alphabet used to encode the kmer.
        
      Returns:
          A np.ndarray of probabilities, one for each kmer,
          e.g. [0.1, 0.9]
      """
        tensor = Predict._tensor_encoding(kmers, alphabet)
        model = tf.keras.models.load_model(model_file)
        return model.predict(tensor)
