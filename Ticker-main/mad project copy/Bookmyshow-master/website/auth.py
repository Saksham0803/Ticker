from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from.models import RegisteredUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .views import view
import re


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pas = request.form.get('password')

        user = RegisteredUser.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.pas, pas):
                flash('logged in', category='success')   #'Logged in successfully!'
                login_user(user, remember=True)
                # redirect to home page
                return redirect(url_for('views.home'))

            else:
                flash('Enter correct Password', category='error')    #Incorrect
        else:
            flash('Email does not exist', category='error')    #, Please Register
    return render_template('login.html', user=current_user)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        pas1 = request.form.get('password1')
        pas2 = request.form.get('password2')
        type_user = request.form.get('user_type')

        # print(request.form.get('theatre_admin'))

        if pas1 != pas2:
            flash("Passwords don\'t match", category='error')   #not matching
        elif len(name) < 3:
            flash('Name must contain greater than 4 Characters', category='error')
        else:
            user = RegisteredUser.query.filter_by(email=email).first()
            
            if user:
                flash('Account already exists', category='warning')    #, Please Login
            else:
                if bool(re.search('^[\w.+\-]+@admin$', email)):
                    # if type_user == "theatre_admin":
                    #     flash('You cannot use bookmyshow domain for other purposes', category='warning')
                    #     return render_template('sign_up.html', user = current_user)
                    # else:
                    new_user = RegisteredUser(email=email, name=name, pas = generate_password_hash(pas1, method='sha256'), is_admin=True)    # is_theatre_admin=False,
                # elif type_user == "theatre_admin":
                #     new_user = RegisteredUser(email=email, name=name, pas=generate_password_hash(pas1, method='sha256'), is_theatre_admin=True, is_super_admin=False)
                else:
                    new_user = RegisteredUser(email=email, name=name, pas=generate_password_hash(pas1, method='sha256'), is_admin=False)   #is_theatre_admin=False,
                print(new_user)
                db.session.add(new_user)
                db.session.commit()
                # login_user(user, remember=True)
                flash('Account created!', category='success')
                
                # redirect to home page
                return redirect(url_for('views.home'))

    return render_template('sign_up.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))