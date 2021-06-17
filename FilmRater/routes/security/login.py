from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

from app import app
from model import User


@app.route('/login', methods=['GET'])
def login():
    return render_template("security/login.html")


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    if user is None:
        flash('Данный пользователь не существует!')
        return redirect(url_for('login'))

    if check_password_hash(user.password, password):
        if user.is_active():
            login_user(user)
            print("YEsss")
        else:
            flash('Подтвердите вашу почту.')
            return redirect(url_for('login'))
    else:
        flash('Неверный пароль')
        return redirect(url_for('login'))

    return redirect(url_for('login'))
