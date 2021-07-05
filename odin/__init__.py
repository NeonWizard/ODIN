import os
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import gpt_2_simple as gpt2

from . import defaults

def models():
	"""
	Returns all available GPT-2 models.
	"""

	return next(os.walk("models/"))[1]

def generate(
	model_name,
	length=defaults.LENGTH,
	truncate=defaults.TRUNCATE,
	prefix=defaults.PREFIX,
	seed=defaults.SEED,
	temperature=defaults.TEMPERATURE,
	top_k=defaults.TOP_K,
	top_p=defaults.TOP_P,
	include_prefix=defaults.INCLUDE_PREFIX,
	n_samples=defaults.N_SAMPLES,
	batch_size=defaults.BATCH_SIZE
):
	"""
	Generates text via a specified GPT-2 model.
	"""

	if model_name == "test":
		return { "data": ["there are 40 cherries on the cherry tree."] }

	if model_name not in models():
		return { "error": "The specified model does not exist." }

	sess = gpt2.start_tf_sess()
	gpt2.load_gpt2(sess, model_name=model_name)

	response = gpt2.generate(
		sess,
		model_name=model_name,
		return_as_list=True,

		length=length,
		truncate=truncate,
		prefix=prefix,
		seed=seed,
		temperature=temperature,
		top_k=top_k,
		top_p=top_p,
		nsamples=n_samples,
		batch_size=batch_size
	)
	for i in range(len(response)):
		if prefix and not include_prefix:
			response[i] = response[i][len(prefix):]

	print(response)

	gpt2.reset_session(sess)

	return { "data": response }
