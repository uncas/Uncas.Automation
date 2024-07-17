import unittest

class AssistantUnitTests(unittest.TestCase):
	def test_getFilePath(self):
		from Utils.FileUtils import getFilePath
		path = getFilePath("../Data/test.db")
		self.assertIn("Source/Utils/../../Data/test.db", path)

	def getListOfTexts(self):
		from Services.Google.GoogleDocsService import getListOfTextContent
		import json
		from Utils.FileUtils import getFilePath
		file = getFilePath("Tests/GoogleDocContent.json")
		fileStream = open(file)
		content = json.load(fileStream)
		fileStream.close()
		return getListOfTextContent(content)

	def test_getListOfTextContent(self):
		items = self.getListOfTexts()
		self.assertEqual(len(items), 10)
	
	def test_mapListOfTextContentToDatedEntries(self):
		import datetime
		items = self.getListOfTexts()
		from Flows.PersonalAssistant.Resources.ResourceTools import mapListOfTextContentToDatedEntries
		entries = mapListOfTextContentToDatedEntries(items, 2, "Journal entries")
		self.assertEqual(len(entries), 2)
		self.assertEqual(entries[0]["date"], datetime.datetime(2024, 3, 1))
		self.assertIn("How it is going?", entries[0]["text"])
		self.assertEqual(entries[1]["date"], datetime.datetime(2024, 2, 20))
		self.assertIn("It is going forward.", entries[1]["text"])
		self.assertIn("But sometimes also backwards", entries[1]["text"])
		self.assertNotIn("Something irrelevant", entries[1]["text"])
		self.assertNotIn("Bla bla bla", entries[1]["text"])
	
if __name__ == '__main__':
    unittest.main()