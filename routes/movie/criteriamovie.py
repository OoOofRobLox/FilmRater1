from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

from app import app, db
from flask_login import login_required, current_user
from model import CriteriaMovie, Movie, Criteria, User, Genre
from utils.decorator import has_authority


@app.route('/criteriaMovie', methods=['GET'])
@login_required
@has_authority('Admin')
def criteriamovie():
    crMov = CriteriaMovie.query.all()
    crit = Criteria.query.all()
    users = User.query.all()
    movies = Movie.query.all()
    return render_template("movie/criteriaMovie.html", crMov=crMov, crit=crit, users=users, movies=movies)


@app.route('/criteriaMovie', methods=['POST'])
@login_required
@has_authority('Admin')
def add_criteriamovie():
    evaluation = request.form.get('evaluation')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    criteria_name = request.form.get('criteria_name')
    try:
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
    except Exception:
        flash('')
        return redirect(url_for('criteriamovie'))
    return redirect(url_for('criteriamovie'))


@app.route('/calc', methods=['POST'])
@login_required
def calculate():
    criteria_name = request.form.get('criteria_name')
    genres = Genre.query.all()
    selected_movies = []
    movies = Movie.query.all()
    try:
        evaluation = float(request.form.get('evaluation'))
        criteria = Criteria.query.filter(Criteria.name == criteria_name).first()
        for movie in movies:
            query = CriteriaMovie.query.filter(CriteriaMovie.criteria_id == criteria.id).filter(
                CriteriaMovie.movie_id == movie.id)
            sum = 0
            for i in query.all():
                print(str(i.evaluation) + " " + str(i.criteria_id))
                sum += i.evaluation
            if evaluation <= sum / query.count():
                selected_movies.append(movie)

        # avg = CriteriaMovie.query.filter()
        # .with_entities(func.avg(CriteriaMovie.evaluation)).all()
        print(selected_movies)
    except Exception:
        flash('')
        return render_template("movie/movieList.html", movies=selected_movies, genres=genres)
    return render_template("movie/movieList.html", movies=selected_movies, genres=genres)


@app.route('/delete-criteriamovie', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_criteriamovie():
    criteriamovie_id = request.form.get('criteriamovie_id')
    try:
        crMov = CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).first()
        db.session.delete(crMov)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('criteriamovie'))
    return redirect(url_for('criteriamovie'))


@app.route('/change-criteriamovie', methods=['POST'])
@login_required
@has_authority('Admin')
def change_criteriamovie():
    criteriamovie_id = request.form.get('criteriamovie_id')
    user_name = request.form.get('user_name')
    movie_name = request.form.get('movie_name')
    criteria_name = request.form.get('criteria_name')
    try:
        usr = User.query.filter(func.lower(User.nickname) == func.lower(user_name)).first()
        mov = Movie.query.filter(func.lower(Movie.name) == func.lower(movie_name)).first()
        crt = Criteria.query.filter(func.lower(Criteria.name) == func.lower(criteria_name)).first()
        CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).update({
            'evaluation': request.form.get('evaluation'),
            'user_id': usr.id,
            'movie_id': mov.id,
            'criteria_id': crt.id,
        })
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('criteriamovie'))
    return redirect(url_for('criteriamovie'))


@app.route('/movie/<movie_id>', methods=['POST'])
@login_required
def add_crmov_by_usr(movie_id):
    evaluation = int(request.form.get('evaluation'))
    if evaluation > 100:
        evaluation = 100
    elif evaluation < 0:
        evaluation = 0
    user = current_user.id
    criteria_name = request.form.get('criteria_name')

    try:
        crt = Criteria.query.filter(func.lower(Criteria.name) == func.lower(criteria_name)).first()

        is_exists = CriteriaMovie.query.filter(CriteriaMovie.criteria_id == crt.id).filter(
            CriteriaMovie.movie_id == movie_id).filter(
            CriteriaMovie.user_id == user).first()

        if is_exists is not None:
            flash('')
            print("feqfqfqef")
        else:
            crMov = CriteriaMovie(
                evaluation=evaluation,
                user_id=user,
                movie_id=movie_id,
                criteria_id=crt.id
            )
            db.session.add(crMov)
            db.session.commit()

        update_general_rating(movie_id)
    except Exception:
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/movie/delete/<movie_id>', methods=['POST'])
@login_required
def delete_user_criteriamovie(movie_id):
    criteriamovie_id = request.form.get('criteriamovie_id')
    print(criteriamovie_id)
    try:
        crMov = CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).first()
        db.session.delete(crMov)
        db.session.commit()
        update_general_rating(movie_id)
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


@app.route('/movie/change/<movie_id>', methods=['POST'])
@login_required
def change_user_criteriamovie(movie_id):
    criteriamovie_id = request.form.get('criteriamovie_id')
    try:
        evaluation = int(request.form.get('evaluation'))

        if evaluation > 100:
            evaluation = 100
        elif evaluation < 0:
            evaluation = 0

        CriteriaMovie.query.filter(CriteriaMovie.id == criteriamovie_id).update({
            'evaluation': evaluation
        })

        db.session.commit()
        update_general_rating(movie_id)
    except Exception:
        flash('')
        return redirect(url_for('show_movie', movie_id=movie_id))
    return redirect(url_for('show_movie', movie_id=movie_id))


def update_general_rating(movie_id):
    query = CriteriaMovie.query.filter(CriteriaMovie.movie_id == movie_id)
    sum = 0
    for i in query.all():
        print(str(i.evaluation) + " " + str(i.criteria_id))
        sum += i.evaluation
    Movie.query.filter(Movie.id == movie_id).update({'generalRating': float(sum) / query.count()})
    db.session.commit()
