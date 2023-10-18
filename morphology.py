from typing import List

from type import FormattedMorpheme, FreeMorpheme, Morpheme, Morphology

from morphemes import Morphemes


m = Morphemes("./morphemes")

def get_morphemes(word: str):
	data = m.parse(word)
	return Morphology.model_validate(data)

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
