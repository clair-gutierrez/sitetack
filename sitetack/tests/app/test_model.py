from sitetack.app.model import Model
from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.alphabet import Alphabet
from sitetack.app.kmer import Kmer
from sitetack.app.predict import Predict
import tensorflow as tf
from itertools import product
import pytest


class TestModel:
    def test_model_directory_path_is_dir(self):
        model_directory_path = Model.model_directory_path()
        assert model_directory_path.is_dir()

    def test_master_file_path_is_file(self):
        master_file_path = Model.master_file_path()
        assert master_file_path.is_file()

    def test_get_directory_from_module_valid_module(self):
        directory = Model.get_directory_from_module("sitetack.models")
        assert directory.is_dir()

    def test_get_h5_file_is_in_correct_path(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.HUMAN
        label = LabelKind.WITH_LABELS
        h5_file = Model.get_h5_file(ptm, organism, label)
        assert h5_file.is_file()
        assert h5_file.suffix == ".h5"
        assert ptm.value.directory_name in h5_file.parts
        assert organism.value.directory_name in h5_file.parts
        assert label.value.filename_query in h5_file.stem

    def test_get_h5_file_can_be_loaded(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.HUMAN
        label = LabelKind.NO_LABELS
        h5_file = Model.get_h5_file(ptm, organism, label)
        assert tf.keras.models.load_model(h5_file) is not None

    def test_get_alphabet_alphabet_exists_for_choices(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.HUMAN
        label = LabelKind.NO_LABELS
        alphabet = Model.get_alphabet(ptm, organism, label)
        assert isinstance(alphabet, Alphabet)

    def test_get_alphabet_get_h5_file_can_be_predicted(self):
        ptm = PtmKind.PHOSPHORYLATION_ST
        organism = OrganismKind.HUMAN
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

    @pytest.mark.parametrize(
        "ptm, organism, label", list(product(PtmKind, OrganismKind, LabelKind))
    )
    def test_get_alphabet_get_h5_file_all_can_be_predicted(self, ptm, organism, label):
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
