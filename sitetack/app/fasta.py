from pathlib import Path
from typing import List, Tuple
from sitetack.app.alphabet import Alphabet
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
        sequence_name: str = ""  # Initialize sequence_name as an empty string
        sequence: str = ""  # Initialize sequence as an empty string
        lines = fasta_text.strip().split('\n')

        for line in lines:
            if line.startswith('>'):
                if sequence_name:  # Check if sequence_name is not an empty string
                    sequences.append(Sequence(sequence_name, sequence))
                sequence_name = line[1:].strip()
                sequence = ''  # Reset sequence for the next record
            else:
                sequence += line.strip()  # Concatenate the sequence line

        if sequence_name:  # Check for the last record
            sequences.append(Sequence(sequence_name, sequence))

        return sequences
    
    
    @staticmethod
    def validate_fasta_text(fasta_text: str, alphabet: Alphabet) -> Tuple[bool, str]:
        """
        Validates the format of a given FASTA text.

        Parameters:
        fasta_text (str): A string containing FASTA formatted text.

        Returns:
        Tuple[bool, str]: A tuple where the first element is a boolean indicating
                        whether the FASTA text is valid or not, and the second
                        element is an error message if the text is invalid.
        """
        unique_sequence_names = set()
        if not fasta_text.strip():
            return False, "The FASTA text is empty."
        
        lines = fasta_text.strip().split('\n')
        if not lines[0].startswith('>'):
            return False, "The FASTA text must start with a header line (>)."
        
        valid_chars = set(alphabet.str)  # For nucleotides, including ambiguity codes

        sequence_started = False
        for line in lines:
            if line.startswith('>'):
                if sequence_started:  # A new header starts, so reset the flag
                    sequence_started = False

                # Also, make sure the header is unique
                sequence_name = line[1:].strip()
                print(f"sequence_name: {sequence_name}")
                if sequence_name in unique_sequence_names:
                    return False, f"Duplicate sequence name found: {sequence_name}"
                else:
                    unique_sequence_names.add(sequence_name)
                continue
            else:
                sequence_started = True
                if not set(line.strip()).issubset(valid_chars):
                    return False, f"Invalid character found in sequence. Valid characters are: {alphabet.str}"
        
        if not sequence_started:  # No sequence lines found after headers
            return False, "No sequence data found after header lines."
        
        return True, "The FASTA text is valid."