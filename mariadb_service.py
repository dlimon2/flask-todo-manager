from main import app, db
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.ext.declarative import declarative_base

#Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        #return '<User %r>' % self.username
        return self

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        #return '<Task %r>' % self.description
        return self
#Métodos
def get_users():
    return User.query.all()

def get_tasks(user_id):
    return Task.query.filter_by(user_id=user_id)