"""
Flask app to diplay user data

Followed Google Login tutorial from 
https://realpython.com/flask-google-login/
"""


import json
import os
import sqlite3

from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests

from db import init_db_command
from user import User


# CONFIGURE APPROPRIATELY USING ENVIRONMENTAL VARIABLES
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# flask and flask-login (session management) setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24) # used for login manager
db = 'https://ec463-miniproject-824d0-default-rtdb.firebaseio.com/'
login_manager = LoginManager()
login_manager.init_app(app)

# database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # assume already created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    """ helper function to retrieve user from db """
    return User.get(user_id)


def get_google_provider_cfg():
    """ retrieve Google provider configuration """
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/')
def index():
    # r = requests.get(db+'.json')
    # return r.json()
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app.route('/login')
def login():
    # find out URL for Google login
    authorization_endpoint = get_google_provider_cfg()["authorization_endpoint"]

    # construct request for Google login 
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # get required Google auth code
    code = request.args.get("code")

    # find URL to hit to get tokens that allow info on behalf of a user
    token_endpoint = get_google_provider_cfg()["token_endpoint"]

    # send request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    # find URL for user profile information
    userinfo_endpoint = get_google_provider_cfg()["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # save user info if user email is verified
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        user_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # create user with Google information
    user = User(
        id_=unique_id,
        name=user_name,
        email=user_email,
        profile_pic=picture
    )

    # add user to database if not exist
    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email, picture)

    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context="adhoc") # adhoc for encrypted connection with Google
