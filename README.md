# EC463 Fall 2024 Miniproject - Jilin Zheng, Cole Knutsen

## Hardware Assignment

Please see our [REPORT.md](./REPORT.md) for our responses.

## Software Assignment

We built a simple web app using Flask that incorporates authentication via Google and databases using Google Firebase Realtime Database (for hardware-collected data) and SQLite (for user information). The web app shows users their scores...(WIP)

### Running the Web App

To run the web app in a local test/development environment (the only option available...)

1. Clone the repo
2. `cd` into the [web-app](./web-app/) directory
3. Run `pip install -r requirements.txt` either directly or through a virtual environment
4. Run `python app.py` (you may need to do this twice if the `sqlite_db` is not yet created...)

## References

- [Create a Flask Application With Google Login](https://realpython.com/flask-google-login/)
