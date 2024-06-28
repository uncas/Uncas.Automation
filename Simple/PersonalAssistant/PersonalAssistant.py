from Logger import Logger
from dotenv import load_dotenv # type: ignore
load_dotenv()
import os
logger = Logger()

def getLlm():
	llmType = os.getenv('LlmType')
	model = os.getenv("LlmModel")
	if not llmType:
		import sys
		sys.exit("*** ERROR: You need to set the environment variable LlmType, for example in an .env file.")
	logger.info("Using " + llmType + " with model " + model + ".")
	if llmType == "OpenAi":
		from langchain_openai import ChatOpenAI # type: ignore
		return ChatOpenAI(model=model)
	
	from langchain_community.chat_models import ChatOllama # type: ignore
	return ChatOllama(model=model)

def combineDocs(docs):
	return "\n\n".join(doc.page_content for doc in docs)

def askQuestion(question, conversationHistory):
	logger.debug("A")
	from EmbeddingVectorStore import getVectorStore
	logger.debug("B")
	from langchain_core.prompts import PromptTemplate
	logger.debug("C")
	from langchain_core.output_parsers.string import StrOutputParser
	logger.debug("D")
	from langchain_core.runnables import RunnableSequence, RunnablePassthrough
	logger.debug("E")
	llm = getLlm()
	logger.debug("F")
	standaloneQuestionTemplate = "Given a question, convert it to a standalone question. " + \
		"You may also use the conversation history, if any, to improve on the standalone question. " + \
		"Question: {question}. Conversation history: {conversation_history}. Standalone question:"
	logger.debug(standaloneQuestionTemplate)
	standaloneQuestionPrompt = PromptTemplate.from_template(standaloneQuestionTemplate)
	standaloneQuestionChain = RunnableSequence(standaloneQuestionPrompt, llm, StrOutputParser())

	vectorStoreRetriever = getVectorStore(logger).as_retriever()
	retrieverChain = RunnableSequence(lambda x: x["standalone_question"], vectorStoreRetriever, combineDocs)
	
	import datetime
	answerTemplate = "Given a question and a context, provide an answer to the user. " + \
		"You may also use the conversation history, if any." + \
 		"We want this answer to be friendly, " + \
 		"only answer from the context provided and never make up answers, " + \
 		"apologise if you do not know the answer. " + \
 		"Do not mention the context in the answer, since the user does not know about that. " + \
		"The current date and time is " + str(datetime.datetime.now()) + ". " + \
		"Question: {question}. Context: {context}. Conversation history: {conversation_history}. Answer: "
	logger.debug(answerTemplate)
	answerPrompt = PromptTemplate.from_template(answerTemplate)
	answerChain = RunnableSequence(answerPrompt, llm, StrOutputParser())

	chain = RunnableSequence(
		{
        	"standalone_question": standaloneQuestionChain,
        	"original_input": RunnablePassthrough()
    	},
		{
        	"context": retrieverChain,
        	"question": lambda previousOutput: previousOutput["original_input"]["question"],
			"conversation_history": lambda previousOutput: previousOutput["original_input"]["conversation_history"]
    	},
		answerChain
	)

	result = chain.invoke({ "question": question, "conversation_history": conversationHistory })
	return result

if __name__ == "__main__":
	conversationHistory = ""
	for i in range(5):
		question = input("How can I help you?")
		answer = askQuestion(question, conversationHistory)
		conversationHistory += "User: " + question + ". "
		conversationHistory += "AI: " + answer + ". "
		print("Answer: ", answer)
