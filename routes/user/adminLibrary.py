from flask import render_template, request, redirect, url_for, flash

from app import app, db
from flask_login import login_required, current_user
from sqlalchemy import func
from model import Movie, Genre, CriteriaMovie, Criteria, User, user_movie
from utils.decorator import has_authority


@app.route('/usermovie', methods=['GET'])
@login_required
@has_authority('Admin')
def show_all():
    movies = Movie.query.order_by(Movie.name.asc()).all()
    users = User.query.order_by(User.nickname.asc()).all()
    return render_template("user/userMovie.html", movies=movies, users=users)


@app.route('/addusermovie', methods=['POST'])
@login_required
@has_authority('Admin')
def add_movie_to_user():
    movie_name = request.form.get('movie_name')
    user_name = request.form.get('user_name')
    try:
        mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
        usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
        usr.movies.append(Movie.query.filter(Movie.id == mov.id).first())
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))


@app.route('/deleteusermovie', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_movie_from_user():
    movie_id = request.form.get('movie_id')
    user_id = request.form.get('user_id')
    try:
        usr = User.query.filter(User.id == user_id).first()
        usr.movies.remove(Movie.query.filter(Movie.id == movie_id).first())
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))
