from typing import List 
import tensorflow as tf

from sitetack.alphabet import Alphabet

class Predict:
    """ Contains methods for making predictions on sequences """

    @classmethod
    def to_indices(cls, sequence: str, alphabet: Alphabet) -> List[int]:
        """
        Convert a string sequence of amino acids to a list of integers representing the
        one-hot encoding of the sequence.

        Parameters:
        - sequence: A string of amino acid characters to be encoded. Each character in the
                    string should be a valid character in alphabet.
        - alphabet: alphabet for amino acid sequences

        Returns:
        - A list of integers where each integer represents the position of an amino acid
          in alphabet.

        Example:
        >>> ProteinEncoder.to_indices("ARN", "ARNDCEQGHILKMFPSTWYV-U")
        [0, 1, 2]

        Note:
        - The method assumes that the input sequence contains only valid amino acid characters
          as defined in the alphabet. If an invalid character is encountered, a KeyError will be raised.
        """
        #  maps each character in the alphabet to a unique integer
        char_to_int = {c: i for i, c in enumerate(alphabet)}
        return [char_to_int[char] for char in sequence]
    
    @classmethod
    def to_one_hot(cls, sequence: str, althabet: Alphabet) -> List[tf.Tensor]:
        """
        Convert a sequence of indices into their corresponding one-hot encoded tensors.
        The depth of the one-hot encoding, i.e., the number of unique categories
        that each index can represent is equal to the length of the class's _ALPHABET.

        Parameters:
        - sequence: A sequence to be converted into one-hot format
        - alphabet: alphabet for amino acid sequences

        Returns:
        - A list of one-hot encoded tensors corresponding to the input sequence.
        """
        depth = len(cls._ALPHABET)
        return [tf.one_hot(cls._to_indices(item), depth) for item in sequence]

