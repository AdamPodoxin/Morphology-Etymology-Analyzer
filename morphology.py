from dataclasses import dataclass
from typing import Literal, Optional, List
from morphemes import Morphemes
from dacite import from_dict


@dataclass
class Morpheme:
    text: str
    type: Literal["root", "prefix", "bound"]


@dataclass
class FreeMorpheme:
    type: Literal["free"]
    children: List[Morpheme]


@dataclass
class ParsedMorphology():
    status: Literal["FOUND_IN_DATABASE", "NOT_FOUND"]
    word: str
    tree: Optional[List[Morpheme | FreeMorpheme]]


m = Morphemes("./morphemes")

def get_morphemes(word: str):
    data = m.parse(word)
    return from_dict(data_class=ParsedMorphology, data=data)

