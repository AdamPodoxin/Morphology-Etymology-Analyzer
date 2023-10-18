from pydantic import BaseModel, Field

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from morphology import get_morphemes, format_morphology
from etymology import FormattedMorphemeWithEtymology, get_etymology_for_morphemes, extract_etymology_for_word


class Analysis(BaseModel):
	word: str
	etymology: str
	morphemes_with_etymology: list[FormattedMorphemeWithEtymology] = Field(..., alias="morphemesWithEtymology")

	class Config:
		populate_by_name = True


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
	return "Please specify a word with /{word}"

@app.get("/{word}")
async def analyze(word: str):
	print("Analyzing word:", word)

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
