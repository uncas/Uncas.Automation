# Started from https://github.com/rabbitmetrics/langchain-agents-explained

def askAgent(tools, question):
    from langchain import hub
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_community.chat_models import ChatOllama
    #from langchain.chat_models import ChatOpenAI
    #chat = ChatOpenAI(model_name="gpt-4",temperature=0.2)
    chat = ChatOllama(model="llama3", temperature=0)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(chat, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)
    return agent_executor.invoke({"input": question})

def askRealAgent(question):
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    #print(wikipedia.run("HUNTER X HUNTER"))
    tools = [wikipedia]
    return askAgent(tools, question)

input = input("Question: ")
print(askRealAgent(input))









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
