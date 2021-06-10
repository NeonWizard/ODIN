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

	return None

@app.route("/api/models", methods=["GET"])
def models():
	"""
	Returns all available GPT-2 models by name.
	"""

	return flask.render_template("")

@app.route("/api/models/<name>", methods=["GET"])
def generate(name):
	"""
	Generates text via a specified GPT-2 model.
	"""

	length = request.args.get("length")

	print(name, length)


if __name__ == "__main__":
	# start server
	app.run()
