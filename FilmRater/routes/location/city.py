from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import City


@app.route('/city', methods=['GET'])
def city():
    name = request.args.get('name')

    if name is not None:
        cities = City.query.filter(City.name.ilike("%{}%".format(name))).order_by(City.name.asc()).all()
    else:
        cities = City.query.order_by(City.name.asc()).all()
    return render_template("location/city.html", cities=cities)


@app.route('/city', methods=['POST'])
def add_city():
    name = request.form.get('name')
    cty = City(
        name=name
    )
    db.session.add(cty)
    db.session.commit()
    return redirect(url_for('city'))


@app.route('/delete-city', methods=['POST'])
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
def change_city():
    city_id = request.form.get('city_id')
    City.query.filter(City.id == city_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('city'))
