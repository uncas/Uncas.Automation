import unittest

class NewAssistantIntegrationTests(unittest.TestCase):
	def test_pass(self):
		pass

	def test_read_web_page(self):
		from Services.web_page_reader import read_web_page_text, read_web_page_markdown
		from Utils.FileUtils import writeText
		writeText("Output", "google_com.txt", read_web_page_text("https://www.google.com"))
		writeText("Output", "google_com.md", read_web_page_markdown("https://www.google.com"))
