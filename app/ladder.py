from flask import render_template
from app import app, get_preview, LINK

import json
import requests
import re

@app.route('/ladder/<int:ladder_id>')
@app.route('/ladder/<int:ladder_id>/')
def ladder(ladder_id):
	ladder = json.loads(requests.post(LINK, json={'method': 'ladders.get', 'ladder': ladder_id}).text)

	if ladder['error']:
		return render_template('message.html', cont=ladder['message'])

	return render_template('ladder.html',
		title = ladder['ladder']['name'],
		description = re.sub(r'\<[^>]*\>', '', ladder['ladder']['description']),
		tags = ladder['ladder']['tags'],
		url = 'ladder/' + str(ladder_id),

		preview = get_preview,

		ladder = ladder['ladder'],
	)