import os
def models():
	"""
	Returns all available GPT-2 models.
	"""

	return next(os.walk("models/"))[1]

def generate(model):
	"""
	Generates text via a specified GPT-2 model.
	"""

	return ""
