""" Keeps track of the model configurations """

from sitetack.app.enums import PtmKind, OrganismKind, LabelKind
from sitetack.app.alphabet import Alphabet
from pathlib import Path
import importlib.util
import pandas


class Model:
    """ Given a set of PTM, organism and label, this class represents a model """

    def __init__(self, ptm: PtmKind, organism: OrganismKind, label: LabelKind):
        """
        Given a ptm choice, an organism choice and a label choice, this class will load
        the corresponding model from the models directory

        Parameters:
            ptm: The PTM to use, e.g. phosphorylation
            organism: The organism to use, e.g. human or all organism
            label: The label to use, e.g. with labfels or no labels
        """
        self._ptm = ptm
        self._organism = organism
        self._label = label

    @classmethod
    def model_directory_path(cls):
        """ Get the path to the models directory."""
        return cls.get_directory_from_module("sitetack.models")

    @classmethod
    def master_file_path(cls):
        """ Get the path to the master file, which contains ptm, organism and label, and alphabet information."""
        return cls.model_directory_path() / "master_info.xlsx"

    @staticmethod
    def get_directory_from_module(module: str) -> Path:
        """ Get the directory of a module.

            Parameters:
                module (str): The name of the module, e.g. 'sitetack.models'.
            Returns:
                Path: The directory of the module.
        """
        spec = importlib.util.find_spec(module)
        if spec is not None and spec.origin is not None:
            return Path(spec.origin).parent
        raise ValueError(f"Module {module} not found")

    @classmethod
    def get_h5_file(
        cls, ptm: PtmKind, organism: OrganismKind, label: LabelKind
    ) -> Path:
        """ Get the h5 file for a given PTM, organism and label.

            Parameters:
                ptm (PtmKind): The PTM to use
                organism (OrganismKind): The organism to use
                label (LabelKind): The label to use        
        """
        ptm_directory_name = ptm.value.directory_name
        organism_directory_name = organism.value.directory_name
        organism_directory = (
            cls.model_directory_path() / ptm_directory_name / organism_directory_name
        )
        h5_files = list(organism_directory.glob("*.h5"))
        label_query = label.value.filename_query
        for h5_file in h5_files:
            if label_query in h5_file.name:
                return h5_file
        raise FileNotFoundError(f"No h5 file found for {ptm}, {organism}, {label}")

    @classmethod
    def get_alphabet(
        cls, ptm: PtmKind, organism: OrganismKind, label: LabelKind
    ) -> Alphabet:
        """ Get the alphabet for a given PTM, organism and label.

            Parameters:
                ptm (PtmKind): The PTM to use
                organism (OrganismKind): The organism to use
                label (LabelKind): The label to use
            Returns:
                Alphabet: The alphabet for the given PTM, organism and label
        """
        df = pandas.read_excel(cls.master_file_path())
        dataset_df = df[df["Dataset"] == "Musite Deep"]
        ptm_df = dataset_df[dataset_df["PTM"] == ptm.value.directory_name]
        organism_df = ptm_df[ptm_df["Organism"] == organism.value.directory_name]

        # organism_df should have only one row
        if len(organism_df) != 1:
            raise RuntimeError(
                f"Expected one row for {ptm}, {organism}, {label} but got {len(organism_df)}"
            )

        if label == LabelKind.NO_LABELS:
            alphabet = organism_df["Alphabet no labels"].values[0]
        elif label == LabelKind.WITH_LABELS:
            alphabet = organism_df["Alphabet labels"].values[0]
        else:
            raise ValueError(f"Unknown label {label}")

        return Alphabet(str=alphabet)
