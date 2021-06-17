from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

from app import app, db
from model import CriteriaMovie, Movie, Criteria, User


@app.route('/criteriaMovie', methods=['GET'])
def criteriamovie():
    crMov = CriteriaMovie.query.all()
    crit = Criteria.query.all()
    users = User.query.all()
    movies = Movie.query.all()
    return render_template("movie/criteriaMovie.html", crMov=crMov, crit=crit, users=users, movies=movies)


@app.route('/criteriaMovie', methods=['POST'])
def add_criteriamovie():
    evaluation = request.form.get('evaluation')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    criteria_name = request.form.get('criteria_name')
    usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
    mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
    crt = Criteria.query.filter(func.lower(Criteria.name) == func.lower(criteria_name)).first()
    crMov = CriteriaMovie(
        evaluation=evaluation,
        user_id=usr.id,
        movie_id=mov.id,
        criteria_id=crt.id
    )
    db.session.add(crMov)
    db.session.commit()
    return redirect(url_for('criteriaMovie'))


@app.route('/delete-criteriamovie', methods=['POST'])
def delete_criteriamovie():
    criteriamovie_id = request.form.get('criteriamovie_id')
    try:
        crMov = CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).first()
        db.session.delete(crMov)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('criteriaMovie'))
    return redirect(url_for('criteriaMovie'))


@app.route('/change-criteriamovie', methods=['POST'])
def change_criteriamovie():
    criteriamovie_id = request.form.get('criteriamovie_id')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    criteria_name = request.form.get('criteria_name')
    usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
    mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
    crt = Criteria.query.filter(func.lower(Criteria.name) == func.lower(criteria_name)).first()
    CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).update({
        'text': request.form.get('text'),
        'user_id': usr.id,
        'movie_id': mov.id,
        'criteria_id': crt.id
    })
    db.session.commit()
    return redirect(url_for('criteriaMovie'))
