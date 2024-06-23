# Started from https://github.com/rabbitmetrics/langchain-agents-explained

#from langchain.chat_models import ChatOpenAI
#chat = ChatOpenAI(model_name="gpt-4",temperature=0.2)

from langchain_community.chat_models import ChatOllama
chat = ChatOllama(model="llama3", temperature=0)

# Function that extracts data from API
def get_data(object_name):
    return ["dummy data", "b", "c", "d", "e", "e", "e", "e"]

# Turn the get_data function into a new function that receives text and returns text and create a tool out of the new function
from typing import Optional
def get_shopify_insight(shopify_object: Optional[str] = None) -> int:
    """Tool that counts the number of items for a given Shopify data object. Valid shopify_objects include "Customer", "Order", "Product" and "Webhook"."""
    object_name = (shopify_object or "Order")
    data = get_data(object_name)
    return len(data)

from langchain.tools.base import StructuredTool
shopify_insights_tool = StructuredTool.from_function(get_shopify_insight)
     
# We can now call the tool and count items returned as a string
#print(shopify_insights_tool.invoke('Customer'))

# Create the agent based on the tool and the chatmodel
tools = [shopify_insights_tool]

from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(chat, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({"input": "How many orders are in the Shopify store?"})

print(result)