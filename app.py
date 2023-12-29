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

@app.errorhandler(404)
def page_not_found(error):
    return render_template("notfound.html"), 404

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        user_id = session["user_id"]
        date = request.form.get("date")
        plants = request.form.get("plant")
        plants = plants.split()
        where = request.form.get("location")
        where = where.split()
        data = db.execute("SELECT name FROM plants;")
        
        # Check to see if user response matches with plants logged in database
        for plant in plants:
            if plant in data:
                db.execute("INSERT INTO history VALUES ((SELECT id FROM plot WHERE local_x = ? AND local_y = ?), (SELECT id FROM plants WHERE name = ?), ?);", where[0], where[1], plant, date)

        # If so, add them to their garden table

        return render_template("add.html", plants=plants)
    
    else:
        return render_template("add.html")

@app.route("/avas_garden")
@login_required
def avas_garden():
    bed1 = db.execute("SELECT * FROM plot WHERE bed = 1;")
    bed2 = db.execute("SELECT * FROM plot WHERE bed = 2;")
    bed3 = db.execute("SELECT * FROM plot WHERE bed = 3;")
    bed4 = db.execute("SELECT * FROM plot WHERE bed = 4;")
    bed5 = db.execute("SELECT * FROM plot WHERE bed = 5;")
    bed6 = db.execute("SELECT * FROM plot WHERE bed = 6;")
    return render_template("avas_garden.html", bed1=bed1, bed2=bed2, bed3=bed3, bed4=bed4, bed5=bed5, bed6=bed6)

@app.route("/history")
@login_required
def history():
    return render_template("history.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Check out if user has anything logged in their garden database
    # If have, show them their current garden
    # If not, redirect them to page where can add what have
    return render_template("index.html")

@app.route("/plan", methods=["GET", "POST"])
@login_required
def plan():
    return render_template("plan.html")


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
    
