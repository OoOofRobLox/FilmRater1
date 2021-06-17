from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Genre
from flask_login import login_required, current_user
from utils.decorator import has_authority


@app.route('/genre', methods=['GET'])
@login_required
@has_authority('Admin')
def genre():
    name = request.args.get('name')
    if name is not None:
        genres = Genre.query.filter(Genre.name.ilike("%{}%".format(name))).order_by(Genre.name.asc()).all()
    else:
        genres = Genre.query.order_by(Genre.name.asc()).all()
    return render_template("movie/genre.html", genres=genres)


@app.route('/genre', methods=['POST'])
@login_required
@has_authority('Admin')
def add_genre():
    name = request.form.get('name')
    try:
        gnr = Genre(
            name=name
        )
        db.session.add(gnr)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('genre'))
    return redirect(url_for('genre'))


@app.route('/delete-genre', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_genre():
    genre_id = request.form.get('genre_id')
    try:
        gnr = Genre.query.filter(Genre.id == genre_id).first()
        gnr.movies.clear()
        db.session.commit()
        db.session.delete(gnr)
        db.session.commit()
    except Exception:
        flash('жанр')
        return redirect(url_for('genre'))
    return redirect(url_for('genre'))


@app.route('/change-genre', methods=['POST'])
@login_required
@has_authority('Admin')
def change_genre():
    genre_id = request.form.get('genre_id')
    try:
        Genre.query.filter(Genre.id == genre_id).update({'name': request.form.get('name')})
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('genre'))
    return redirect(url_for('genre'))
