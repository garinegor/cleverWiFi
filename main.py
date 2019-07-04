import wifi
from flask import Flask, render_template

app = Flask(__name__)

ssids = ["Home", "F808", "Kek"]


@app.route("/")
def hello():

    return render_template("wifi.html", ssids=ssids)