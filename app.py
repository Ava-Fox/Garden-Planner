import os
from flask import Flask, render_template
from cs50 import SQL
from flask_session import Session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    # Should I make them log in? 
    return render_template("index.html")