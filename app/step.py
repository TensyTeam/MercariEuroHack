from flask import render_template, Markup
from app import app, LINK

import json
import requests
import re
import markdown

@app.route('/ladder/<int:ladder_id>/question/<int:step_id>')
@app.route('/ladder/<int:ladder_id>/question/<int:step_id>/')
def step(ladder_id, step_id):
	step = json.loads(requests.post(LINK, json={'method': 'step.get', 'ladder': ladder_id, 'step': step_id}).text)

	if step['error']:
		return render_template('message.html', cont=step['message'])

	step['step']['cont'] = Markup(step['step']['cont'])
	step['step']['theory'] = Markup(step['step']['theory'])
	for i in range(len(step['step']['options'])):
			step['step']['options'][i] = Markup(markdown.markdown(step['step']['options'][i]))

	return render_template('step.html',
		title = step['step']['name'],
		description = re.sub(r'\<[^>]*\>', '', step['step']['cont']) + '\n' + '; '.join([re.sub(r'\<[^>]*\>', '', i) for i in step['step']['options']]),
		tags = step['tags'],
		url = 'ladder/' + str(ladder_id) + '/question/' + str(step_id),

		enumerate = enumerate,

		ladder_id = ladder_id,
		step = step['step'],
	)