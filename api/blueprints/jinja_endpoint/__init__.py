from flask import Blueprint, request, render_template

blueprint = Blueprint("meme", __name__, url_prefix="/api")

@blueprint.route("/meme")
def get_template():
    top = request.args.get("top") if "top" in request.args else "CANCEL THE WEB API CREATION"
    bottom = request.args.get("bottom") if "bottom" in request.args else "I HAVE TO WATCH THIS BIRD"

    return render_template("example.html", top=top, bottom=bottom)
