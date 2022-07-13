from flask_login import UserMixin
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

#Modelos
        
class User(UserMixin, db.Model):
    #__tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        #Crear password hasheada
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        #Check hashed passwd
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False, )

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