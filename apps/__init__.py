# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from apps.api import views
from apps.game import views
