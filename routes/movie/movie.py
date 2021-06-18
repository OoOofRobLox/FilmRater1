from flask import render_template, request, redirect, url_for, flash
import traceback

from app import app, db
from flask_login import login_required, current_user
from sqlalchemy import func
from model import Movie, Genre, CriteriaMovie, Criteria, User, Commentary
from utils.decorator import has_authority


@app.route('/movie', methods=['GET'])
@login_required
@has_authority('Admin')
def movie():
    movies = Movie.query.order_by(Movie.name.asc()).all()
    genres = Genre.query.all()
    return render_template("movie/movie.html", movies=movies, genres=genres)


@app.route('/movie', methods=['POST'])
@login_required
@has_authority('Admin')
def add_movie():
    name = request.form.get('name')
    description = request.form.get('description')
    generalRating = request.form.get('generalRating')
    length = request.form.get('length')
    src = request.form.get('src')
    genres = []
    try:
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
    except Exception:
        flash('')
        return redirect(url_for('movie'))
    return redirect(url_for('movie'))


@app.route('/movie/<movie_id>', methods=['GET'])
@login_required
def show_movie(movie_id):
    curr_movie = Movie.query.filter(Movie.id == movie_id).first()
    genres = Genre.query.all()
    crmovs = CriteriaMovie.query.all()
    criterias = Criteria.query.all()
    user = User.query.filter(User.id == current_user.id).first()

    return render_template("movie/oneMovie.html", movie=curr_movie, genres=genres, crmovs=crmovs, criterias=criterias,
                           user=user)


@app.route('/delete-movie', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_movie():
    try:
        movie_id = request.form.get('movie_id')
        mov = Movie.query.filter(Movie.id == movie_id).first()
        mov.genres.clear()
        db.session.commit()
        comms = Commentary.query.filter(Commentary.movie_id == movie_id).all()
        for com in comms:
            db.session.delete(com)
            db.session.commit()
        users = User.query.all()
        for user in users:
            if mov in user.movies:
                user.movies.remove(Movie.query.filter(Movie.id == movie_id).first())
                user.favorites.remove(Movie.query.filter(Movie.id == movie_id).first())
                db.session.commit()
        db.session.delete(mov)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        traceback.print_exc()
        return redirect(url_for('movie'))
    return redirect(url_for('movie'))


@app.route('/find-by-name', methods=['GET'])
@login_required
def find_by_name():
    name_to_find = request.args.get("name")
    genres = Genre.query.all()
    name_search = "%{}%".format(name_to_find)
    rows = Movie.query.filter(Movie.name.ilike(name_search))
    return render_template("movie/movieList.html", movies=rows.all(), genres=genres)


@app.route('/find-by-genre', methods=['POST'])
@login_required
def find_by_genre():
    gens = Genre.query.all()
    mov = Movie.query.all()
    moviesList = []

    genresToFind = []
    for genre in gens:
        cb = request.form.get('gcb' + str(genre.id))
        if cb is not None:
            genresToFind.append(genre)

    for element in mov:
        if all(elem in element.genres for elem in genresToFind):
            moviesList.append(element)
        else:
            print('')

    return render_template("movie/movieList.html", movies=moviesList, genres=gens)


@app.route('/sort-by-general-rating', methods=['POST'])
@login_required
def sort_by_general_rating():
    mov = Movie.query.order_by(Movie.generalRating.desc()).all()
    gens = Genre.query.all()
    return render_template("movie/movieList.html", movies=mov, genres=gens)


@app.route('/find-by-genre-in-library', methods=['POST'])
@login_required
def find_by_genre_in_library():
    user = current_user
    gens = Genre.query.all()
    moviesList = []

    genresToFind = []
    for genre in gens:
        cb = request.form.get('gcb' + str(genre.id))
        if cb is not None:
            genresToFind.append(genre)

    for element in user.movies:
        if all(elem in element.genres for elem in genresToFind):
            moviesList.append(element)
        else:
            print('')

    return render_template("user/movieSortsResult.html", movies=moviesList, genres=gens)


@app.route('/find-by-criteria-in-library', methods=['POST'])
@login_required
def find_by_criteria_in_library():
    criteria_name = request.form.get('criteria_name')
    evaluation = float(request.form.get('evaluation'))
    try:
        user = current_user
        movies = user.movies
        genres = Genre.query.all()
        criteria = Criteria.query.filter(Criteria.name == criteria_name).first()
        selected_movies = []
        for movie in movies:
            query = CriteriaMovie.query.filter(CriteriaMovie.criteria_id == criteria.id).filter(
                CriteriaMovie.movie_id == movie.id)
            sum = 0
            for i in query.all():
                print(str(i.evaluation) + " " + str(i.criteria_id))
                sum += i.evaluation
            if evaluation <= float(sum) / query.count():
                selected_movies.append(movie)

        # avg = CriteriaMovie.query.filter()
        # .with_entities(func.avg(CriteriaMovie.evaluation)).all()
        print(selected_movies)
    except Exception:
        flash('')
        return render_template("user/movieSortsResult.html", movies=selected_movies, genres=genres)
    return render_template("user/movieSortsResult.html", movies=selected_movies, genres=genres)
