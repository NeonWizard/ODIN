import flask
from flask import request, jsonify
import os

from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)
app.config["DEBUG"] = True if "DEBUG" in os.environ and os.environ["DEBUG"].lower() == "true" else False

@app.route("/api/ping", methods=["GET"])
def ping(): return "pong"

@app.route("/api/docs", methods=["GET"])
def docs():
	"""
	API documentation.
	"""

	with open("neuraltextserver/APIDOC.md", 'r') as f:
		rendered = markdownFormat(f.read())

	return rendered

@app.route("/api/models", methods=["GET"])
def models():
	"""
	Returns all available GPT-2 models by name.
	"""

	pass

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
