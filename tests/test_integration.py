import unittest
import json

from uncas_automation.Services.Google.GoogleDocsService import downloadDocumentContent
from easai.utils.file_utils import write_text
from uncas_automation.Utils.FileUtils import getFilePath

class AssistantIntegrationTests(unittest.TestCase):
	def test_downloadGoogleDocTestContent(self):
		# Here's a test docoment that I use for testing:
		# https://docs.google.com/document/d/16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE/edit
		testDocId = "16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE"
		content = downloadDocumentContent(testDocId)["content"]
		write_text(getFilePath("../tests/data"), "GoogleDocContent.json", json.dumps(content, indent = 4))

	def test_GoogleMapsDirections(self):
		from uncas_automation.Services.Google.GoogleMapsService import GoogleMapsService
		result = GoogleMapsService.GetDirections("Berlin, Germany", "Paris, France")
		self.assertGreater(result["distanceInKm"], 1000)
		self.assertGreater(result["durationInMinutes"], 500)

	def test_getMails(self):
		from uncas_automation.Services.Google.GmailService import getInboxMessages
		messages = getInboxMessages()
		#for message in messages:
		#	print("From " + message["sender"] + ": " + message["subject"])
	
	def test_get_electric_cars_in_denmark(self):
		from uncas_automation.Services.eletric_cars_service import get_electric_cars_in_denmark
		cars = get_electric_cars_in_denmark()
		#print(cars[:1000])
		self.assertGreater(len(cars), 0)

	def test_wikipedia(self):
		from uncas_automation.Services.wikipedia_service import search_wikipedia
		result = search_wikipedia("Covid-19")
		#print("wikipedia: " + result)

	def test_wikipedia_langchain(self):
		from uncas_automation.Services.wikipedia_service import search_wikipedia_langchain
		result = search_wikipedia_langchain("Covid-19")
		#print("wikipedia_langchain: " + result)

	def test_search_internet(self):
		from uncas_automation.Services.internet_search_service import search_internet
		result = search_internet("Covid-19", top_results_to_return = 10, country_code = "dk", language_code = "da")
		#for item in result:
		#	print(item["title"], item["href"])

	def test_read_web_page(self):
		from uncas_automation.Services.web_page_reader import read_web_page_text, read_web_page_markdown
		from easai.utils.file_utils import write_text
		write_text("Output", "google_com.txt", read_web_page_text("https://www.google.com"))
		write_text("Output", "google_com.md", read_web_page_markdown("https://www.google.com"))

	def test_find_images(self):
		import json
		from uncas_automation.Services.internet_search_service import find_images
		from easai.utils.file_utils import write_text

		images = list(find_images("python", top_results_to_return = 5))
		self.assertEqual(len(images), 5)
		write_text("Output", "images.json", json.dumps(images, indent = 4))

	def test_read_webpage_text(self):
		from uncas_automation.Services.web_page_reader import read_web_page_text
		text = read_web_page_text("https://raw.githubusercontent.com/uncas/Uncas.Automation/main/uncas_automation/assistant/Readme.md")
		self.assertIn("Personal assistant", text)
