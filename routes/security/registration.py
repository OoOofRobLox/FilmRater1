import datetime
import traceback

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user
from werkzeug.security import generate_password_hash

from app import app, db
from model import User, Role, City
from sqlalchemy import func


@app.route('/registration', methods=['GET'])
def registration():
    cities = City.query.all()
    return render_template("security/registration.html", citites=cities)


@app.route('/registration', methods=['POST'])
def registration_post():
    email = request.form.get('email')
    try:
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        nickname = request.form.get('nickname')

        city_name = request.form.get('city_name')

        cty = City.query.filter(func.lower(City.name) == func.lower(city_name)).first()

        user = User.query.filter(User.email == email).first()

        if user is not None:
            flash("Данный email уже занят!")
            return redirect(url_for('registration'))

        if password1 != password2:
            flash("Пароли не совпадают!")
            return redirect(url_for('registration'))

        hash_password = generate_password_hash(password1)
        new_user = User(
            email=email,
            password=hash_password,
            nickname=nickname,
            role_id=Role.query.filter(Role.name == 'Student').first().id,
            registration_date=datetime.datetime.now(),
            city_id=cty.id,
            active=True
        )
        db.session.add(new_user)
        db.session.commit()
        logout_user()

    except Exception:
        user = User.query.filter(User.email == email).first()
        db.session.delete(user)
        db.session.commit()
        traceback.print_exc()
        flash("Не удалось зарегестрироваться")

    return redirect(url_for('login'))
