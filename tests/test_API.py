import unittest

from api.app import app

class TestSimple(unittest.TestCase):
	# -- Setup --
	def setUp(self):
		app.testing = True
		app.debug = False

		self.app = app.test_client()

	# -- Tests --
	def test_auth(self):
		response = self.app.get("/api/auth")
		self.assertEqual(response.status_code, 200)

	def test_generate(self):
		"""
		Tests for /api/models/<name>
		This tests text generation and parameters.
		"""

		endpoint = "/api/models/test"

		# - Fail cases
		# length
		response = self.app.get(endpoint, data={
			"length": -1
		})
		self.assertEqual(response.status_code, 400)

		# temperature
		response = self.app.get(endpoint, data={
			"temperature": -1
		})
		self.assertEqual(response.status_code, 400)
		response = self.app.get(endpoint, data={
			"temperature": 2.3
		})
		self.assertEqual(response.status_code, 400)

		# top_k
		response = self.app.get(endpoint, data={
			"top_k": -1
		})
		self.assertEqual(response.status_code, 400)

		# top_p
		response = self.app.get(endpoint, data={
			"top_p": -1
		})
		self.assertEqual(response.status_code, 400)
		response = self.app.get(endpoint, data={
			"top_p": 3.7
		})
		self.assertEqual(response.status_code, 400)

		# n_samples
		response = self.app.get(endpoint, data={
			"n_samples": -1
		})
		self.assertEqual(response.status_code, 400)

		# batch_size
		response = self.app.get(endpoint, data={
			"n_samples": 1,
			"batch_size": 2
		})
		self.assertEqual(response.status_code, 400)

		# - Success cases
		# default
		response = self.app.get(endpoint)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json["meta"]["parameters"], {
            "batch_size": 1,
            "include_prefix": True,
            "length": 512,
            "n_samples": 1,
            "prefix": None,
            "sample_delimiter": "",
            "seed": None,
            "temperature": 0.7,
            "top_k": 0,
            "top_p": 0.0,
            "truncate": None
		})

		# configured
		response = self.app.get(endpoint, data={
			"length": 4,
			"temperature": 1.0,
			"top_k": 1,
			"n_samples": 2,
			"batch_size": 2,
			"truncate": "someword",
			"prefix": "yeap",
			"seed": 34895738945,
			"include_prefix": False
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json["meta"]["parameters"], {
            "batch_size": 2,
            "include_prefix": False,
            "length": 4,
            "n_samples": 2,
            "prefix": "yeap",
            "sample_delimiter": "====================\n",
            "seed": 34895738945,
            "temperature": 1.0,
            "top_k": 1,
            "top_p": 0.0,
            "truncate": "someword"
		})


	def test_ping(self):
		response = self.app.get("/api/ping")
		self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
	unittest.main()
