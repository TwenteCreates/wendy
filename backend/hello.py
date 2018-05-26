from flask import Flask
from flask_cors import CORS


import os

app = Flask(__name__)
cors = CORS(app)


def get_environmental_variable(key=None):
    if not key:
        raise
    return os.getenv(key, default=None)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye")
def bye():
    return "bye World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12000)
