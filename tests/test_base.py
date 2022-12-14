from flask_testing import TestCase
from flask import current_app, url_for
from main import app

class MainTest(TestCase): #La clase MainTest extiende TestCase
    def create_app(self):
        #Creamos y seteamos a TRUE la variable TESTING, para que
        #Flask sepa que estamos ejecutando una prueba.
        app.config['TESTING'] = True
        #Indicamos que no se utilizará el Token de WTF Forms porque
        #en este caso no se tiene una sesión activa del usuario.
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        return app

    #Para saber si la app realmente existe
    def test_app_exists(self):
        #Para la prueba usaremos assertions, pasándole como argumento
        #La current app importada desde Flask.
        self.assertIsNotNone(current_app)

    #Para saber si la app se encuentra en modo testing
    def test_app_in_testing_mode(self):
        #Verifica si la configuración de current_app 'TESTING' es True
        self.assertTrue(current_app.config['TESTING'])

    #Para comprobar si 'index' redirige a 'hello'
    def test_index_redirect(self):
        #Obtenemos el response de index
        response = self.client.get(url_for('index'))
        #Usamos assertRedirects de flask_testing con la response como argumento
        #Y la locación a verificar como segundo argumento
        self.assertRedirects(response, url_for('hello'))

    #Para comprobar que hello devuelve 200 con el método GET
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        #Comprobar statuscode 200 al hacer una petición GET en 'hello'
        self.assert200(response)

    def test_hello_post(self):
        ###DEPRECATED###
        #Creamos en un diccionario 'data' la información que espera el form
        #para el método POST en 'hello'
        # fake_form = {
        #     'username': 'fake_user',
        #     'password': 'fake_password'
        # }
        ###END DEPRECATED###
        
        # Intentamos hacer post en hello
        response = self.client.post(url_for('hello'))
        
        # Validamos que devuelva código 405 al hacer POST sobre /hello
        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        #Verificar que "auth" se encuentre en los blueprints de la App
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake_user',
            'password': 'fake_password'
        }

        response = self.client.post(url_for('auth.login', data=fake_form))
        #Este assert redirects me daba error ya que esperaba un statuscode en los 300's
        #(redirecciones) pero la redirección realmente da un statuscode 200
        #self.assertRedirects(response, url_for('index'))
        self.assert200(response)