from app import app
from db import db
from flask import render_template, redirect, request, session


def show_game(game_id):
    id = game_id
    avg_sql = db.session.execute("SELECT * FROM averages WHERE game_id=:id", {"id": id})
    game_sql = db.session.execute("SELECT * FROM games WHERE id=:id", {"id": id})
    avg = avg_sql.fetchone()
    player = db.session.execute("SELECT username FROM users WHERE id=:user_id", {"user_id": avg.user_id})
    player_one = player.fetchone()
    game = game_sql.fetchone()
    return render_template("game.html", game=game, avg=avg, player1=player_one)