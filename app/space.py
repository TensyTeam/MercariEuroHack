from flask import render_template, request
from app import app, LINK

@app.route('/space')
@app.route('/space/')
def study():
	return render_template('study.html',
		title = 'Space',
		description = '',
		tags = ['space', 'learn', 'teach'],
		url = 'space',

		LINK = LINK,

		teacher = request.args.get('teacher'),
	)