import unittest

from api.app import app

class TestSimple(unittest.TestCase):
	# -- Setup --
	def setUp(self):
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		self.assertEqual(app.debug, False)

		self.app = app.test_client()

	# -- Tests --
	def test_auth(self):
		response = self.app.get("/api/auth")
		self.assertEquals(response.status_code, 200)

	def test_ping(self):
		response = self.app.get("/api/ping")
		self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
	unittest.main()
