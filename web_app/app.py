from flask import Flask, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "your_google_client_id"
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "your_google_client_secret"

google_bp = make_google_blueprint(redirect_to="dashboard")
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    user_info = resp.json()
    return f"Hello, {user_info['displayName']}! <br> Welcome to your dashboard."
