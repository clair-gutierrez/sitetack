from dataclasses import dataclass, field


@dataclass(frozen=True)
class Alphabet:
    """
    Represents the standard alphabet for amino acid sequences,
                    including a dash for gaps or unknown amino acids.
                    For example, "ARNDCEQGHILKMFPSTWYV-U"
    """
    str: str
    length: int = field(init=False)

    def __post_init__(self):
        # check that all characters are unique
        assert len(set(self.str)) == len(self.str), "Alphabet contains duplicate characters"

        self.length = len(self.str)




