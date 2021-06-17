from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Role


@app.route('/role', methods=['GET'])
def role():
    name = request.args.get('name')
    if name is not None:
        roles = Role.query.filter(Role.name.ilike("%{}%".format(name))).order_by(Role.name.asc()).all()
    else:
        roles = Role.query.order_by(Role.name.asc()).all()
    return render_template("user/role.html", roles=roles)


@app.route('/role', methods=['POST'])
def add_role():
    name = request.form.get('name')
    role = Role(
        name=name,
    )
    db.session.add(role)
    db.session.commit()
    return redirect(url_for('role'))


@app.route('/delete-role', methods=['POST'])
def delete_role():
    role_id = request.form.get('role_id')
    role = Role.query.filter(Role.id == role_id).first()
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('role'))


@app.route('/change-role', methods=['POST'])
def change_role():
    role_id = request.form.get('role_id')
    Role.query.filter(Role.id == role_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('role'))
