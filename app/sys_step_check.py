from flask import request, render_template, redirect
from app import app, LINK

import requests
import json

@app.route('/sys_step_check/<int:ladder_id>/<int:step_id>', methods=['POST'])
def sys_step_check(ladder_id, step_id):
	x = request.form

	req = {
		'method': 'step.check',
		'ladder': ladder_id,
		'step': step_id,
		'answers': [int(i) for i in x],
	}

	correct = json.loads(requests.post(LINK, json=req).text)

	if correct['error']:
		return render_template('message.html', cont=correct['message'])

	if correct['correct']:
		return redirect(LINK + 'ladder/' + str(ladder_id) + '/question/' + str(correct['step']))
	else:
		return redirect(LINK + 'ladder/' + str(ladder_id) + '/study/' + str(step_id))