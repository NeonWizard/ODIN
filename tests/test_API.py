import unittest
import os
from dotenv import load_dotenv
load_dotenv()

from api.app import app
from odin import defaults

class TestAPI(unittest.TestCase):
	# -- Setup --
	def setUp(self):
		app.testing = True
		app.debug = False

		self.app = app.test_client()

	# -- Tests --
	def test_auth(self):
		data = {
			"username": os.getenv("USERNAME"),
			"password": os.getenv("PASSWORD")
		}
		response = self.app.post("/api/auth", json=data)
		self.assertEqual(response.status_code, 200)

	def test_generate(self):
		"""
		Tests for /api/models/<name>
		This tests text generation and parameters.
		"""

		# TODO: split each into different methods

		endpoint = "/api/models/test"

		# Log in
		data = {
			"username": os.getenv("USERNAME"),
			"password": os.getenv("PASSWORD")
		}
		token = self.app.post("/api/auth", json=data).get_data(as_text=True)

		headers = {
			"Authorization": f"Bearer {token}"
		}

		# - Fail cases
		# length
		response = self.app.post(endpoint, json={
			"length": -1
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# seed
		response = self.app.post(endpoint, json={
			"seed": 2**33
		}, headers=headers)
		self.assertEqual(response.status_code, 400)
		response = self.app.post(endpoint, json={
			"seed": 48573,
			"n_samples": 2
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# temperature
		response = self.app.post(endpoint, json={
			"temperature": -1
		}, headers=headers)
		self.assertEqual(response.status_code, 400)
		response = self.app.post(endpoint, json={
			"temperature": 2.3
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# top_k
		response = self.app.post(endpoint, json={
			"top_k": -1
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# top_p
		response = self.app.post(endpoint, json={
			"top_p": -1
		}, headers=headers)
		self.assertEqual(response.status_code, 400)
		response = self.app.post(endpoint, json={
			"top_p": 3.7
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# n_samples
		response = self.app.post(endpoint, json={
			"n_samples": -1
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# batch_size
		response = self.app.post(endpoint, json={
			"n_samples": 1,
			"batch_size": 2
		}, headers=headers)
		self.assertEqual(response.status_code, 400)

		# - Success cases
		# default
		response = self.app.post(endpoint, json={}, headers=headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json["meta"]["parameters"], {
			"batch_size": defaults.BATCH_SIZE,
			"include_prefix": defaults.INCLUDE_PREFIX,
			"length": defaults.LENGTH,
			"n_samples": defaults.N_SAMPLES,
			"prefix": defaults.PREFIX,
			"seed": defaults.SEED,
			"temperature": defaults.TEMPERATURE,
			"top_k": defaults.TOP_K,
			"top_p": defaults.TOP_P,
			"truncate": defaults.TRUNCATE
		})

		# configured
		response = self.app.post(endpoint, json={
			"length": 4,
			"temperature": 1.0,
			"top_k": 1,
			"n_samples": 2,
			"batch_size": 2,
			"truncate": "someword",
			"prefix": "yeap",
			"include_prefix": False
		}, headers=headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json["meta"]["parameters"], {
			"batch_size": 2,
			"include_prefix": False,
			"length": 4,
			"n_samples": 2,
			"prefix": "yeap",
			"seed": None,
			"temperature": 1.0,
			"top_k": 1,
			"top_p": 0.0,
			"truncate": "someword"
		})


	def test_ping(self):
		response = self.app.get("/api/ping")
		self.assertEqual(response.status_code, 200)
