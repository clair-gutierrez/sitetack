import numpy as np
from typing import List, Tuple
import tensorflow as tf

from sitetack.alphabet import Alphabet
from sitetack.kmer import Kmer

class Predict:
    """ Contains methods for making predictions on sequences """

    @staticmethod
    def to_indices(kmer: Kmer, alphabet: Alphabet) -> List[int]:
        """
        Convert a string sequence of amino acids to a list of integers representing the
        one-hot encoding of the kmer

        Parameters:
        - kmer: A kmer to be encoded. Each character in the kmer should be a valid character in alphabet.
        - alphabet: alphabet for amino acid sequences

        Returns:
        - A list of integers where each integer represents the position of an amino acid
          in alphabet.

        Example:
        >>> ProteinEncoder.to_indices("ARN", "ARNDCEQGHILKMFPSTWYV-U")
        [0, 1, 2]

        Note:
        - The method assumes that the input kmer contains only valid amino acid characters
          as defined in the alphabet. If an invalid character is encountered, a KeyError will be raised.
        """
        #  maps each character in the alphabet to a unique integer
        char_to_int = {c: i for i, c in enumerate(alphabet)}
        return [char_to_int[char] for char in kmer]
    
    @staticmethod
    def to_one_hot(kmer: Kmer, althabet: Alphabet) -> List[tf.Tensor]:
        """
        Convert a kmer into their corresponding one-hot encoded tensors.
        The depth of the one-hot encoding, i.e., the number of unique categories
        that each index can represent is equal to the length of the alphabet

        Parameters:
        - kmer: A kmer to be converted into one-hot format
        - alphabet: alphabet for amino acid sequences

        Returns:
        - A list of one-hot encoded tensors corresponding to the input kmer
        """
        depth = len(althabet)
        return [tf.one_hot(Predict.to_indices(item, althabet), depth) for item in kmer]

    @staticmethod
    def on_kmer(kmer: Kmer, alphabet: Alphabet, model_file="cnn.h5") -> float:
      """
      Predicts the probability that the amino acid centered in the kmer is a phosphorylation site. 

      Parameters:
          kmer: The kmer to predict on
          alphabet: The alphabet used to encode the kmer.
        
      Returns:
        A probability in the range [0, 1]
      """        
      one_hot_kmer = Predict.to_one_hot(kmer, alphabet)
      tensor = tf.convert_to_tensor(one_hot_kmer)
      dataset = tf.reshape(tensor, (-1, 35, len(alphabet), 1))
      new_model = tf.keras.models.load_model(model_file)
      array = new_model.predict(dataset)
      return array[0][0]
