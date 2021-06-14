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
		"models": models
	}

@app.route("/api/models/<string:name>", methods=["GET"])
def generate(name):
	"""
	Generates text via a specified GPT-2 model.
	"""

	# TODO: consider having generate build out a dynamically generated URL to confirm generation request by requesting to generated URL
	# Two separate endpoints: request_generate and generate. The first would return a token from the server, which would have to be sent
	# in the call to the second endpoint.

	# - Parse arguments
	length = request.form.get("length", 512, type=int)
	truncate = request.form.get("truncate", None, type=str) # token to truncate at
	prefix = request.form.get("prefix", None, type=str)
	seed = request.form.get("seed", None, type=int)
	temperature = request.form.get("temperature", 0.7, type=float)
	top_k = request.form.get("top_k", 0, type=int)
	top_p = request.form.get("top_p", 0.0, type=float)

	include_prefix = request.form.get("include_prefix", "true", type=str)
	include_prefix = include_prefix.lower() == "true"

	sample_delimiter = request.form.get("sample_delimiter", "=" * 20 + "\n", type=str)
	n_samples = request.form.get("n_samples", 1, type=int)
	if n_samples == 1: sample_delimiter = ""
	batch_size = request.form.get("batch_size", 1, type=int) # Number of batches (only affects speed/memory. Must divide n_samples

	# - Validate arguments
	if length <= 0 or length >= 16384:
		return { "error": "Valid length is between 0 and 16384 exclusively." }, 400
	if temperature < 0.0 or temperature > 1.0:
		return { "error": "Valid temperature is between 0.0 and 1.0 inclusively." }, 400
	if top_k != 0 and top_p != 0.0:
		return { "error": "top_k and top_p are mutually exclusive." }, 400
	if top_k < 0:
		return { "error": "top_k must be a non-negative number." }, 400
	if top_p < 0.0 or top_p > 1.0:
		return { "error": "Valid top_p is between 0.0 and 1.0 inclusively." }, 400
	if n_samples <= 0 or n_samples > 8:
		return { "error": "Valid n_samples is between 0 and 8 inclusively." }, 400
	if n_samples % batch_size != 0:
		return { "error": "Batch sizes must be able to divide n_samples" }, 400

	# - Generate response
	name = name.lower()
	if name == "test":
		gen_time = datetime.timedelta(milliseconds=69)
		result = "there are 40 cherries on the cherry tree."
	else:
		start_time = datetime.datetime.now()
		result = odin.generate(name)
		gen_time = datetime.datetime.now() - start_time

	return {
		"data": result,
		"meta": {
			"generation_time": round(gen_time.total_seconds() * 1000),
			"parameters": {
				"length": length,
				"truncate": truncate,
				"prefix": prefix,
				"seed": seed,
				"temperature": temperature,
				"top_k": top_k,
				"top_p": top_p,
				"include_prefix": include_prefix,
				"sample_delimiter": sample_delimiter,
				"n_samples": n_samples,
				"batch_size": batch_size
			}
		}
	}


if __name__ == "__main__":
	# start server
	app.run()
