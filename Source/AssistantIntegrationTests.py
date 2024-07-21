import unittest

class AssistantIntegrationTests(unittest.TestCase):
	def test_downloadGoogleDocTestContent(self):
		from Services.Google.GoogleDocsService import downloadDocumentContent
		from Utils.FileUtils import writeText, getFilePath
		import json
		# Here's a test docoment that I use for testing:
		# https://docs.google.com/document/d/16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE/edit
		testDocId = "16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE"
		content = downloadDocumentContent(testDocId)["content"]
		writeText(getFilePath("Tests"), "GoogleDocContent.json", json.dumps(content, indent = 4))

	def test_GoogleMapsDirections(self):
		from Services.Google.GoogleMapsService import GoogleMapsService
		result = GoogleMapsService.GetDirections("Berlin, Germany", "Paris, France")
		self.assertGreater(result["distanceInKm"], 1000)
		self.assertGreater(result["durationInMinutes"], 500)

	@unittest.skip("Skipping for now")
	def test_getMails(self):
		from Services.Google.GmailService import getInboxMessages
		messages = getInboxMessages()
		for message in messages:
			print("From " + message["sender"] + ": " + message["subject"])
	
	@unittest.skip("Skipping for now")
	def test_get_electric_cars_in_denmark(self):
		from Services.eletric_cars_service import get_electric_cars_in_denmark
		cars = get_electric_cars_in_denmark()
		print(cars[:1000])
		self.assertGreater(len(cars), 0)
