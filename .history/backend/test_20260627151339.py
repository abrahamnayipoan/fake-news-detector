from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is working"

app.run(port=5000, debug=False)