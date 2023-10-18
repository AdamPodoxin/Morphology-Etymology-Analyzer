from pydantic import BaseModel, Field

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from google.cloud.firestore_v1.document import DocumentReference

from db import WordDoc, get_word_doc_from_db

from morphology import get_morphemes, format_morphology
from etymology import FormattedMorphemeWithEtymology, get_etymology_for_morphemes, extract_etymology_for_word


class Analysis(BaseModel):
	word: str
	etymology: str
	morphemes_with_etymology: list[FormattedMorphemeWithEtymology] = Field(..., alias="morphemesWithEtymology")

	class Config:
		populate_by_name = True


def analyze_word(word: str):
	morphology = get_morphemes(word)

	match morphology.status:
		case "FOUND_IN_DATABASE":
			formatted_morphemes = format_morphology(morphology)
			formatted_morphemes_with_etymology = get_etymology_for_morphemes(formatted_morphemes)

			analysis = Analysis(word=word, etymology=extract_etymology_for_word(word), morphemes_with_etymology=formatted_morphemes_with_etymology)

			return JSONResponse(analysis.model_dump(by_alias=True))
		case "NOT_FOUND":
			return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
		case _:
			return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_analysis_from_db(word_doc: WordDoc):
	morphemes = list(map(lambda doc: FormattedMorphemeWithEtymology.model_validate(doc.get().to_dict()), word_doc.morphemes))

	analysis = Analysis(word=word_doc.word, etymology=word_doc.etymology, morphemesWithEtymology=morphemes)
	
	return JSONResponse(analysis.model_dump(by_alias=True))


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
	return "Please specify a word with /{word}"

@app.get("/{word}")
async def analyze(word: str):
	print("Analyzing word:", word)

	word_doc = get_word_doc_from_db(word)

	if word_doc:
		return get_analysis_from_db(word_doc)
	else:
		return analyze_word(word)
