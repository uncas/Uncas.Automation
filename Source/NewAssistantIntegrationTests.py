import unittest

class NewAssistantIntegrationTests(unittest.TestCase):
	def test_pass(self):
		pass

	def test_read_web_page(self):
		from Services.web_page_reader import read_web_page
		print(read_web_page("https://www.google.com"))