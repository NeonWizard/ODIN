import flask
from flask import Blueprint, request
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from functools import wraps

app = flask.current_app
blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route("/auth", methods=["POST"])
def auth():
	"""
	Authenticate the user via username/password and return a token.
	---
	tags: [Authorization]
	definitions:
		-	schema:
				id: Error
				properties:
					error:
						type: string
						description: Information about the error
	parameters:
		-	name: username
			in: body
			description: The user's username
			required: true
			schema:
				type: string

		-	name: password
			in: body
			description: The user's password
			required: true
			schema:
				type: string

	responses:
		200:
			description: User was successfully authenticated
			schema:
				type: object
				properties:
					token:
						type: string
						description: An auth token that is valid for 24 hours
		400:
			description: Request contained invalid data
			schema:
				$ref: "#/definitions/Error"

		401:
			description: Unable to authenticate with the specified username and password
			schema:
				$ref: "#/definitions/Error"
	"""

	username = request.json.get("username")
	password = request.json.get("password")
	if username == None or password == None:
		return { "error": "Username and password are both required." }, 400

	if username != app.config["USERNAME"] or password != app.config["PASSWORD"]:
		return { "error": "Username and password are invalid." }, 401

	s = Serializer(app.config["SECRET_KEY"], expires_in=86400)
	return { "token": s.dumps({ "username": username }) }

def require_token(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not "Authorization" in request.headers:
			return { "error": "Authorization header is required." }, 400

		s = Serializer(app.config["SECRET_KEY"])
		token = request.headers.get("Authorization").split()[1]

		try:
			username = s.loads(token)["username"]
		except BadSignature:
			return { "error": "Invalid auth token." }, 401
		except SignatureExpired:
			return { "error": "Auth token is expired." }, 401

		if username != app.config["USERNAME"]:
			return { "error": "Token is not authorized for this resource." }, 401

		return f(*args, **kwargs)

	return decorated_function
