from flask import Blueprint, render_template

test = Blueprint('test', __name__)

@test.route('/testing')
def testing():
	return render_template('testing.html', text='Testing', array=['A', 'B', 'C', 'E'])