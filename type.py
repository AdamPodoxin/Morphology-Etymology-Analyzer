from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from google.cloud.firestore_v1.document import DocumentReference


# DB

class WordDoc(BaseModel):
	word: str
	etymology: str | None
	morphemes_refs: list[DocumentReference]

	class Config:
		arbitrary_types_allowed = True


# Morphology

class Morpheme(BaseModel):
	text: str
	type: Literal["root", "prefix", "bound"]


class FreeMorpheme(BaseModel):
	type: Literal["free"]
	children: List[Morpheme]


class Morphology(BaseModel):
	status: Literal["FOUND_IN_DATABASE", "NOT_FOUND"]
	tree: Optional[List[Morpheme | FreeMorpheme]]


class FormattedMorpheme(BaseModel):
	text: str
	type: Literal["root", "prefix", "suffix"]


# Etymology

class FormattedMorphemeWithEtymology(FormattedMorpheme):
	etymology: str


# Main

class Analysis(BaseModel):
	word: str
	etymology: str | None
	morphemes_with_etymology: list[FormattedMorphemeWithEtymology] = Field(..., alias="morphemesWithEtymology")

	class Config:
		populate_by_name = True
