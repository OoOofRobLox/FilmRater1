from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Criteria


@app.route('/criteria', methods=['GET'])
def criteria():
    # name = request.args.get('name')
    criterias = Criteria.query.order_by(Criteria.name.asc()).all()
    # if name is not None:
    #    cities = City.query.filter(City.name.ilike("%{}%".format(name))).order_by(City.name.asc()).all()
    # else:
    #    cities = City.query.order_by(City.name.asc()).all()
    return render_template("movie/criteria.html", criterias=criterias)


@app.route('/criteria', methods=['POST'])
def add_criteria():
    criteria_name = request.form.get('criteria_name')
    newCriteria = Criteria(
        name=criteria_name,
    )
    db.session.add(newCriteria)
    db.session.commit()
    return redirect(url_for('criteria'))


@app.route('/delete-criteria', methods=['POST'])
def delete_criteria():
    criteria_id = request.form.get('criteria_id')
    criteriaToDelete = Criteria.query.filter(Criteria.id == criteria_id).first()
    print(criteriaToDelete.evaluation)
    db.session.delete(criteriaToDelete)
    db.session.commit()
    return redirect(url_for('criteria'))


#@app.route('/criteria/<criteria_id>', methods=['GET'])
#def one_criteria(criteria_id):
#     name = request.args.get('name')
#    criteriaa = Criteria.query.filter(Criteria.id == criteria_id).first()
#    return render_template("movie/oneCriteria.html", criteria=criteriaa)


@app.route('/change-criteria', methods=['POST'])
def change_criteria():
    criteria_id = request.form.get('criteria_id')
    Criteria.query.filter(Criteria.id == criteria_id).update(
        {'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('criteria'))
