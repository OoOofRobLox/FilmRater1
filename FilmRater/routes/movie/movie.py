from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Movie, Genre


@app.route('/movie', methods=['GET'])
def movie():
    movies = Movie.query.order_by(Movie.name.asc()).all()
    genres = Genre.query.all()
    return render_template("movie/movie.html", movies=movies, genres=genres)


@app.route('/movie', methods=['POST'])
def add_movie():
    name = request.form.get('name')
    description = request.form.get('description')
    generalRating = request.form.get('generalRating')
    length = request.form.get('length')
    src = request.form.get('src')
    genres = []
    for genre in Genre.query.all():
        cb = request.form.get('gcb' + str(genre.id))
        if cb is not None:
            genres.append(genre)

    mov = Movie(
        name=name,
        description=description,
        generalRating=generalRating,
        length=length,
        isFavorite=False,
        src=src
    )

    mov.genres = genres
    db.session.add(mov)
    db.session.commit()
    return redirect(url_for('movie'))


@app.route('/delete-movie', methods=['POST'])
def delete_movie():
    movie_id = request.form.get('movie_id')
    try:
        mov = Movie.query.filter(Movie.id == movie_id).first()
        db.session.delete(mov)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('movie'))
    return redirect(url_for('movie'))
