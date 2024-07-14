from boobjuice import create_app
import logging, sys

app = create_app()

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	app.run(debug=True)