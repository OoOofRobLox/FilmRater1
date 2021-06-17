from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Genre


@app.route('/genre', methods=['GET'])
def genre():
    name = request.args.get('name')
    if name is not None:
        genres = Genre.query.filter(Genre.name.ilike("%{}%".format(name))).order_by(Genre.name.asc()).all()
    else:
        genres = Genre.query.order_by(Genre.name.asc()).all()
    return render_template("movie/genre.html", genres=genres)


@app.route('/genre', methods=['POST'])
def add_genre():
    name = request.form.get('name')
    gnr = Genre(
        name=name
    )
    db.session.add(gnr)
    db.session.commit()
    return redirect(url_for('genre'))


@app.route('/delete-genre', methods=['POST'])
def delete_genre():
    genre_id = request.form.get('genre_id')
    try:
        gnr = Genre.query.filter(genre.id == genre_id).first()
        db.session.delete(gnr)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть город.')
        return redirect(url_for('genre'))
    return redirect(url_for('genre'))


@app.route('/change-genre', methods=['POST'])
def change_genre():
    genre_id = request.form.get('genre_id')
    Genre.query.filter(Genre.id == genre_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('genre'))
