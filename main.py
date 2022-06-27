from crypt import methods
from ensurepip import bootstrap
import unittest
from flask import Flask, make_response, request, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'StringSuperSeguro'

sections = ['Python', 'Economía', 'Gamedev']

class LoginForm(FlaskForm):
    #Las variables reciben un parámetro validator de DataRequired
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

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