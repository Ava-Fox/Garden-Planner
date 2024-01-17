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
button = None

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
                db.execute("INSERT INTO history VALUES ((SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?), (SELECT id FROM plants WHERE name = ?), ?);", where[0], where[1], where[2], plant, date)

        # If so, add them to their garden table

        return render_template("add.html", plants=plants)
    
    else:
        return render_template("add.html")

@app.route("/avas_garden")
@login_required
def avas_garden():
    # Wonder if can make more dynamic...
    plots = db.execute("SELECT * FROM plot ORDER BY bed, local_y, local_x;")
    print(plots)
    columns = {}
    rows = {}
    # beds = {
    #     1: {
    #        columns: {1: []},
    #         rows: {1: []},
    #    },
    # }
    for plot in plots:
        bed = plot['bed']

        column = plot['local_x']
        row = plot['local_y']
        if column in columns.keys():
            columns[column].append(plot['id'])
        else:
            columns[column] = [plot['id']]
        if row in rows.keys():
            rows[row].append(plot['id'])
        else:
            rows[row] = [plot['id']]
        
    return render_template("avas_garden.html", columns=columns, rows=rows)

@app.route("/history")
@login_required
def history():
    return render_template("history.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # When click button, redirect to a button-history page
    # Check to see if any history for that plot, and show on screen
    if request.method == "POST":
        button = request.form.get("clicked-button")
        button = button.split()
        history = db.execute("SELECT * FROM history WHERE plot_id = (SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?);", button[0], button[1], button[2])
        print(history)
        print(button)
        return render_template("plothistory.html", button=button, history=history)
    else:
        return render_template("index.html")

@app.route("/plothistory", methods=["GET", "POST"])
def plothistory():
    return render_template("plothistory.html")


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
    
