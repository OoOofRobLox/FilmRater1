from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

from app import app, db
from flask_login import login_required, current_user
from model import CriteriaMovie, Movie, Criteria, User, Commentary


@app.route('/movie/addcomm/<movie_id>', methods=['POST'])
@login_required
def add_commentary_by_usr(movie_id):
    text = request.form.get('comment_text')
    try:
        user = current_user.id

        comment = Commentary(
            text=text,
            user_id=user,
            movie_id=movie_id,
        )
        db.session.add(comment)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/movie/deletecomm/<movie_id>', methods=['POST'])
@login_required
def delete_commentary_by_usr(movie_id):
    commentary_id = request.form.get('commentary_id')
    try:
        comment = Commentary.query.filter(Commentary.id == commentary_id).first()
        db.session.delete(comment)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/movie/changecomm/<movie_id>', methods=['POST'])
@login_required
def change_commentary_by_usr(movie_id):
    commentary_id = request.form.get('commentary_id')
    try:
        Commentary.query.filter(Commentary.id == commentary_id).update({
            'text': request.form.get('comment_text')  # ,
            # 'criteria_id': crt.id,
        })
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))
