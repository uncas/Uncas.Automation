# Function that extracts data from API
def get_data(object_name):
    return ["dummy data", "b", "c", "d", "e", "e", "e", "e"]

# Import StructuredTool and ChatOpenAI needed for creating the agent based on GPT-4
from langchain.tools.base import StructuredTool

#from langchain.chat_models import ChatOpenAI
#chat = ChatOpenAI(model_name="gpt-4",temperature=0.2)

from langchain_community.chat_models import ChatOllama
chat = ChatOllama(model="llama3", temperature=0)

# Turn the get_data function into a new function that receives text and returns text and create a tool out of the new function
from typing import Optional

def get_shopify_insight(shopify_object: Optional[str] = None) -> str:
    """Tool that counts the number of items for a given Shopify data object. Valid shopify_objects include "Customer", "Order", "Product" and "Webhook"."""
    object_name = (shopify_object or "Order")
    data = get_data(object_name)
    return str(len(data))

shopify_insights_tool = StructuredTool.from_function(get_shopify_insight)
     
# We can now call the tool and count items returned as a string
shopify_insights_tool('Customer')

# Create the agent based on the tool and the chatmodel
from langchain.agents import initialize_agent, AgentType
tools = [shopify_insights_tool]
agent_chain = initialize_agent(tools, 
                               chat, 
                               agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
                               verbose=True)
     
# Run the agent
agent_chain.invoke("How many orders are there in the Shopify store?")
