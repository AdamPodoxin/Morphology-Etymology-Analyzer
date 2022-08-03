from flask import Flask, request
from main import analyze

app = Flask(__name__)


@app.route("/")
def index():
    return "Please specify a word with /analyze?word=WORD"


@app.route("/analyze", methods=["GET"])
def analyze_route():
    word = request.args.get("word")
    return analyze(word)
