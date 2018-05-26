from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye")
def bye():
    return "bye World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12000)
