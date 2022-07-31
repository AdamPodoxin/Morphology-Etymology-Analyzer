from etym import get_etym
from morph import get_morphs, get_root_spliced


def build_morpheme(morph, type, etym):
    return {
        "morph": morph,
        "type": type,
        "etym": etym
    }


def get_prefixes(root_spliced):
    prefixes = []
    for i in range(len(root_spliced) - 1):
        current_morph = root_spliced[i]
        prefixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"{current_morph}-")))

        return prefixes


def get_suffixes(tree, tree_children):
    suffixes = []
    for i in range(1, len(tree_children)):
        current_morph = tree_children[i]["text"]
        suffixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"-{current_morph}")))

    for i in range(1, len(tree)):
        current_morph = tree[i]["text"]
        suffixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"-{current_morph}")))


def analyze(word):
    morphs = get_morphs(word)

    tree = morphs["tree"]
    tree_children = tree[0]["children"]
    root = tree_children[0]["text"]
    root_spliced = get_root_spliced(root)

    prefixes = get_prefixes(root_spliced)
    suffixes = get_suffixes(tree, tree_children)

    root_word = root_spliced[len(root_spliced) - 1]
    root_morph = build_morpheme(root_word, "free", get_etym(root_word))

    return {
        "prefixes": prefixes,
        "root": root_morph,
        "suffixes": suffixes
    }
