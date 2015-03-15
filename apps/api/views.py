from flask import jsonify

from apps import app
from apps.markov import MarkovWords
m = MarkovWords(3)

@app.route('/api/board')
def index():
    output = m.create_board(36, 5)
    return jsonify(board=output)
