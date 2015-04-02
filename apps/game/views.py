from apps import app

from flask import render_template

@app.route('/')
@app.route('/game')
def game():
    return render_template('game.html')
