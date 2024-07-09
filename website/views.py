import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from .database import Boobjuice, IllegalArgumentError

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
	except IllegalArgumentError as e:
		print(e.message)
		flash(e.message, category='danger')
	except Exception as e:
		print('Something went wrong...', e)
		flash('Something went wrong...', category='danger')
	
	return json.dumps('')