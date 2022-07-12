from crypt import methods
from ensurepip import bootstrap
import unittest
from flask import make_response, request, redirect, render_template, session, url_for, flash
from flask_login import login_required
import unittest
from app import create_app
from app.forms import LoginForm
from app.models import get_tasks
app = create_app();


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

### RUTAS ###

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))

    session['user_ip'] = user_ip

    return response

#Quitamos el método POST de la ruta hello
#@app.route('/hello', methods=['GET', 'POST'])
@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'tasks': get_tasks(1),
        #'login_form': login_form,
        #se añade username al contexto
        'username': username

    }

    return render_template('hello.html', **context)