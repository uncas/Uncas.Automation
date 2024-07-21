class AssistantTool:
	def __init__(self, method, description, parameters = [], name = None):
		self.parameters = parameters
		self.description = description
		self.method = method
		self.name = name if name else method.__name__
	
	def mapToOpenAiTool(self):
		properties = {}
		for parameter in self.parameters:
			properties[parameter.name] = parameter.getOpenAiToolProperties()
		return {
			"type": "function",
			"function": {
				"name": self.name,
				"description": self.description,
				"parameters": {
					"type": "object",
					"properties": properties
				}
			}
		}

class AssistantToolParameter:
	def __init__(self, name, description, type = "string", enum = None):
		self.name = name
		self.description = description
		self.type = type
		self.enum = enum
	
	def getOpenAiToolProperties(self):
		value = {
			"type": self.type,
			"description": self.description
		}
		if self.enum:
			value["enum"] = self.enum
		return value

def getAllTools():
	from Flows.PersonalAssistant.Functions.createJiraIssue import createJiraIssueTool, getMyJiraIssuesTool
	from Flows.PersonalAssistant.Functions.getCalendarEvents import getTodaysCalendarEventsTool
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeatherTool
	from Flows.PersonalAssistant.Functions.getDateAndTime import getDateAndTimeTool
	from Flows.PersonalAssistant.Functions.getLocation import getLocationTool
	from Flows.PersonalAssistant.Functions.getTravelDirections import getTravelDirectionsTool
	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocsTool
	from Flows.PersonalAssistant.Functions.getLatestNews import getLatestNewsTool, getNewsDetailsTool
	from Flows.PersonalAssistant.Functions.readEmail import readEmailTool, writeEmailTool
	from Flows.PersonalAssistant.Functions.readWebPage import readWebPageTool
	from Flows.PersonalAssistant.Functions.searchArxiv import searchArxivTool
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProvidersTool, getUnwatchedGoodWatchableMoviesTool
	from Flows.PersonalAssistant.Resources.ResourceTools import getResourceTools
	from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool

	tools = []

	tools.append(createJiraIssueTool())
	tools.append(findInfoInDocsTool())

	tools.append(getCurrentWeatherTool())
	tools.append(getDateAndTimeTool())
	tools.append(getLatestNewsTool())
	tools.append(getLocationTool())
	tools.append(getMyJiraIssuesTool())
	tools.append(getNewsDetailsTool())
	tools.append(getTodaysCalendarEventsTool())
	tools.append(getTravelDirectionsTool())
	tools.append(getUnwatchedGoodWatchableMoviesTool())
	tools.append(getWatchProvidersTool())

	tools.append(readEmailTool())
	tools.append(readWebPageTool())
	tools.append(search_wikipedia_tool())
	tools.append(searchArxivTool())
	tools.append(writeEmailTool())

	for tool in getResourceTools():
		tools.append(tool)

	return tools
