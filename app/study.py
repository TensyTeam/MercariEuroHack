from flask import render_template
from app import app, LINK

@app.route('/ladder/<int:ladder_id>/study/<int:step_id>')
@app.route('/ladder/<int:ladder_id>/study/<int:step_id>/')
def study(ladder_id, step_id):
	return render_template('study.html',
		title = 'Study',
		description = '',
		tags = ['study', 'learn'],
		url = 'ladder/' + str(ladder_id) + '/study/' + str(step_id),

		LINK = LINK,
	)