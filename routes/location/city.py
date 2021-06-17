from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import City
from utils.decorator import has_authority
from flask_login import login_required, current_user


@app.route('/city', methods=['GET'])
@login_required
@has_authority('Admin')
def city():
    name = request.args.get('name')

    if name is not None:
        cities = City.query.filter(City.name.ilike("%{}%".format(name))).order_by(City.name.asc()).all()
    else:
        cities = City.query.order_by(City.name.asc()).all()
    return render_template("location/city.html", cities=cities)


@app.route('/city', methods=['POST'])
@login_required
@has_authority('Admin')
def add_city():
    name = request.form.get('name')
    try:
        cty = City(
            name=name
        )
        db.session.add(cty)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('city'))
    return redirect(url_for('city'))


@app.route('/delete-city', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_city():
    city_id = request.form.get('city_id')
    try:
        cty = City.query.filter(City.id == city_id).first()
        db.session.delete(cty)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть город.')
        return redirect(url_for('city'))
    return redirect(url_for('city'))


@app.route('/change-city', methods=['POST'])
@login_required
@has_authority('Admin')
def change_city():
    city_id = request.form.get('city_id')
    try:
        City.query.filter(City.id == city_id).update({'name': request.form.get('name')})
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('city'))
    return redirect(url_for('city'))
