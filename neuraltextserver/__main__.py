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
def homepage():
	routes = []

	for rule in app.url_map.iter_rules():
		if not str(rule).startswith("/api"): continue
		routes.append('%s' % rule)

	return jsonify(routes)

@app.route("/api/model", methods=["GET"])
def generate():
	model = request.args.get("model")
	length = request.args.get("length")

	print(model, length)


if __name__ == "__main__":
	# start server
	app.run()
