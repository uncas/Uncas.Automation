import unittest

from uncas_automation.Services.Google.GoogleDocsService import readDocument

class GoogleDocsServiceTests(unittest.TestCase):
	def test_readDocument(self):
		# Here's a test docoment that I have used for testing a certain structure:
		# https://docs.google.com/document/d/16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE/edit
		id = "16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE"
		doc = readDocument(id)
		title = doc["title"]
		text = doc["text"]
		self.assertEqual(title, "Automation Test Doc")
		self.assertIn("Journal", text)
