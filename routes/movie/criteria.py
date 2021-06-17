from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Criteria
from flask_login import login_required, current_user
from utils.decorator import has_authority


@app.route('/criteria', methods=['GET'])
@login_required
@has_authority('Admin')
def criteria():
    # name = request.args.get('name')
    criterias = Criteria.query.order_by(Criteria.name.asc()).all()
    # if name is not None:
    #    cities = City.query.filter(City.name.ilike("%{}%".format(name))).order_by(City.name.asc()).all()
    # else:
    #    cities = City.query.order_by(City.name.asc()).all()
    return render_template("movie/criteria.html", criterias=criterias)


@app.route('/criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def add_criteria():
    criteria_name = request.form.get('criteria_name')
    try:
        newCriteria = Criteria(
            name=criteria_name,
        )
        db.session.add(newCriteria)
        db.session.commit()
    except Exception:
        return redirect(url_for('criteria'))
    return redirect(url_for('criteria'))


@app.route('/delete-criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_criteria():
    criteria_id = request.form.get('criteria_id')
    try:
        criteriaToDelete = Criteria.query.filter(Criteria.id == criteria_id).first()
        criteriaToDelete.criteriaMovies.clear()
        db.session.commit()
        db.session.delete(criteriaToDelete)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('criteria'))
    return redirect(url_for('criteria'))


# @app.route('/criteria/<criteria_id>', methods=['GET'])
# def one_criteria(criteria_id):
#     name = request.args.get('name')
#    criteriaa = Criteria.query.filter(Criteria.id == criteria_id).first()
#    return render_template("movie/oneCriteria.html", criteria=criteriaa)


@app.route('/change-criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def change_criteria():
    criteria_id = request.form.get('criteria_id')
    try:
        Criteria.query.filter(Criteria.id == criteria_id).update(
            {'name': request.form.get('name')})
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('criteria'))
    return redirect(url_for('criteria'))
