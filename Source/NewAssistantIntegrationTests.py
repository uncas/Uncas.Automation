import unittest

class NewAssistantIntegrationTests(unittest.TestCase):
	def test_pass(self):
		pass

	def test_find_images(self):
		import json
		from Services.internet_search_service import find_images
		from Utils.FileUtils import writeText

		images = list(find_images("python", top_results_to_return = 5))
		self.assertEqual(len(images), 5)
		for image in images:
			print(image)
		writeText("Output", "images.json", json.dumps(images, indent = 4))
