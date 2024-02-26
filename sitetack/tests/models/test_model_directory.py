import importlib
from pathlib import Path
from typing import List
import tensorflow as tf

"""
Inside of the models directory there are ptm directories, and inside of the ptm directories there are organism directories.
models -> ptm -> organism -> h5 files
"""

class TestModelDirectory:
    
    @classmethod
    def setup_class(cls):
        # model directory is in sitetacks.models
        cls.models_directory = cls.get_directory_from_module('sitetack.models')
    
    @staticmethod
    def get_directory_from_module(module: str) -> Path:
        """ Get the directory of a module.

            Parameters:
                module (str): The name of the module, e.g. 'sitetack.models'.
            Returns:
                Path: The directory of the module.
        """
        spec = importlib.util.find_spec(module)
        return Path(spec.origin).parent

    @classmethod
    def get_all_valid_h5_files(cls) -> List[Path]:
        """ Get all the valid h5 files in the models directory.

            Returns:
                list[Path]: A list of all the h5 files in the models directory.
        """
        h5_files = []
        ptm_directories = [d for d in cls.models_directory.iterdir() if d.is_dir()]

        # For each PTM directory ...
        for ptm_directory in ptm_directories:
            organism_directories = [d for d in ptm_directory.iterdir() if d.is_dir()]

            # For each organism directory, check that there are two h5 files
            for organism_directory in organism_directories:
                h5_files = list(organism_directory.glob('*.h5'))
                h5_files.extend(h5_files)
        return h5_files

    
    def test_ptm_directory_has_two_subdirectories(self):
        directory_name_1 = "Human"
        directory_name_2 = "All organism"

        # All the subdirectories in the models directory, represents PTM models
        ptm_directories = [d for d in self.models_directory.iterdir() if d.is_dir()]

        # Check that each PTM directory has two subdirectories
        # One for human and one for all organisms
        for ptm_directory in ptm_directories:
            organism_directory_names = [d.name for d in ptm_directory.iterdir() if d.is_dir()]
            assert directory_name_1 in organism_directory_names
            assert directory_name_2 in organism_directory_names
            assert len(organism_directory_names) == 2
    
    def test_organism_directory_has_two_models(self):
        # All the subdirectories in the models directory, represents PTM models
        ptm_directories = [d for d in self.models_directory.iterdir() if d.is_dir()]

        # For each PTM directory ...
        for ptm_directory in ptm_directories:
            organism_directories = [d for d in ptm_directory.iterdir() if d.is_dir()]

            # For each organism directory, check that there are two h5 files
            for organism_directory in organism_directories:
                h5_files = list(organism_directory.glob('*.h5'))
                assert len(h5_files) == 2

    def test_h5_files_labeled_correctly(self):
        # All the subdirectories in the models directory, represents PTM models
        ptm_directories = [d for d in self.models_directory.iterdir() if d.is_dir()]

        # For each PTM directory ...
        for ptm_directory in ptm_directories:
            organism_directories = [d for d in ptm_directory.iterdir() if d.is_dir()]

            # For each organism directory, check that there are two h5 files
            for organism_directory in organism_directories:
                h5_files = list(organism_directory.glob('*.h5'))
                # one file should contain the word "no_labels", the other should contain the word "with_labels"
                for h5_file in h5_files:
                    if "no_labels" in h5_file.name:
                        assert "no_labels" in h5_file.stem
                    else:
                        assert "with_labels" in h5_file.stem
    
    def test_all_h5_files_are_valid_models(self):
        h5_files = self.get_all_valid_h5_files()
        for h5_file in h5_files:
            assert tf.keras.models.load_model(h5_file) is not None





        
       