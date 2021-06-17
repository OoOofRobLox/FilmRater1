from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import User, Movie, Genre, Criteria
from flask_login import login_required, current_user


@app.route('/library', methods=['GET'])
@login_required
def library():
    user_id = current_user.id
    print(user_id)
    user = User.query.filter(User.id == user_id).first()
    genres = Genre.query.all()
    criterias = Criteria.query.all()
    return render_template("user/library.html", user=user, genres=genres, criterias=criterias)


@app.route('/movie/addmovietolib/<movie_id>', methods=['POST'])
def add_movie_to_library(movie_id):
    try:
        user = current_user
        user.movies.append(Movie.query.filter(Movie.id == movie_id).first())
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/delete-from-library', methods=['POST'])
def delete_movie_from_library():
    try:
        movie_id = request.form.get('movie_id')
        user = current_user
        user.movies.remove(Movie.query.filter(Movie.id == movie_id).first())
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('library'))
    return redirect(url_for('library'))
