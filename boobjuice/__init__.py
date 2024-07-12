from flask import Flask

def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'q9+E1aA?#6}H3PSWQ7£5*8=(V8CtBieM'

	from boobjuice.routes import views

	app.register_blueprint(views, url_prefix='/')

	return app