from flask import Flask, request, jsonify
from morphemes import Morphemes

m = Morphemes("./")
m.parse("unsuccessful")

# Init app
app = Flask(__name__)


@app.route("/morphemes", methods=["GET"])
def morphemes():
    word = request.args["word"]
    return jsonify(m.parse(word))


# Run server
if __name__ == "__main__":
    app.run(debug=True)
