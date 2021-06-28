import os
import time, datetime
import flask
from flask import request, jsonify
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

import odin

from .blueprints.example import blueprint as jinja_template_blueprint
from .blueprints.basic import blueprint as basic_endpoints
from .blueprints.auth import blueprint as auth_endpoints
from .blueprints.auth import require_token

from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(jinja_template_blueprint)
app.register_blueprint(basic_endpoints)
app.register_blueprint(auth_endpoints)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", None)
assert(app.config["SECRET_KEY"] != None and app.config["SECRET_KEY"] != "")

app.config["USERNAME"] = os.getenv("USERNAME", None)
app.config["PASSWORD"] = os.getenv("PASSWORD", None)
assert(app.config["USERNAME"] != None and app.config["USERNAME"] != "")
assert(app.config["PASSWORD"] != None and app.config["PASSWORD"] != "")

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

@app.errorhandler(404)
def not_found(e):
	return jsonify(error=str(e)), 404

@app.route("/api/models", methods=["GET"])
@require_token
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

@app.route("/api/models/<string:name>", methods=["POST"])
@require_token
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

	# - Parse arguments
	length = request.json.get("length", odin.defaults.LENGTH)
	truncate = request.json.get("truncate", odin.defaults.TRUNCATE)
	prefix = request.json.get("prefix", odin.defaults.PREFIX)
	seed = request.json.get("seed", odin.defaults.SEED)
	temperature = request.json.get("temperature", odin.defaults.TEMPERATURE)
	top_k = request.json.get("top_k", odin.defaults.TOP_K)
	top_p = request.json.get("top_p", odin.defaults.TOP_P)

	include_prefix = request.json.get("include_prefix", odin.defaults.INCLUDE_PREFIX)

	n_samples = request.json.get("n_samples", odin.defaults.N_SAMPLES)
	batch_size = request.json.get("batch_size", odin.defaults.BATCH_SIZE)

	# - Validate arguments
	if length < 1 or length > 16384:
		return { "error": "Valid length is between 1 and 16384 inclusively." }, 400
	if seed and (seed < 0 or seed > 2**32-1):
		return { "error": "Valid seed is between 0 and 2**32 - 1 inclusively." }, 400
	if temperature < 0.0 or temperature > 1.0:
		return { "error": "Valid temperature is between 0.0 and 1.0 inclusively." }, 400
	if top_k != 0 and top_p != 0.0:
		return { "error": "top_k and top_p are mutually exclusive." }, 400
	if top_k < 0:
		return { "error": "top_k must be a non-negative number." }, 400
	if top_p < 0.0 or top_p > 1.0:
		return { "error": "Valid top_p is between 0.0 and 1.0 inclusively." }, 400
	if seed and n_samples > 1:
		return { "error": "If seed is set, n_samples must be equal to 1." }, 400
	if n_samples < 1 or n_samples > 8:
		return { "error": "Valid n_samples is between 1 and 8 inclusively." }, 400
	if n_samples % batch_size != 0:
		return { "error": "Batch sizes must be able to divide n_samples" }, 400

	# - Generate response
	name = name.lower()
	if name == "test":
		gen_time = datetime.timedelta(milliseconds=69)
		result = { "data": "there are 40 cherries on the cherry tree." }
	else:
		start_time = datetime.datetime.now()
		result = odin.generate(
			name,
			length=length,
			truncate=truncate,
			prefix=prefix,
			seed=seed,
			temperature=temperature,
			top_k=top_k,
			top_p=top_p,
			include_prefix=include_prefix,
			n_samples=n_samples,
			batch_size=batch_size
		)
		gen_time = datetime.datetime.now() - start_time

	if "error" in result:
		return { "error": result["error"] }, 400

	return {
		"data": result["data"],
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
				"n_samples": n_samples,
				"batch_size": batch_size
			}
		}
	}


if __name__ == "__main__":
	# start server
	app.run()
