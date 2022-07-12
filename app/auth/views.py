from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from app.forms import LoginForm, SignupForm
from . import auth
from app.models import User
from app import login_manager
from app.extensions import db

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    login_form = LoginForm()
    #El context se envia como parámetro al template
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = User.query.filter_by(username=login_form.username.data).first()
        if username and username.check_password(password=login_form.password.data):
            flash('success :DDDDDD')
            login_user(username)
            return redirect(url_for('hello'))
        else:
            flash('Datos incorrectos')
            return redirect(url_for('auth.login'))
    else:
        flash('Usuario no existe')
    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Bye')
    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        existing_user = User.query.filter_by(username=signup_form.username.data).first()
        if existing_user is None:
            user = User(username = signup_form.username.data)
            user.set_password(signup_form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario existente')


    return render_template('signup.html', **context)
