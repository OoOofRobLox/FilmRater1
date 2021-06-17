from flask_login import UserMixin

from app import db, DEFAULT_PROFILE_IMAGE

genre_movie = db.Table('genre_movie',
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
                       )

user_movie = db.Table('user_movie',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
                      )


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    src = db.Column(db.String(1023), unique=False, nullable=False, default=DEFAULT_PROFILE_IMAGE)
    registration_date = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    comments = db.relationship('Commentary', backref='user', lazy=True)
    movies = db.relationship('Movie', secondary=user_movie, lazy=False, backref=db.backref('umovies', lazy=True))
    criteriaMovies = db.relationship('CriteriaMovie', backref='cmusers', lazy=True)

    def is_active(self):
        return self.active


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    users = db.relationship('User', backref='city', lazy=True)


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    generalRating = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    src = db.Column(db.String(1023), unique=False, nullable=False, default=DEFAULT_PROFILE_IMAGE)
    isFavorite = db.Column(db.Boolean, unique=False, nullable=False)

    genres = db.relationship('Genre', secondary=genre_movie, lazy=False, backref=db.backref('genres', lazy=True))
    comments = db.relationship('Commentary', backref='movie', lazy=True)
    users = db.relationship('User', secondary=user_movie, lazy=False, backref=db.backref('users', lazy=True))
    criteriaMovies = db.relationship('CriteriaMovie', backref='cmovies', lazy=True)


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    movies = db.relationship('Movie', secondary=genre_movie, lazy=False, backref=db.backref('gmovies', lazy=True))


class Criteria(db.Model):
    __tablename__ = "criteria"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    criteriaMovies = db.relationship('CriteriaMovie', backref='critrias', lazy=True)


class Commentary(db.Model):
    __tablename__ = "commentary"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), unique=False, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)


class CriteriaMovie(db.Model):
    __tablename__ = "criteriamovie"
    id = db.Column(db.Integer, primary_key=True)
    evaluation = db.Column(db.Integer, unique=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('criteria.id'), nullable=False)


