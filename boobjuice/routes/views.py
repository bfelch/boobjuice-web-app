from flask import Blueprint, flash, render_template, request
from boobjuice.persistence import Boobjuice, DataAccessError, IllegalArgumentError

import logging

views = Blueprint('views', __name__)

datastore = Boobjuice()

@views.route('/')
def summary():
	return render_template('summary.html', entries=datastore.get())

@views.route('/manage')
def manage():
	return render_template('manage.html', entries=datastore.get())

@views.route('/record', methods=['PUT', 'POST', 'DELETE'])
def record():
	try:
		data = request.get_json(silent=True)

		match request.method:
			case 'PUT':
				datastore.insert(data)
			case 'POST':
				datastore.update(data)
			case 'DELETE':
				datastore.delete(data)
		flash('Success!', category='success')
	except DataAccessError as e:
		message = 'Data access error...'
		logging.error(f'{message} {e.message}')
		flash(message, category='danger')
		return message, 500
	except IllegalArgumentError as e:
		message = 'Illegal argument error...'
		logging.error(f'{message} {e.message}')
		flash(message, category='danger')
		return message, 500
	except Exception as e:
		message = 'Something went wrong...'
		logging.error(f'{message} {e}')
		flash(message, category='danger')
		return message, 500
	
	return '', 200