import random

from flask import jsonify

from apps import app
from apps.realwords import all_real_words

from apps.markov import MarkovWords
m = MarkovWords(3)

@app.route('/api/board/<int:words>')
def index(words):
    output = m.create_board(words, random.randint(3,10))
    return jsonify(board=output)

@app.route('/api/realwords')
def realwords():
    return jsonify(words=list(all_real_words))
