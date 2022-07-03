from crypt import methods
from ensurepip import bootstrap
import unittest
from flask import make_response, request, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.forms import LoginForm


app = create_app();

sections = ['Python', 'Economía', 'Gamedev']

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

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    #se obtiene username de la sesión
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'sections': sections,
        'login_form': login_form,
        #se añade username al contexto
        'username': username

    }

    # procesar datos de forma y almacenar 'username' en sesión
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        #Flash para avisar username registrado
        flash('Usuario registrado con éxito')
        return redirect(url_for('index'))

    return render_template('hello.html', **context)