import numpy as np
from typing import List
import tensorflow as tf
from dataclasses import dataclass, asdict

from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.model import Model
from sitetack.app.fasta import Fasta

@dataclass(frozen=True)
class SitePrediction:
    """ Contains the prediction for a site """
    site: int
    amino_acid: str
    probability: float

@dataclass(frozen=True)
class SequencePrediction:
    """ Contains the predictions for a sequence """
    sequence_name: str
    sequence: str
    site_predictions: List[SitePrediction]

@dataclass(frozen=True)
class SequencePredictions:
    """ Contains the predictions for a list of sequences """
    sequence_predictions: List[SequencePrediction]


    def to_dict(self):
       return asdict(self)
       



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

    def on_kmers(kmers: List[Kmer], alphabet: Alphabet, model_file) -> List[float]:
      """
      Predicts the probability that the amino acid centered in the kmer is a phosphorylation site for all kmers. 

      Parameters:
          kmer: The kmers to predict on
          alphabet: The alphabet used to encode the kmer.
        
      Returns:
          A array of probabilities, one for each kmer,
          e.g. [0.1, 0.9]
      """        
      tensor = Predict._tensor_encoding(kmers, alphabet)
      model = tf.keras.models.load_model(model_file)
      result =  model.predict(tensor)
      # convert the result to a list of floats
      return [float(probability) for probability in result]
    
    @staticmethod
    def on_fasta(fasta_text: str, ptm: PtmKind, organism: OrganismKind, label: LabelKind) -> SequencePredictions:
      """
      Predicts the probabilities that the sites are phosphorylation sites for all kmers in the fasta text.

      Parameters:
          fasta_text: The fasta text to predict on
          ptm: The PTM to predict on
          organism: The organism to predict on
          label: The label to predict on
      
      Returns:
          A list of SequencePredictions, one for each sequence in the fasta text
      """
      alphabet = Model.get_alphabet(ptm, organism, label)
      sequences = Fasta.read_sequences_from_text(fasta_text)
      h5_file = Model.get_h5_file(ptm, organism, label)
      sequence_predictions = []
      for sequence in sequences:
          kmers = [kmer for amino_acid in ptm.value.amino_acids for kmer in sequence.get_kmers(Predict.KMER_LENGTH, amino_acid)]
          probabilities = Predict.on_kmers(kmers, alphabet, h5_file)
          site_predictions = [SitePrediction(kmer.site, kmer.amino_acid, probability) for kmer, probability in zip(kmers, probabilities)]
          sequence_predictions.append(SequencePrediction(sequence.sequence_name, sequence.sequence, site_predictions))
      return SequencePredictions(sequence_predictions)
