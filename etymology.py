from typing import List

from type import FormattedMorpheme, FormattedMorphemeWithEtymology

import requests
from bs4 import BeautifulSoup


def extract_etymology_for_word(word: str):
	url = f"https://www.etymonline.com/word/{word}"
	page = requests.get(url)

	if page.status_code == 200:
		scraper = BeautifulSoup(page.content, "html.parser")

		etymology_section = scraper.find(class_="word__defination--2q7ZH")
		etymology_paragraph = etymology_section.findChild(name="p")

		return etymology_paragraph.text

def get_etymology_for_morpheme(morpheme: FormattedMorpheme):
	match morpheme.type:
		case "root":
			word = morpheme.text
		case "prefix":
			word = f"{morpheme.text}-"
		case "suffix":
			word = f"-{morpheme.text}"

	etymology = extract_etymology_for_word(word)

	return FormattedMorphemeWithEtymology(text=morpheme.text, type=morpheme.type, etymology=etymology)

def get_etymology_for_morphemes(morphemes: List[FormattedMorpheme]):
	return list(map(lambda morpheme: get_etymology_for_morpheme(morpheme), morphemes))
