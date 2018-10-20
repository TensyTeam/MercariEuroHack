from flask import render_template
from app import app

@app.route('/test')
@app.route('/test/')
def index():
	return render_template('index.html',
		title = 'Test',
		description = '',
		tags = ['test', 'tensegrity', 'tensy'],
		url = 'test',
	)