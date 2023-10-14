import json
from dataclasses import dataclass, is_dataclass, asdict
from etymology import get_etymology
from morphology import get_morphemes, splice_root
from fastapi import FastAPI

@dataclass
class Morpheme:
    morpheme: str
    type: str
    etymology: str


@dataclass
class Analysis:
    prefixes: str
    root_morpheme: str
    suffixes: str


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


def get_prefixes(root_spliced: list[str]):
    prefixes: list[Morpheme] = []
    for i in range(len(root_spliced) - 1):
        current_morpheme = f"{root_spliced[i]}-"
        prefixes.append(Morpheme(current_morpheme, "bound", get_etymology(current_morpheme)))

    return prefixes



def get_suffixes(tree, tree_children):
    suffixes = []
    
    for i in range(1, len(tree_children)):
        current_morpheme = tree_children[i]["text"]
        add_morpheme = current_morpheme

        type = tree_children[i]["type"]
        if type == "root":
            type = "free"
        else:
            add_morpheme = f"-{current_morpheme}"

        suffixes.append(Morpheme(add_morpheme, type, get_etymology(f"-{current_morpheme}")))


    try:
        for i in range(1, len(tree)):
            current_morpheme = tree[i]["text"]
            add_morpheme = current_morpheme
            
            type = tree[i]["type"]
            if type == "root":
                type = "free"
            else:
                add_morpheme = f"-{current_morpheme}"

            suffixes.append(Morpheme(add_morpheme, type, get_etymology(f"-{current_morpheme}")))
    except:
        try:
            for i in range(1, len(tree)):
                current_morpheme = tree[i]["children"][0]["text"]
                add_morpheme = current_morpheme
                
                type = tree[i]["children"][0]["type"]
                if type == "root":
                    type = "free"
                else:
                    add_morpheme = f"-{current_morpheme}"

                suffixes.append(Morpheme(add_morpheme, type, get_etymology(f"-{current_morpheme}")))
        finally:
            print("")


    return suffixes


def analyze(word: str) -> Analysis:
    morphemes = get_morphemes(word)

    tree = morphemes["tree"]

    prefixes: list[Morpheme] = []

    i = 0
    while i < len(tree) and tree[i]["type"] == "prefix":
        current_prefix = f"{tree[i]['text']}-"
        prefixes.append(Morpheme(current_prefix, "prefix", get_etymology(current_prefix)))
        i += 1

    tree_children = tree[i]["children"]

    root = tree_children[0]["text"]
    root_spliced = splice_root(root)

    prefixes.extend(get_prefixes(root_spliced))
    suffixes = get_suffixes(tree, tree_children)

    root_word = root_spliced[len(root_spliced) - 1]
    root_morpheme = Morpheme(root_word, "free", get_etymology(root_word))

    return Analysis(prefixes, root_morpheme, suffixes)

app = FastAPI()


@app.get("/")
async def root():
    return "Please specify a word with /analyze?word=WORD"

@app.get("/analyze")
async def analyze_route(word: str):
    print("Analyzing word", word)
    return {"word": word}
    # analysis = analyze(word)
    # return {
    #     "prefixes": analysis.prefixes,
    #     "root_morpheme": analysis.root_morpheme,
    #     "suffixes": analysis.suffixes
    # }