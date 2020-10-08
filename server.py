# server.py
# where your python app starts

# pip3 install Flask
from flask import Flask, jsonify, render_template, request

application = Flask(__name__)


# I've started you off with Flask, 
# but feel free to use whatever libs or frameworks you'd like through `.requirements.txt`.

# unlike express, static files are automatic: http://flask.pocoo.org/docs/0.12/quickstart/#static-files

# http://flask.pocoo.org/docs/0.12/quickstart/#routing
# http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
@application.route('/')
def hello():
    return render_template('index.html')
 
# listen for requests : hacer que el servidor esté disponible públicamente con flask run --host=0.0.0.0)
if __name__ == "__main__":
    application.run(host='0.0.0.0')