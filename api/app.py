import os
import time, datetime
import flask
from flask import request, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

import odin

from .blueprints.example import blueprint as jinja_template_blueprint
from .blueprints.basic import blueprint as basic_endpoints
from .blueprints.auth import blueprint as auth_endpoints

app = flask.Flask(__name__)
app.register_blueprint(jinja_template_blueprint)
app.register_blueprint(basic_endpoints)
app.register_blueprint(auth_endpoints)

swaggerui_blueprint = get_swaggerui_blueprint(
	"/api/docs",
	"/api/spec"
)
app.register_blueprint(swaggerui_blueprint)

@app.route("/api/spec")
def spec():
	swag = swagger(app)
	swag["info"]["title"] = "ODIN API"
	swag["info"]["version"] = 1.0
	return jsonify(swag)

@app.route("/api/models", methods=["GET"])
def models():
	"""
	Returns all available GPT-2 models.
	---
	tags: [Models]
	definitions:
		- schema:
			id: Model
			properties:
				name:
					type: string
					description: Identifying name for the model (such as deiga-300)
	responses:
		200:
			description: Successfully retrieved list of models
			schema:
				type: object
				properties:
					models:
						type: array
						description: An array of all available models
						items:
							$ref: "#/definitions/Model"
	"""

	models = odin.models()

	return {
		"models": models
	}

@app.route("/api/models/<string:name>", methods=["GET"])
def generate(name):
	"""
	Generates text via a specified GPT-2 model.
	---
	tags: [Models]
	parameters:
		-	name: name
			in: path
			description: Name of the model
			type: string
			required: true

		-	name: length
			in: body
			description: The number of words to generate
			schema:
				type: integer
				minimum: 1
				maximum: 16384
				default: 512

		-	name: truncate
			in: body
			description: A token to truncate the returned text at
			schema:
				type: string

		-	name: prefix
			in: body
			description: Text to start generation from
			schema:
				type: string

		-	name: seed
			in: body
			description: An integer to seed the random number generator to have deterministic results
			schema:
				type: integer

		-	name: temperature
			in: body
			description: The temperature to use for generation
			schema:
				type: number
				format: float
				minimum: 0.0
				maximum: 1.0
				default: 0.7

		-	name: top_k
			in: body
			description: Sample from the K most likely words (can't be used with top_p)
			schema:
				type: integer
				default: 0

		-	name: top_p
			in: body
			description: Sample from the smallest possible set of words whose cumulative probability exceeds P (can't be used with top_k)
			schema:
				type: number
				format: float
				maximum: 1.0
				default: 0.0

		-	name: include_prefix
			in: body
			description: Whether to include the specified prefix in the returned text
			schema:
				type: boolean
				default: true

		-	name: sample_delimiter
			in: body
			description: Text used to delimit multiple samples when n_samples > 1
			schema:
				type: string
				default: "===================="

		-	name: n_samples
			in: body
			description: Number of samples to generate
			schema:
				type: integer
				minimum: 1
				maximum: 8
				default: 1

		-	name: batch_size
			in: body
			description: Number of batches (only affects speed/memory). Must divide n_samples
			schema:
				type: integer
				minimum: 1
				default: 1

	responses:
		200:
			description: Successfully generated text from the specified model
			schema:
				type: object
				properties:
					data:
						type: string
						description: The generated text
					meta:
						type: object
						description: Meta information about the request
						properties:
							generation_time:
								type: integer
								description: The amount of time taken to generate the text in milliseconds
							parameters:
								type: object
								description: All of the generation parameters that resulted from the request
		400:
			description: Request contained invalid data
			schema:
				type: object
				properties:
					error:
						type: string
						description: Information about the error
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
	if length < 1 or length > 16384:
		return { "error": "Valid length is between 1 and 16384 inclusively." }, 400
	if temperature < 0.0 or temperature > 1.0:
		return { "error": "Valid temperature is between 0.0 and 1.0 inclusively." }, 400
	if top_k != 0 and top_p != 0.0:
		return { "error": "top_k and top_p are mutually exclusive." }, 400
	if top_k < 0:
		return { "error": "top_k must be a non-negative number." }, 400
	if top_p < 0.0 or top_p > 1.0:
		return { "error": "Valid top_p is between 0.0 and 1.0 inclusively." }, 400
	if n_samples < 1 or n_samples > 8:
		return { "error": "Valid n_samples is between 1 and 8 inclusively." }, 400
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
