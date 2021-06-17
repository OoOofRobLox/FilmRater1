from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Movie, Genre


@app.route('/unlogged', methods=['GET'])
def unlogMovie():
    movies = Movie.query.order_by(Movie.name.asc()).all()
    genres = Genre.query.all()
    return render_template("user/unlogUnreg.html", movies=movies, genres=genres)
