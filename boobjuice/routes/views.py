from flask import Blueprint, flash, render_template, request

import json
import logging

from boobjuice.persistence import PumpedMilk, PumpProfile, DataAccessError, IllegalArgumentError

views = Blueprint('views', __name__)

profile = PumpProfile()
pumpedMilk = PumpedMilk()

@views.route('/')
def summary():
	return render_template('summary.html', entries=json.dumps(pumpedMilk.get()))

@views.route('/manage')
def manage():
	return render_template('manage.html', entries=json.dumps(pumpedMilk.get()))

@views.route('/record/pumped-milk', methods=['PUT', 'POST', 'DELETE'])
def record_pumped_milk():
	try:
		data = request.get_json(silent=True)

		match request.method:
			case 'PUT':
				pumpedMilk.insert(data)
			case 'POST':
				pumpedMilk.update(data)
			case 'DELETE':
				pumpedMilk.delete(data)
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

@views.route('/record/profile', methods=['PUT', 'POST', 'DELETE'])
def record_profile():
	try:
		data = request.get_json(silent=True)

		match request.method:
			case 'PUT':
				profile.insert(data)
			case 'POST':
				profile.update(data)
			case 'DELETE':
				profile.delete(data)
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