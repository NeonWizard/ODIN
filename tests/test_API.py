import unittest

from neuraltextserver import app

class TestSimple(unittest.TestCase):
	# -- Setup --
	def setUp(self):
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		self.assertEqual(app.debug, False)

		self.app = app.test_client()

	# -- Tests --
	def test_ping(self):
		response = self.app.get("/api/neuraltext/ping")
		self.assertEquals(response.status_code, 200)

if __name__ == "__main__":
	unittest.main()
