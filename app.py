from flask import Flask, request, jsonify

# Init app
app = Flask(__name__)


@app.route("/morphemes", methods=["GET"])
def morphemes():
    word = request.args["word"]
    return jsonify({"word": word})


# Run server
if __name__ == "__main__":
    app.run(debug=True)
