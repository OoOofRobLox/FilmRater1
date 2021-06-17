from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import app, db
from model import User, Role, City
from flask_login import login_required, current_user


@app.route('/userAcc', methods=['GET'])
@login_required
def user_account():
    try:
        user = current_user
        length = 0
        count = 0
        for mov in user.movies:
            length += mov.length
            count += 1
    except Exception:
        flash('')
        return render_template("user/userAccount.html", user=user, length=length, count=count)
    return render_template("user/userAccount.html", user=user, length=length, count=count)
