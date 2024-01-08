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
    # Wonder if can make more dynamic...
    bed1 = db.execute("SELECT * FROM plot WHERE bed = 1 ORDER BY local_y;")
    bed2 = db.execute("SELECT * FROM plot WHERE bed = 2 ORDER BY local_y;")
    bed3 = db.execute("SELECT * FROM plot WHERE bed = 3 ORDER BY local_y;")
    bed4 = db.execute("SELECT * FROM plot WHERE bed = 4 ORDER BY local_y;")
    bed5 = db.execute("SELECT * FROM plot WHERE bed = 5 ORDER BY local_y;")
    bed6 = db.execute("SELECT * FROM plot WHERE bed = 6 ORDER BY local_y;")
    beds = [bed1, bed2, bed3, bed4, bed5, bed6]
    rows = {1: [],}
    for bed in beds:
        # Seperate plots in each bed into list of rows?
        last_y = bed[0]['local_y']
        current_row = 1
        # Too convoluted?
        # {
        #     1: [{'id': ..., 
        #          'local_x': ...,
        #          'local_y': 1,
        #         },
        #          {},
        #          ],
        #     2: [{...}, {}, ...],
        # }

        for plot in bed:
            if plot['local_y'] != last_y:
                #Create new row
                current_row += 1
                rows[current_row] = []
                rows[current_row].append(plot)
                
                #update last_y
                last_y = plot['local_y']
                print(f"Current row: {current_row}")
            # Add plot into current row
            else:
                rows[current_row].append(plot)
                print(f"Current row: {current_row} bed: {plot['bed']}")
            
                
    print(f"Rows: {rows}")
    return render_template("avas_garden.html", rows=rows)

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
    
