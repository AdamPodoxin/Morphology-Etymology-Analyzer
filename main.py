import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from morphology import get_morphemes, format_morphology


app = FastAPI()

@app.get("/")
async def root():
    return "Please specify a word with /{word}"

@app.get("/{word}")
async def analyze_route(word: str):
    print("Analyzing word:", word)

    morphology = get_morphemes(word)
    match morphology.status:
        case "FOUND_IN_DATABASE":
            formatted_morphemes = format_morphology(morphology)
            return JSONResponse(jsonable_encoder(formatted_morphemes))
        case "NOT_FOUND":
            return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
        case _:
            return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
