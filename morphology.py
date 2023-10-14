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
class Morphology:
	status: Literal["FOUND_IN_DATABASE", "NOT_FOUND"]
	tree: Optional[List[Morpheme | FreeMorpheme]]


@dataclass
class FormattedMorpheme:
	text: str
	type: Literal["root", "prefix", "suffix"]


m = Morphemes("./morphemes")

def get_morphemes(word: str):
	data = m.parse(word)
	return from_dict(data_class=Morphology, data=data)

def format_morpheme(morpheme: Morpheme):
	type = "suffix" if morpheme.type == "bound" else morpheme.type
	return FormattedMorpheme(text=morpheme.text, type=type)

def format_morphology(morphology: Morphology):
	formatted_morphemes: List[FormattedMorpheme] = []
	
	for morpheme in morphology.tree:
		if isinstance(morpheme, FreeMorpheme):
			formatted_morphemes.extend(map(format_morpheme, morpheme.children))
		else:
			formatted_morphemes.append(format_morpheme(morpheme))

	return formatted_morphemes
