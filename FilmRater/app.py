from flask import Flask, redirect
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.trim_blocks = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1@localhost:5432/Rater'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hsdkfjhsdjhadjkyuewyhfuehmndkhasjfhuiesdjvhasjdf'
UPLOAD_FOLDER = 'static/image/uploads'
UPLOAD_FOLDER_FOR_SOLUTIONS = 'static/files'
DEFAULT_PROFILE_IMAGE = 'defaultProfile.png'
ALLOWED_PROFILE_IMAGE_EXTENSIONS = {'jpeg', 'jpg', 'gif', 'tiff', 'png', 'bmp', 'svg', 'WebP', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'] = UPLOAD_FOLDER_FOR_SOLUTIONS
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'arturo.koepp2@ethereal.email'
app.config['MAIL_PASSWORD'] = '8sSe3N3yNB9Pe3KWcE'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

from model import *

from routes.location import city
from routes.user import user, role, commentary
from routes.movie import criteria, genre, criteriamovie, movie
from routes.security import registration, login, logout

@app.route('/')
def hello_world():
    return

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
