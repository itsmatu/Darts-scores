from flask import render_template, redirect, request, session
from app import app
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

import users
import scores
import game

@app.route("/")
def index():
	return redirect("/mainpage")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("username"):
            return redirect("/")
        else:
            return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", error="Passwords doesn't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error="User already exists")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("username"):
            return redirect("/")
        else:
            return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error="Incorrect username or password. Please try again.")

@app.route("/logout")
def logout():
	if session.get("username"):
		users.logout()
	return redirect("/")

@app.route("/mainpage", methods = ["POST", "GET"])
def mainpage():
    if request.method == "GET":
        if session.get("username"):
            return scores.get_user_scores()
        else:
            return redirect("/mainpage/allstats")
    if request.method == "POST":
        if scores.check_valid_score():
            scores.add_score()
            return redirect("/")
        else:
            return scores.get_user_scores()

@app.route("/game/<int:id>", methods = ["GET"])
def match(id):
	return game.show_game(id)

@app.route("/newgame", methods = ["GET", "POST"])
def newgame():
	if request.method == "GET":
		return render_template("newgame.html")

	if request.method == "POST":
		if session.get("username"):
			username = session["username"]
			user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
			return redirect("/newgame")

@app.route("/mainpage/allstats", methods = ["GET"])
def allstats():
	return scores.get_all_scores()
