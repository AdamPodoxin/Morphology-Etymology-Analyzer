from morphemes import Morphemes


def get_morphemes(word: str):
    m = Morphemes("./morphemes")
    return m.parse(word)


def splice_root(root: str):
    return list(filter(lambda morph: len(morph) > 0, root.split('<')))
