from sitetack.fasta import Fasta
from sitetack.sequence import Sequence
from sitetack.kmer import Kmer
from sitetack.predict import Predict
import tensorflow as tf

if __name__ == "__main__":
    sequence = Fasta.read_sequences('tests/resources/one_sequence.fasta').pop()
    print(f"sequence: {sequence}")

    kmers = sequence.get_kmers(35, 'S')
    print(f"kmers: {kmers}")

    kmer = kmers[0]
    print(f"kmer: {kmer}")

    alphabet = "ARNDCEQGHILKMFPSTWYVXZ-U"
    one_hot_kmer = Predict.to_one_hot(kmer, alphabet)

    tensor = tf.convert_to_tensor(one_hot_kmer)
    print(f"tensor.shape: {tensor.shape}")


    dataset = tf.reshape(tensor, (-1, 35, len(alphabet), 1))
    print(f"dataset.shape: {dataset.shape}")

    new_model = tf.keras.models.load_model(f'cnn.h5')

    predictions = new_model.predict(dataset)
    print(f"predictions: {predictions}")




