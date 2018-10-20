from flask import render_template
from app import app

@app.route('/', methods=['GET'])
@app.route('/index')
@app.route('/index/')
def index():
	return render_template('index.html',
		title = 'Main',
		description = '',
		tags = ['main page', 'tensegrity', 'tensy'],
		url = 'index',
	)