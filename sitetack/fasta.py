from pathlib import Path
from typing import List
from sitetack.sequence import Sequence



class Fasta:
    """ For reading fasta files. """
    
    @staticmethod
    def read_sequences(fasta_file: Path) -> List[Sequence]:
        """
        Read a fasta file and returns a list of Sequences.

        For example, if the fasta file contains:
        >RNase_1
        MALEKSLVRLLLLVLILLVLGWVQPSLGKESRAKKFQRQHMDSDSSPSSSSTYCNQMMRR
        RNMTQGRCKPVNTFVHEPLVDVQNVCFQEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRY
        PNCAYRTSPKERHIIVACEGSPYVPVHFDASVEDST

        Returns:
        Sequences([
            Sequence(uniprot_id='RNase_1', sequence='MALEKSLVRLLLLVLILLVLGWVQPSLGKESRAKKFQRQHMDSDSSPSSSSTYCNQMMRRRNMTQGRCKPVNTFVHEPLVDVQNVCFQEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRYPNCAYRTSPKERHIIVACEGSPYVPVHFDASVEDST')
        ]
        """
        sequences = []
        with open(fasta_file) as f:
            uniprot_id = None
            sequence = None
            for line in f:
                if line.startswith('>'):
                    if uniprot_id is not None:
                        sequences.append(Sequence(uniprot_id, sequence))
                    uniprot_id = line[1:].strip()
                    sequence = ''
                else:
                    sequence += line.strip()
            if uniprot_id is not None:
                sequences.append(Sequence(uniprot_id, sequence))
        return sequences
