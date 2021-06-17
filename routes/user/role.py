from flask import render_template, request, redirect, url_for, flash

from app import app, db
from model import Role
from utils.decorator import has_authority
from flask_login import login_required


@app.route('/role', methods=['GET'])
@login_required
@has_authority('Admin')
def role():
    name = request.args.get('name')
    if name is not None:
        roles = Role.query.filter(Role.name.ilike("%{}%".format(name))).order_by(Role.name.asc()).all()
    else:
        roles = Role.query.order_by(Role.name.asc()).all()
    return render_template("user/role.html", roles=roles)


@app.route('/role', methods=['POST'])
@login_required
@has_authority('Admin')
def add_role():
    name = request.form.get('name')
    try:
        role = Role(
            name=name,
        )
        db.session.add(role)
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('role'))
    return redirect(url_for('role'))


@app.route('/delete-role', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_role():
    role_id = request.form.get('role_id')
    try:
        role = Role.query.filter(Role.id == role_id).first()
        db.session.delete(role)
        db.session.commit()
    except Exception:
        return redirect(url_for('role'))
    return redirect(url_for('role'))


@app.route('/change-role', methods=['POST'])
@login_required
@has_authority('Admin')
def change_role():
    role_id = request.form.get('role_id')
    try:
        Role.query.filter(Role.id == role_id).update({'name': request.form.get('name')})
        db.session.commit()
    except Exception:
        flash('')
        return redirect(url_for('role'))
    return redirect(url_for('role'))
