from etym import get_etym
from flask import Flask, request
from morph import get_morphs, get_root_spliced


def build_morpheme(morph, type, etym):
    return {
        "morph": morph,
        "type": type,
        "etym": etym
    }


# Init app
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/morphemes", methods=["GET"])
def morphemes():
    word = request.args["word"]

    morphs = get_morphs(word)

    prefixes = []
    root_morph = {}
    suffixes = []

    tree = morphs["tree"]
    tree_children = tree[0]["children"]
    root = tree_children[0]["text"]
    root_spliced = get_root_spliced(root)

    for i in range(len(root_spliced) - 1):
        current_morph = root_spliced[i]
        prefixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"{current_morph}-")))

    root_word = root_spliced[len(root_spliced) - 1]
    root_morph = build_morpheme(root_word, "free", get_etym(root_word))

    for i in range(1, len(tree_children)):
        current_morph = tree_children[i]["text"]
        suffixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"-{current_morph}")))

    for i in range(1, len(tree)):
        current_morph = tree[i]["text"]
        suffixes.append(build_morpheme(current_morph, "bound",
                        get_etym(f"-{current_morph}")))

    return {
        "prefixes": prefixes,
        "root": root_morph,
        "suffixes": suffixes
    }


# Run server
if __name__ == "__main__":
    app.run(debug=True)
