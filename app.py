from flask import Flask, request, jsonify
from main import analyze

app = Flask(__name__)


@app.route("/")
def index():
    return "Please specify a word with /analyze?word=WORD"


@app.route("/analyze", methods=["GET"])
def analyze_route():
    word = request.args.get("word")
    analysis = analyze(word)

    response = jsonify(analysis)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response