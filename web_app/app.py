""" Flask app to diplay user data """


import requests
from flask import Flask


db = 'https://ec463-miniproject-824d0-default-rtdb.firebaseio.com/'
app = Flask(__name__)


@app.route("/")
def index():
    r = requests.get(db+'.json')
    return r.json()
