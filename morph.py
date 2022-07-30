from morphemes import Morphemes


def get_morphs(word):
    m = Morphemes("./morphemes")
    return m.parse(word)
