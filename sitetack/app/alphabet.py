from dataclasses import dataclass


@dataclass(frozen=True)
class Alphabet:
    """
    Represents the standard alphabet for amino acid sequences,
                    including a dash for gaps or unknown amino acids.
                    For example, "ARNDCEQGHILKMFPSTWYV-U"
    """

    str: str

    def __post_init__(self):
        # check that all characters are unique
        if len(self.str) != len(set(self.str)):
            raise ValueError("Alphabet must not contain duplicate characters")

    def __len__(self):
        """ Return the length of the alphabet """
        return len(self.str)

    def __iter__(self):
        """ Make the alphabet iterable by returning an iterator over the string """
        return iter(self.str)
