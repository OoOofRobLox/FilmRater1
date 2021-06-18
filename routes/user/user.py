import datetime

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import app, db
from model import User, Role, City
from utils.decorator import has_authority
from flask_login import login_required


@app.route('/user', methods=['GET'])
#@login_required
#@has_authority('Admin')
def user():
    name = request.args.get('name')
    if name is not None:
        users = User.query.filter(User.nickname.ilike("%{}%".format(name))).order_by(User.nickname.asc()).all()
    else:
        users = User.query.order_by(User.nickname.asc()).all()
    roles = Role.query.all()
    cities = City.query.all()
    return render_template("user/user.html", users=users, roles=roles, cities=cities)


@app.route('/user', methods=['POST'])
#@login_required
#@has_authority('Admin')
def add_user():
    email = request.form.get('email')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    src = request.form.get('src')
    city_name = request.form.get('city_name')
    role_name = request.form.get('role_name')
    try:
        cty = City.query.filter(func.lower(City.name) == func.lower(city_name)).first()
        rle = Role.query.filter(func.lower(Role.name) == func.lower(role_name)).first()

        hash_password = generate_password_hash(password)

        usr = User(
            email=email,
            password=hash_password,
            nickname=nickname,
            src=src,
            city_id=cty.id,
            registration_date=datetime.datetime.now(),
            role_id=rle.id,
            active=True
        )
        db.session.add(usr)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('user'))
    return redirect(url_for('user'))


@app.route('/delete-user', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_user():
    user_id = request.form.get('user_id')
    try:
        usr = User.query.filter(User.id == user_id).first()
        db.session.delete(usr)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть.')
        return redirect(url_for('user'))
    return redirect(url_for('user'))


@app.route('/change-user', methods=['POST'])
@login_required
@has_authority('Admin')
def change_user():
    user_id = request.form.get('user_id')
    city_name = request.form.get('city_name')
    role_name = request.form.get('role_name')
    try:
        cty = City.query.filter(func.lower(City.name) == func.lower(city_name)).first()
        rle = Role.query.filter(func.lower(Role.name) == func.lower(role_name)).first()
        User.query.filter(User.id == user_id).update({
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'nickname': request.form.get('nickname'),
            'src': request.form.get('src'),
            'city_id': cty.id,
            'role_id': rle.id,

        })
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('user'))
    return redirect(url_for('user'))
