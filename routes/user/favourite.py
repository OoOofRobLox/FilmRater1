from flask import render_template, request, redirect, url_for, flash
import traceback

from app import app, db
from model import User, Movie, Genre, Criteria
from flask_login import login_required, current_user


@app.route('/favourites', methods=['GET'])
@login_required
def fav():
    user_id = current_user.id
    user = User.query.filter(User.id == user_id).first()
    genres = Genre.query.all()
    criterias = Criteria.query.all()
    return render_template("user/favourite.html", user=user, genres=genres, criterias=criterias)


@app.route('/movie/addfavoritemovie/<movie_id>', methods=['POST'])
def add_favorite_movie(movie_id):
    try:
        user = current_user
        user.favorites.append(Movie.query.filter(Movie.id == movie_id).first())
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/delete-from-favorite', methods=['POST'])
def delete_from_favorite():
    try:
        movie_id = request.form.get('movie_id')
        user = current_user
        user.favorites.remove(Movie.query.filter(Movie.id == movie_id).first())
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('fav'))
    return redirect(url_for('fav'))
