from flask import render_template
from app import app, get_preview, LINK

import json
import requests

@app.route('/', methods=['GET'])
@app.route('/index')
@app.route('/index/')
@app.route('/learn')
@app.route('/learn/')
def learn():
	ladders = json.loads(requests.post(LINK, json={'method': 'ladders.gets'}).text)

	if ladders['error']:
		return render_template('message.html', cont=ladders['message'])

	return render_template('learn.html',
		title = 'Learn',
		description = '',
		tags = ['learn', 'tensegrity', 'tensy'],
		url = 'learn',

		preview = get_preview,

		ladders = ladders['ladders'],
	)