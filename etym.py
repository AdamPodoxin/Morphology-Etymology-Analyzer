import requests
from bs4 import BeautifulSoup


def get_etym(word):
    URL = f"https://www.etymonline.com/word/{word}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        section = soup.find_all("section", class_="word__defination--2q7ZH")[0]
        paras = section.findAll("p")
        first_para = paras[0]

        i = 0
        while i < len(paras) and len(first_para.text) == 0:
            i += 1
            first_para = paras[i]

        etym_text = first_para.text

        return etym_text
    except:
        if '-' in word:
            return get_etym(word.replace('-', ''))
        else:
            return ""
