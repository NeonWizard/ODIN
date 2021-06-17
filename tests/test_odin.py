import unittest

import odin

class TestOdin(unittest.TestCase):
	# -- Setup --
	def setUp(self):
		pass

	# -- Tests --
	def test_list_models(self):
		models = odin.models()

	def test_generate(self):
		odin.generate(
			"test",
			length=16,
			truncate="sometext",
			prefix="someprefix",
			seed=489534,
			temperature=0.8,
			top_k=0,
			top_p=0,
			include_prefix=True,
			n_samples=2,
			batch_size=2
		)
