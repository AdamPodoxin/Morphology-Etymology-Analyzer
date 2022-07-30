from flask import Flask, request, jsonify
from morphemes import Morphemes
from morph import get_morphs

m = Morphemes("./morphemes")

# Init app
app = Flask(__name__)


@app.route("/morphemes", methods=["GET"])
def morphemes():
    word = request.args["word"]
    return jsonify(get_morphs(word))


# Run server
if __name__ == "__main__":
    app.run(debug=True)
