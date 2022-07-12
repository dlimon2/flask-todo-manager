from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from app.forms import LoginForm
from . import auth
from app.models import User
from app import login_manager

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = User.query.filter_by(username=login_form.username.data).first()
        password_db = User.query.filter_by(password=login_form.password.data).first()
        #Por el momento se descarta el uso de passwords hasheados, se manejará en plain
        #if username and username.check_password(password=login_form.password.data):
        if username and password_db:
            flash('success :DDDDDD')
            login_user(username)
            return redirect(url_for('hello'))
        else:
            flash('Datos incorrectos')
            return redirect(url_for('auth.login'))
    else:
        flash('Usuario no existe')
    return render_template('login.html', **context)