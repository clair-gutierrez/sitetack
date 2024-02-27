from pathlib import Path
from typing import List
from sitetack.app.sequence import Sequence



class Fasta:
    """ For reading fasta files. """
    
    @staticmethod
    def read_sequences_from_file(fasta_file: Path) -> List[Sequence]:
        """
        Read a fasta file and returns a list of Sequences.
        """
        sequences: List[Sequence] = []  
        # Open the fasta file, and read the lines using read_sequences_from_text
        with open(fasta_file, 'r') as f:
            sequences = Fasta.read_sequences_from_text(f.read())
        return sequences
    
    @staticmethod
    def read_sequences_from_text(fasta_text: str) -> List[Sequence]:
        """
        Parses a FASTA formatted text and returns a dictionary with the sequence IDs as keys
        and a tuple containing the name (description) and sequence as values.

        Parameters:
        fasta_text (str): A string containing FASTA formatted text.

        Returns:
        dict: A dictionary with sequence IDs as keys and tuples of (name, sequence) as values.
        """
        sequences: List[Sequence] = []  
        uniprot_id: str = ""  # Initialize uniprot_id as an empty string
        sequence: str = ""  # Initialize sequence as an empty string
        lines = fasta_text.strip().split('\n')

        for line in lines:
            if line.startswith('>'):
                if uniprot_id:  # Check if uniprot_id is not an empty string
                    sequences.append(Sequence(uniprot_id, sequence))
                uniprot_id = line[1:].strip()
                sequence = ''  # Reset sequence for the next record
            else:
                sequence += line.strip()  # Concatenate the sequence line

        if uniprot_id:  # Check for the last record
            sequences.append(Sequence(uniprot_id, sequence))

        return sequences
    

