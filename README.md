# EC463 Fall 2024 Miniproject - Jilin Zheng, Cole Knutsen

## Hardware Assignment

Please see our [REPORT.md](./REPORT.md) for our responses.

## Software Assignment

We built a simple web app using Flask that incorporates authentication via Google and databases using Google Firebase Realtime Database (for hardware-collected data) and SQLite (for user information). The web app shows users their scores...(WIP)

### Running the Web App

To run the web app in a local test/development environment (the only option available...)

1. Clone the repo
2. `cd` into the [flask-backend](./flask-backend/) directory
3. Run `pip install -r requirements.txt` either directly or through a virtual environment
4. Run `python app.py` (you may need to do this twice if the `sqlite_db` is not yet created, which is used to retrieve user data...)

### User Data Privacy

To view their response time game scores (and their own scores only!), users can login using Google, and the only information asked for is their name and email. Their email (excluding everything after and including `@`) is used as their username, and a Realtime Database request query is generated using that username.

Consequently, this means that in [exercise_game.py](./assignment/exercise_game.py), the user playing the response time game must modify the `user_email` variable to be their email address (without including the `@`). This is definitely not the most user-friendly way to provide such a 'user-separation' functionality, but it gets the job done for this assignment...

### Known Issues

- For some reason, the `urequests`/`requests` module does not always work, leading an `OSError: -2`...but running the [exercise_game](./assignment/exercise_game.py) script again (or several more times) works fine...
  - One cause of this OSError could be your WIFI connection - do double-check your WIFI connection is stable.

## Reference(s)

- [Create a Flask Application With Google Login](https://realpython.com/flask-google-login/)
