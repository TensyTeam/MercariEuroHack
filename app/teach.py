from flask import render_template
from app import app, LINK

@app.route('/teach')
@app.route('/teach/')
def teach():
	return render_template('teach.html',
		title = 'Teach',
		description = '',
		tags = ['study', 'teach'],
		url = 'teach',

		LINK = LINK,
	)