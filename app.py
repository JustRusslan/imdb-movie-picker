from flask import Flask, render_template, request, redirect
import sqlite3
from random import *
import time

app = Flask(__name__)

con = sqlite3.connect("movies_datalab.db", check_same_thread = False)
cur = con.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/next', methods = ["POST"])
def next():
    global movie_id
    movie_id = randint(0, 250)
    movie_inf = f"SELECT * FROM movies WHERE id = {movie_id} AND watched = 0"
    movie = cur.execute(movie_inf).fetchall()
    return render_template("index.html", movie = movie)

@app.route('/watched', methods = ["POST"])
def watched():
    my_time = time.ctime()
    cur.execute(f"UPDATE movies SET watched = 1, watched_date = '{my_time}' WHERE id = {movie_id}")
    return render_template("index.html")

@app.route('/nice', methods = ["POST"])
def nice():
    cur.execute(f"UPDATE movies SET watched = 1 WHERE id = {movie_id}")
    nice_movie = cur.execute(f"SELECT * FROM movies WHERE id = {movie_id}").fetchall()
    return render_template("nice.html", nice_movie = nice_movie)


@app.route('/history', methods = ["POST"])
def history():
    watched_movies = cur.execute("SELECT * FROM movies WHERE watched = 1").fetchall()
    return render_template("index.html", watched_movies = watched_movies)