import os
import time, datetime
import flask
from flask import request, jsonify

import odin

from .blueprints.example import blueprint as jinja_template_blueprint
from .blueprints.basic import blueprint as basic_endpoints
from .blueprints.auth import blueprint as auth_endpoints

app = flask.Flask(__name__)
app.register_blueprint(jinja_template_blueprint)
app.register_blueprint(basic_endpoints)
app.register_blueprint(auth_endpoints)


@app.route("/api/models", methods=["GET"])
def models():
	"""
	Returns all available GPT-2 models.
	"""

	models = odin.models()

	return {
		"data": models,
		"meta": {
			"result_count": len(models)
		}
	}

@app.route("/api/models/<string:name>", methods=["GET"])
def generate(name):
	"""
	Generates text via a specified GPT-2 model.
	"""

	# TODO: consider having generate build out a dynamically generated URL to confirm generation request by requesting to generated URL
	# Two separate endpoints: request_generate and generate. The first would return a token from the server, which would have to be sent
	# in the call to the second endpoint.

	# length = request.args.get("length")

	start_time = datetime.datetime.now()

	result = odin.generate(name)

	gen_time = datetime.datetime.now() - start_time

	return {
		"data": result,
		"meta": {
			"generation_time": round(gen_time.total_seconds() * 1000)
		}
	}


if __name__ == "__main__":
	# start server
	app.run()
