import os

from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///garden.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", message="*Please provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", message="*Please provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", message="*Invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register use"""
    if request.method == "POST":
        # Confirm user typed in all fields
        if not request.form.get("username"):
            return render_template("register.html", message="*Please provide a username")
        elif not request.form.get("password"):
            return render_template("register.html", message="*Please provide a password")
        elif not request.form.get("confirm"):
            return render_template("register.html", message="*Please confirm password")
        
        # Check if username already exists
        rows = db.execute("SELECT * FROM users where username = ?;", request.form.get("username"))
        if rows:
            return render_template("register.html", message="*Username already exists")
        
        # Check for matching passwords
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("register.html", message="Passwords do not match")
        
        # Enter user data into database w/ hashed password
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, generate_password_hash(password))
        return redirect("/")

    else:
        return render_template("register.html")
    

