import os

from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session, url_for
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
        plant = request.form.get("plant")
        bed = request.form.get("bed")
        x = request.form.get("x")
        y = request.form.get("y")
        seed_source = request.form.get("seed_source")
        notes = request.form.get("notes")

        plant_id = db.execute("SELECT id FROM plants WHERE name = ?;", plant)
        plot_id = db.execute("SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?", bed, x, y)
        
        if not plot_id:
            return render_template("add.html", message="Invalid plot")

        if plant_id:
            plant_id = plant_id[0]['id']
            db.execute("INSERT INTO history (plot_id, plant_id, date, seed_source, notes) VALUES ((SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?), ?, ?, ?, ?);", bed, x, y, plant_id, date, seed_source, notes)
        else:
            db.execute("INSERT INTO plants (name) VALUES (?);", plant.lower())
            db.execute("INSERT INTO history(plot_id, plant_id, date, seed_source, notes) VALUES ((SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?), (SELECT id FROM plants WHERE name = ?), ?, ?, ?);", bed, x, y, plant, date, seed_source, notes)
        
        # Check to see if user response matches with plants logged in database
        
        # If so, add them to their garden table

        return render_template("add.html")
    
    else:
        return render_template("add.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # When click button, redirect to a button-history page
    # Check to see if any history for that plot, and show on screen
    if request.method == "POST":
        button = request.form.get("clicked-button")
        button = button.split()
        session['button'] = button
        return redirect(url_for('plothistory', button=button))
    else:
        return render_template("index.html")

@app.route("/plothistory", methods=["GET", "POST"])
def plothistory():
    button = session.get('button')
    history = db.execute("SELECT history.id, date, name, url,  seed_source,  notes FROM history JOIN plants ON history.plant_id = plants.id WHERE plot_id = (SELECT id FROM plot WHERE bed = ? AND local_x = ? AND local_y = ?) ORDER BY DATE DESC;", button[0], button[1], button[2])
    print(history)
    if request.method == "POST":
        notes = request.form.get("notes")
        notes_id = request.form.get("notes_id")
        current_notes = db.execute("SELECT notes FROM history WHERE id = ?", notes_id)
        current_notes = current_notes[0]['notes']
        notes = f"{notes} | {current_notes}"
        db.execute("UPDATE history SET notes = ? WHERE id = ?;", notes, notes_id)
        return redirect(url_for('plothistory', button=button, history=history))
    return render_template("plothistory.html", button=button, history=history)

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
    
if __name__ == "__main__":
    app.run(debug=True)