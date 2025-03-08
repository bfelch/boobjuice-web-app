import logging, sys

from boobjuice import create_app

app = create_app()

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
	app.run(debug=True)