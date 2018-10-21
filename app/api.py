from flask import request
from app import app

from mongodb import *

from json import dumps


def errors(x, filters):
	for i in filters:
		if i[0] in x:
			# Неправильный тип данных
			if type(x[i[0]]) != i[2] or (type(x[i[0]]) == list and any(type(j) != i[3] for j in x[i[0]])):
				mes = 'Invalid data type: %s (required %s' % (i[0], str(i[2]))
				if i[2] == list:
					mes += ' - %s' % str(i[3])
				mes += ')'
				return dumps({'error': 4, 'message': mes})

		# Не все поля заполнены
		elif i[1]:
			return dumps({'error': 3, 'message': 'Not all required fields are filled in: %s' % i[0]})


@app.route('/', methods=['POST'])
def process():
	x = request.json
	# print(x)

	if 'method' not in x:
		return dumps({'error': 2, 'message': 'Wrong method'})

	# Убираем лишние отступы
	for i in x:
		if type(x[i]) == str:
			x[i] = x[i].strip()

	try:
# Список ледеров
		if x['method'] == 'ladders.gets':
			filter_db = {'_id': False, 'id': True, 'name': True}
			ladders = list(db['ladders'].find({}, filter_db))

			return dumps({'error': 0, 'ladders': ladders})

# Получение ледера
		elif x['method'] == 'ladders.get':
			mes = errors(x, (
				('ladder', True, int),
			))
			if mes: return mes

			filter_db = {
				'_id': False,
				'id': True,
				'name': True,
				'steps.id': True,
				'description': True,
				'tags': True,
			}

			ladder = db['ladders'].find_one({'id': x['ladder']}, filter_db)

			# Неправильный ледер
			if not ladder:
				return dumps({'error': 6, 'message': 'Ladder does not exsist'})

			return dumps({'error': 0, 'ladder': ladder})

# Получение степа
		elif x['method'] == 'step.get':
			mes = errors(x, (
				('ladder', True, int),
				('step', True, int),
			))
			if mes: return mes

			filter_db = {
				'_id': False,
				'name': True,
				'tags': True,
				'steps.id': True,
				'steps.cont': True,
				'steps.options': True,
				'steps.theory': True,
				'steps.name': True,
			}
			ladder = db['ladders'].find_one({'id': x['ladder']}, filter_db)

			# Неправильный ледер
			if not ladder:
				return dumps({'error': 6, 'message': 'Ladder does not exsist'})

			try:
				step_all = [j['id'] for j in ladder['steps']]
			except:
				step_all = []

			# Неправильный степ
			if x['step'] not in step_all:
				return dumps({'error': 7, 'message': 'Step does not exsist'})

			step_num = step_all.index(x['step'])

			res = {
				'error': 0,
				'step': ladder['steps'][step_num],
				'num': step_num,
				'name': ladder['name'],
				'tags': ladder['tags'],
			}

			return dumps(res)

# Проверка ответов
		elif x['method'] == 'step.check':
			mes = errors(x, (
				('ladder', True, int),
				('step', True, int),
				('answers', True, list, int),
			))
			if mes: return mes

			filter_db = {'_id': False, 'steps.id': True, 'steps.answers': True}
			ladder = db['ladders'].find_one({'id': x['ladder']}, filter_db)

			# Неправильный ледер
			if not ladder:
				return dumps({'error': 6, 'message': 'Ladder does not exsist'})

			try:
				step_all = [j['id'] for j in ladder['steps']]
			except:
				step_all = []

			# Неправильный степ
			if x['step'] not in step_all:
				return dumps({'error': 7, 'message': 'Step does not exsist'})

			step_num = step_all.index(x['step'])

			suc = set(x['answers']) == set(ladder['steps'][step_num]['answers'])

			if suc:
				# Следующий степ
				step_next = ladder['steps'][step_num+1]['id'] if step_num < len(ladder['steps'])-1 else -1

			return dumps({'error': 0, 'correct': suc, 'step': step_next if suc else x['step']})

		else:
			return dumps({'error': 2, 'message': 'Wrong method'})

	# Серверная ошибка
	except Exception as e:
		print(e)
		return dumps({'error': 1, 'message': 'Server error'})