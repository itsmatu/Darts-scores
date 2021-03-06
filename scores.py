from app import app
from db import db
from flask import render_template, redirect, request, session


def get_user_scores():
    username = session["username"]		
    user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
    user_id = user.fetchone()[0]
    averages = db.session.execute("SELECT game_id, average_date, average FROM averages WHERE user_id=:user_id ORDER BY id DESC", {"user_id": user_id})		
    topavgs = db.session.execute("SELECT game_id, average_date, average FROM averages WHERE user_id=:user_id ORDER BY average DESC LIMIT 5", {"user_id": user_id})
    total_avg = db.session.execute("SELECT AVG(average)::numeric(4,1) FROM averages WHERE user_id=:user_id AND average_date > NOW() - INTERVAL '30 days'", {"user_id": user_id})
    total = total_avg.fetchone()[0]
    return render_template("mainpage.html", avgs=averages, total=total, topavgs=topavgs)

def get_all_scores():
    averages = db.session.execute("SELECT averages.game_id, averages.average_date, averages.average, users.username FROM averages JOIN users ON averages.user_id = users.id ORDER BY averages.id DESC")
    top_averages = db.session.execute("SELECT averages.game_id, averages.average_date, averages.average, users.username FROM averages JOIN users ON averages.user_id = users.id  ORDER BY averages.average DESC LIMIT 5")
    return render_template("mainpage.html", avgs=averages, topavgs=top_averages)

def add_score():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    average = request.form["addaverage"]
    tons = request.form["addtons"]
    highest = request.form["addhighest"]
    username = session["username"]
    user = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": username})
    user_id = user.fetchone()[0]
    sql_game = "INSERT INTO games (game_date, player_one) VALUES (current_date, :player_one)"
    db.session.execute(sql_game, {"player_one": user_id})
    game = db.session.execute("SELECT id FROM games ORDER BY id DESC")
    game_id = game.fetchone()[0]
    sql = "INSERT INTO averages (game_id, average_date, user_id, average, tons, highest_score) VALUES (:game_id, current_date, :user_id, :average, :tons, :highest_score)"
    db.session.execute(sql, {"game_id": game_id, "user_id": user_id, "average": average, "tons": tons, "highest_score": highest})
    db.session.commit()

def check_valid_score():
    if float(request.form["addaverage"]) > 180 or (float(request.form["addaverage"]) > int(request.form["addhighest"])):
        return False
    if int(request.form["addtons"]) > 5 or (int(request.form["addtons"]) > 0 and int(request.form["addhighest"]) < 100):
        return False
    if int(request.form["addhighest"]) > 180:
        return False
    return True