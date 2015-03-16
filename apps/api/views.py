import random

from flask import jsonify

from apps import app
from apps.markov import MarkovWords
m = MarkovWords(3)

@app.route('/api/board/<int:words>')
def index(words):
    output = m.create_board(words, random.randint(3,10))
    return jsonify(board=output)
