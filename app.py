from flask import Flask
from os import getenv
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
	return redirect("/mainpage")

@app.route("/register", methods = ["POST", "GET"])
def register():

	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
		hash_value = generate_password_hash(password)
		db.session.execute(sql, {"username": username, "password": hash_value})
		db.session.commit()
		return redirect("/login")

@app.route("/login", methods = ["POST", "GET"])
def login():

	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		session["username"] = username
		sql = "SELECT id, password FROM users WHERE username=:username"
		result = db.session.execute(sql, {"username": username})
		user = result.fetchone()
		if not user:
			return render_template("login.html", error="Incorrect username or password")
		else:
			hash_value = user.password
			if check_password_hash(hash_value, password):
				return redirect("/")
		return render_template("login.html", error="Incorrect username or password")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/mainpage", methods = ["POST", "GET"])
def mainpage():
	if request.method == "GET":
		if session.get("username"):
			username = session["username"]
			user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
			user_id = user.fetchone()[0]
			averages = db.session.execute("SELECT game_id, average_date, average FROM averages WHERE user_id=:user_id ORDER BY id DESC", {"user_id": user_id})
			topavgs = db.session.execute("SELECT game_id, average_date, average FROM averages WHERE user_id=:user_id ORDER BY average DESC LIMIT 5", {"user_id": user_id})
			total_avg = db.session.execute("SELECT AVG(average)::numeric(3,1) FROM averages WHERE user_id=:user_id AND average_date > NOW() - INTERVAL '30 days'", {"user_id": user_id})
			total = total_avg.fetchone()[0]
			return render_template("mainpage.html", avgs=averages, total=total, topavgs=topavgs)
		else:
			return redirect("/mainpage/allstats")
	if request.method == "POST":
		average = request.form["addaverage"]
		username = session["username"]
		user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
		user_id = user.fetchone()[0]
		sql_game = "INSERT INTO games (game_date, player_one) VALUES (current_date, :player_one)"
		db.session.execute(sql_game, {"player_one": user_id})
		game = db.session.execute("SELECT id FROM games ORDER BY id DESC")
		game_id = game.fetchone()[0]
		sql = "INSERT INTO averages (game_id, average_date, user_id, average) VALUES (:game_id, current_date, :user_id, :average)"
		db.session.execute(sql, {"game_id": game_id, "user_id": user_id, "average": average})
		db.session.commit()
		return redirect("/")

@app.route("/game/<int:id>", methods = ["GET"])
def game(id):
	avg_sql = db.session.execute("SELECT * FROM averages WHERE game_id=:id", {"id": id})
	game_sql = db.session.execute("SELECT * FROM games WHERE id=:id", {"id": id})
	avg = avg_sql.fetchone()
	player = db.session.execute("SELECT username FROM users WHERE id=:user_id", {"user_id": avg.user_id})
	player_one = player.fetchone()
	game = game_sql.fetchone()
	return render_template("game.html", game=game, avg=avg, player1=player_one)

@app.route("/newgame", methods = ["GET", "POST"])
def newgame():
	if request.method == "GET":
		return render_template("newgame.html")

	if request.method == "POST":
		if session.get("username"):
			username = session["username"]
			user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
			score = request.form["score"]
			return render_template("newgame.html", score=score)

@app.route("/mainpage/allstats", methods = ["GET"])
def allstats():
		averages = db.session.execute("SELECT averages.game_id, averages.average_date, averages.average, users.username FROM averages JOIN users ON averages.user_id = users.id ORDER BY averages.id DESC")
		top_averages = db.session.execute("SELECT averages.game_id, averages.average_date, averages.average, users.username FROM averages JOIN users ON averages.user_id = users.id  ORDER BY averages.average DESC LIMIT 5")
		return render_template("mainpage.html", avgs=averages, topavgs=top_averages)
