from flask import Flask

import os
import re


app = Flask(__name__)
app.config.from_object('config')


LINK = 'http://0.0.0.0:80/'

def get_preview(url, num=0):
	url = '/static/load/' + url + '/'
	for i in os.listdir('app' + url):
		if re.search(r'^' + str(num) + '\.', i):
			return url + i
	return url + '0.png'


from app import api

from app import learn
# from app import teach
from app import ladder
from app import step

from app import sys_step_check

from app import index