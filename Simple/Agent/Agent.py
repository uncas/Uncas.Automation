# Started from https://github.com/rabbitmetrics/langchain-agents-explained

from typing import Any, Dict
from langchain_core.tools import BaseTool
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_end(self, result: LLMResult, **kwargs) -> Any:
        print(f"My custom handler, response: {result}, kwargs: {kwargs}")

def askAgent(tools : list[BaseTool], question : str) -> Dict[str, Any]:
    from langchain import hub
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_openai import ChatOpenAI
    chat = ChatOpenAI(model="gpt-4o-mini",temperature=0.2, callbacks=[MyCustomHandler()])
    #from langchain_community.chat_models import ChatOllama
    #chat = ChatOllama(model="llama3", temperature=0)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(chat, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, max_iterations=5)
    return agent_executor.invoke({"input": question})

def askRealAgent(question : str) -> Dict[str, Any]:
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    from langchain_community.agent_toolkits.load_tools import load_tools
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    #print(wikipedia.run("HUNTER X HUNTER"))

    #from langchain_community.utilities import OpenWeatherMapAPIWrapper
    #weather = OpenWeatherMapAPIWrapper()
    #print(weather.run("London,GB"))

    tools = load_tools(["openweathermap-api"])
    tools.append(wikipedia)

    return askAgent(tools, question)

question = input("Question: ")
print(askRealAgent(question)["output"])









def askDemoAgent(question):
    def get_shopify_data(object_name):
        return ["dummy data", "b", "c", "d", "e", "e", "e", "e"]
    # Turn the get_shopify_data function into a new function that receives text and returns text and create a tool out of the new function
    from typing import Optional
    def get_shopify_insight(shopify_object: Optional[str] = None) -> int:
        """Tool that counts the number of items for a given Shopify data object. Valid shopify_objects include "Customer", "Order", "Product" and "Webhook"."""
        object_name = (shopify_object or "Order")
        data = get_shopify_data(object_name)
        return len(data)
    from langchain.tools.base import StructuredTool
    shopify_insights_tool = StructuredTool.from_function(get_shopify_insight)
    # We can now call the tool and count items returned as a string
    #print(shopify_insights_tool.invoke('Customer'))
    shopify_tools = [shopify_insights_tool]
    return askAgent(shopify_tools, question)

#print(askDemoAgent("How many orders are in the Shopify store?"))
