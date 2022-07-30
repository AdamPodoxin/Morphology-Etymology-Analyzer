from morphemes import Morphemes


def get_morphs(word):
    m = Morphemes("./morphemes")
    return m.parse(word)


def get_root_spliced(root):
    return list(filter(lambda morph: len(morph) > 0, root.split('<')))
