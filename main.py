import unittest
from flask import make_response, request, redirect, render_template, session, flash, url_for
from flask_login import login_required, current_user
import unittest
from app import create_app
from app.forms import TaskForm, DeleteTask, UpdateTask
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
    task_form = TaskForm()
    delete_form = DeleteTask()
    update_form = UpdateTask()
    tasks = get_tasks(current_user.id)
    context = {
        'user_ip': user_ip,
        'tasks': tasks,
        'username': username,
        'task_form': task_form,
        'delete_form': delete_form,
        'update_form': update_form
    }

    if task_form.validate_on_submit():
        task = Task(description=task_form.description.data, user_id=current_user.id, done=False)
        db.session.add(task)
        db.session.commit()
        flash('Task añadido con éxito!')
        return redirect('/hello')

    return render_template('hello.html', **context)

@app.route('/tasks/delete/<task_id>', methods=['POST'])
def delete(task_id):
    task_ref = Task.query.filter_by(id=task_id).first()
    db.session.delete(task_ref)
    db.session.commit()
    flash('Task eliminado con éxito')
    return redirect('/hello')

@app.route('/task/update/<task_id>/<int:done>', methods=['POST'])
def update(task_id, done):
    print(done)
    task_ref = Task.query.filter_by(id=task_id).first()
    if task_ref.done == True:
        task_ref.done = False
    else:
        task_ref.done = True
    db.session.add(task_ref)
    db.session.commit()
    flash('Acutalizado!')
    return  redirect(url_for('hello'))

