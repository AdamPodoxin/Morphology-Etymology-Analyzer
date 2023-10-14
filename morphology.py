from dataclasses import dataclass
from typing import Literal, Optional, List
from morphemes import Morphemes
from dacite import from_dict


m = Morphemes("./morphemes")


@dataclass
class ParsedMorphology():
    status: Literal["FOUND_IN_DATABASE", "NOT_FOUND"]
    word: str
    morpheme_count: int
    tree: Optional[List]

def get_morphemes(word: str):
    data = m.parse(word)
    return from_dict(data_class=ParsedMorphology, data=data)

