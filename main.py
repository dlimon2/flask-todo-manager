from crypt import methods
from ensurepip import bootstrap
import unittest
from flask import make_response, request, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
import unittest
from app import create_app
from app.forms import TaskForm
from app.models import get_tasks, Task
from app.extensions import db
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

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.username
    #se instancia TaskForm    
    task_form = TaskForm()
    context = {
        'user_ip': user_ip,
        'tasks': get_tasks(current_user.id),
        'username': username,
        #task form a contexto
        'task_form': task_form
    }

    if task_form.validate_on_submit():
        task = Task(description=task_form.description.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task añadido con éxito!')
        return redirect('/hello')

    return render_template('hello.html', **context)