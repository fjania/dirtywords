from apps import app

from flask import render_template

@app.route('/')
@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

@app.route('/promo')
def promo():
    return render_template('promo.html')
