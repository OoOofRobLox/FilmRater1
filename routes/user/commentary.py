from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

from app import app, db
from model import Commentary, Movie, User
from utils.decorator import has_authority
from flask_login import login_required


@app.route('/commentary', methods=['GET'])
@login_required
@has_authority('Admin')
def commentary():
    text = request.args.get('text')
    if text is not None:
        comms = Commentary.query.filter(Commentary.text.ilike("%{}%".format(text))).order_by(
            Commentary.text.asc()).all()
    else:
        comms = Commentary.query.order_by(Commentary.text.asc()).all()

    users = User.query.all()
    movies = Movie.query.all()
    return render_template("user/commentary.html", comms=comms, users=users, movies=movies)


@app.route('/commentary', methods=['POST'])
@login_required
@has_authority('Admin')
def add_commentary():
    text = request.form.get('coment_text')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    try:
        usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
        mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
        comment = Commentary(
            text=text,
            user_id=usr.id,
            movie_id=mov.id
        )
        db.session.add(comment)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('commentary'))
    return redirect(url_for('commentary'))


@app.route('/delete-commentary', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_commentary():
    commentary_id = request.form.get('commentary_id')
    try:
        comment = Commentary.query.filter(Commentary.id == commentary_id).first()
        db.session.delete(comment)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('commentary'))
    return redirect(url_for('commentary'))


@app.route('/change-commentary', methods=['POST'])
@login_required
@has_authority('Admin')
def change_commentary():
    commentary_id = request.form.get('commentary_id')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    try:
        usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
        mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
        Commentary.query.filter(Commentary.id == commentary_id).update({
            'text': request.form.get('text'),
            'user_id': usr.id,
            'movie_id': mov.id
        })
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('commentary'))
    return redirect(url_for('commentary'))
