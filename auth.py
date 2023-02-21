from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .__init__ import *
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password", category='error')
        else:
            flash("the provided email does not match any current user, create account or try different email.", category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # checking if info is valid
        user = User.query.filter_by(email=email).first()
        if user:
            flash("There is already an account associated with this email, please login or try different email", category='error')
        elif (len(email) < 4):
            flash("Email must be at least 4 characters long", category="error")
        elif (len(firstName) < 2):
            flash("first name must be at least 1 character", category="error")
        elif (password1 != password2):
            flash("passwords do not match", category="error")
        elif (len(password1) < 7):
            flash("password must be at least 7 characters", category="error")
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Thank you for creating an account!", category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
