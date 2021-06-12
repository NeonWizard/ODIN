import flask
from flask import request, jsonify
import os

app = flask.Flask(__name__)

@app.route("/api/ping", methods=["GET"])
def ping(): return "pong"

@app.route("/api/docs", methods=["GET"])
def docs():
	"""
	API documentation.
	"""

	# TODO: move to external file and extrapolate from methods
	endpoints = [
		{
			"method": "GET",
			"path": "/ping",
			"description": "Returns 200 OK and the text \"pong\" to signal the server is online.",
			"params": [],
			"response": {
				"data": "ping"
			}
		},
		{
			"method": "GET",
			"path": "/models",
			"description": "Returns all available GPT-2 models by name.",
			"params": [],
			"response": {
				"data": [
					{
					"id": 0,
					"name": "john-keats-300"
					},
					{
					"id": 1,
					"name": "deiga-500"
					}
				],
				"meta": {
					"result_count": 2
				}
			}
		},
		{
			"method": "GET",
			"path": "/models/<name>",
			"description": "Generates text via a specified GPT-2 model.",
			"params": [
				["words", "int", "Number of words to generate."]
			],
			"response": {
				"data": "Howdy, my name is Rawhide Kobayashi. I'm a 27 year old Japanese Japamerican (western culture fan for you foreigners). I brand and wrangle cattle on my ranch, and spend my days perfecting the craft and enjoying superior American passtimes. (Barbeque, Rodeo, Fireworks) I train with my branding iron every day.",
				"meta": {
					"generation_time": "15582"
				}
			}
		},
	]

	return flask.render_template("api_documentation.html", endpoints=endpoints)

@app.route("/api/models", methods=["GET"])
def models():
	"""
	Returns all available GPT-2 models by name.
	"""

	return []

@app.route("/api/models/<name>", methods=["GET"])
def generate(name):
	"""
	Generates text via a specified GPT-2 model.
	"""

	length = request.args.get("length")

	print(name, length)

	return {}


if __name__ == "__main__":
	# start server
	app.run()
