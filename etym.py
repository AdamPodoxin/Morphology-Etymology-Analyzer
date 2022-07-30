import requests
from bs4 import BeautifulSoup


def get_etym(word):
    URL = f"https://www.etymonline.com/word/{word}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        section = soup.find_all("section", class_="word__defination--2q7ZH")[0]
        first_para = section.find("p")
        etym_text = first_para.text

        return etym_text
    except:
        return "404"


arr = filter(lambda morph: len(morph) > 0, "<re<<in<carn".split('<'))
for i in arr:
    print(i)
