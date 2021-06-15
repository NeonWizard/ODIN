from flask import Blueprint, request

blueprint = Blueprint("basic", __name__, url_prefix="/api")

@blueprint.route("/ping", methods=["GET"])
def ping():
	"""
	Returns 200 OK and the text 'pong' to signal the server is online.
	---
	tags: [Basic]
	responses:
		200:
			description: Server is functioning properly and is reachable
			schema:
				type: string
				example: "pong"
		default:
			description: Something bad happened
	"""
	return "pong"
