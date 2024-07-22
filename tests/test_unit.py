import unittest
#from .context import easai

class AssistantUnitTests(unittest.TestCase):
	def test_getFilePath(self):
		from easai.Utils.FileUtils import getFilePath
		path = getFilePath("../Data/test.db")
		self.assertIn("easai/Utils/../../Data/test.db", path)

	def test_getListOfTextContent(self):
		items = self.getListOfTexts()
		self.assertEqual(len(items), 12)
	
	def test_mapListOfTextContentToDatedEntries(self):
		from easai.Flows.PersonalAssistant.Resources.resource_tools import mapListOfTextContentToDatedEntries
		items = self.getListOfTexts()
		entries = mapListOfTextContentToDatedEntries(items, 2, "Journal entries")
		self.assertEqual(len(entries), 2)
		self.assertEqual(entries[0]["date"], {'year': 2024, 'month': 3, 'day': 1})
		self.assertEqual(entries[0]["text"], "How it is going?\nOle Lynge Sørensen was there\n")
		self.assertEqual(entries[1]["date"], {'year': 2024, 'month': 2, 'day': 20})
		self.assertEqual(entries[1]["text"], "It is going forward.\nBut sometimes also backwards\n")

	def test_mapListOfTextContentToDatedEntries_MacCount(self):
		from easai.Flows.PersonalAssistant.Resources.resource_tools import mapListOfTextContentToDatedEntries
		items = self.getListOfTexts()
		entries = mapListOfTextContentToDatedEntries(items, 2, "Journal entries", maxCount = 1)
		self.assertEqual(len(entries), 1)
		self.assertEqual(entries[0]["date"], {'year': 2024, 'month': 3, 'day': 1})

	def test_mapListOfTextContentToDatedEntries_Last1Day(self):
		from easai.Flows.PersonalAssistant.Resources.resource_tools import mapListOfTextContentToDatedEntries
		items = self.getListOfTexts()
		entries = mapListOfTextContentToDatedEntries(items, 2, "Journal entries", lastNDays = 1)
		self.assertEqual(len(entries), 0)

	def test_mapListOfTextContentToDatedEntries_LastNDays(self):
		import datetime
		from easai.Flows.PersonalAssistant.Resources.resource_tools import mapListOfTextContentToDatedEntries
		items = self.getListOfTexts()
		sinceDate = datetime.datetime(2024, 2, 25)
		daysSinceDate = (datetime.datetime.now() - sinceDate).days
		entries = mapListOfTextContentToDatedEntries(items, 2, "Journal entries", lastNDays = daysSinceDate)
		self.assertEqual(len(entries), 1)

	def getListOfTexts(self):
		import json
		from easai.Services.Google.GoogleDocsService import getListOfTextContent
		from easai.Utils.FileUtils import getFilePath
		file = getFilePath("Tests/GoogleDocContent.json")
		fileStream = open(file)
		content = json.load(fileStream)
		fileStream.close()
		return getListOfTextContent(content)
