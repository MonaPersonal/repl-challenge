import os
from flask import (Flask, request, render_template, redirect, session,
                   make_response, jsonify, Response, json)
from urlparse import urlparse
from datetime import datetime, time, timedelta
import pyotp
import time
import random


app = Flask(__name__)
app.config.from_object('config.Development')


def run_user_code(code, parameters):
	#import pdb; pdb.set_trace()
	error = ""
	result = ""
	try:
		exec code
	except SyntaxError as e:
		error = error + "exception: " + str(e) + " "
	try:
		exec("result = run("+parameters+")")
	except TypeError as e:
		error = error + "exception: " + e.message + " "
	except NameError as e:
		error = error + "exception:" + e.message + " "
	return result, error

def deploy_user_code(code):
	url = app.config['APP_HOST'] + ":" + str(app.config['APP_PORT']) + "/"
	rand_num = str(long(time.time()))
	path = app.config['DEP_PATH'] + rand_num + ".txt"
	dep_file = open(path, "w+")
	dep_file.write(code)
	dep_file.close()
	url += "deployed/" + rand_num
	return url

@app.route('/', methods=['GET', 'POST'])
def editor():
	return render_template('editor.html')

@app.route('/deployed/<name>', methods=['GET', 'POST'])
def run_deployed(name):
	path = app.config['DEP_PATH'] + name + ".txt"
	dep_file = open(path, "r")
	code = dep_file.read()
	if request.method == 'POST':
		data = json.loads(request.form['json_str'])
		result, error = run_user_code(code, data['parameters'])
		data = {'result': result, 'code_text': code, 'error': error}
	else:
		data = {'code_text': code}
	resp_data = json.dumps(data)
	resp = Response(response=resp_data, status=200, mimetype="application/json")
	return resp

@app.route('/run', methods=['GET', 'POST'])
def run_code():
	data = json.loads(request.form['json_str'])
	result, error = run_user_code(data['code'], data['parameters'])

	data = {'result': str(result) + str(error),}
	resp_data = json.dumps(data)
	resp = Response(response=resp_data, status=200, mimetype="application/json")
	return resp

@app.route('/deploy', methods=['GET', 'POST'])
def deploy_code():
	data = json.loads(request.form['json_str'])
	url = deploy_user_code(data['code'])
	data = {'url': url,}
	resp_data = json.dumps(data)
	resp = Response(response=resp_data, status=200, mimetype="application/json")
	return resp


if __name__ == "__main__":
    app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'], debug=True)
