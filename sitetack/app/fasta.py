from pathlib import Path
from typing import List
from sitetack.app.sequence import Sequence


class Fasta:
    """ For reading fasta files. """

    @staticmethod
    def read_sequences(fasta_file: Path) -> List[Sequence]:
        """
        Read a fasta file and returns a list of Sequences.
        """
        sequences: List[Sequence] = []
        uniprot_id: str = ""  # Initialize uniprot_id as an empty string
        sequence: str = ""  # Initialize sequence as an empty string

        with open(fasta_file) as f:
            for line in f:
                if line.startswith(">"):
                    if uniprot_id:  # Check if uniprot_id is not an empty string
                        sequences.append(Sequence(uniprot_id, sequence))
                    uniprot_id = line[1:].strip()
                    sequence = ""  # Reset sequence for the next record
                else:
                    sequence += line.strip()  # Concatenate the sequence line

            if uniprot_id:  # Check for the last record
                sequences.append(Sequence(uniprot_id, sequence))

        return sequences
