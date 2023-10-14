import requests
from bs4 import BeautifulSoup


def get_etymology(word: str) -> str:
	return ""
    # URL = f"https://www.etymonline.com/word/{word}"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")

    # try:
    #     section = soup.find_all("section", class_="word__defination--2q7ZH")[0]
    #     paragraphs = section.findAll("p")
    #     first_paragraph = paragraphs[0]

    #     i = 0
    #     while i < len(paragraphs) and len(first_paragraph.text) == 0:
    #         i += 1
    #         first_paragraph = paragraphs[i]

    #     etymology_text = first_paragraph.text

    #     return etymology_text
    # except:
    #     if '-' in word:
    #         return get_etymology(word.replace('-', ''))
    #     else:
    #         return ""
