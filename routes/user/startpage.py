from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Movie, Genre, Criteria
from utils.decorator import has_authority
from flask_login import login_required


@app.route('/startpage', methods=['GET'])
@login_required
def startpage():
    movies = Movie.query.order_by(Movie.name.asc()).all()
    genres = Genre.query.all()
    criterias = Criteria.query.all()
    return render_template("user/startpage.html", movies=movies, genres=genres, criterias=criterias)
