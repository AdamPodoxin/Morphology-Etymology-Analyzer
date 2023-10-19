from type import Analysis, FormattedMorphemeWithEtymology

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db import WordDoc, get_word_doc_from_db, write_analysis_to_db

from morphology import get_morphemes, format_morphology
from etymology import get_etymology_for_morphemes, extract_etymology_for_word


def analyze_word(word: str):
	morphology = get_morphemes(word)

	match morphology.status:
		case "FOUND_IN_DATABASE":
			formatted_morphemes = format_morphology(morphology)
			formatted_morphemes_with_etymology = get_etymology_for_morphemes(formatted_morphemes)

			analysis = Analysis(word=word, etymology=extract_etymology_for_word(word), morphemes_with_etymology=formatted_morphemes_with_etymology)
			post_analysis_to_db(analysis)

			return JSONResponse(analysis.model_dump(by_alias=True))
		case "NOT_FOUND":
			return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
		case _:
			return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_analysis_from_db(word_doc: WordDoc):
	morphemes = list(map(lambda doc: FormattedMorphemeWithEtymology.model_validate(doc.get().to_dict()), word_doc.morphemes_refs))

	analysis = Analysis(word=word_doc.word, etymology=word_doc.etymology, morphemesWithEtymology=morphemes)
	
	return JSONResponse(analysis.model_dump(by_alias=True))


def post_analysis_to_db(analysis: Analysis):
	try:
		write_analysis_to_db(analysis)
	except:
		print(f"Error posting analysis for '{analysis.word}' to database")


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
