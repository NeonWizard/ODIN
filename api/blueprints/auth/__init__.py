from flask import Blueprint, request

blueprint = Blueprint("auth", __name__, url_prefix="/api")

@blueprint.route("/auth", methods=["GET"])
def auth():
	return "auth"
