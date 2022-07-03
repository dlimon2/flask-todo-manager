from flask import Blueprint

#El parámetro url_prefix hace que todas las rutas que comiencen con
# /auth sean dirigidas a este blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Creamos nuevas vistas en app/auth/views.py
from . import views
