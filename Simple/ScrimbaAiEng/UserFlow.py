from dotenv import load_dotenv # type: ignore
load_dotenv()

def getLlm():
	import os
	llmType = os.getenv('LlmType')
	if not llmType:
		import sys
		sys.exit("*** ERROR: You need to set the environment variable LlmType, for example in an .env file.")
	if llmType == "OpenAi":
		from langchain_openai import ChatOpenAI # type: ignore
		model = "gpt-3.5-turbo"
		print(" *** Using OpenAI with model " + model + ".")
		return ChatOpenAI(model=model)
	
	from langchain_community.chat_models import ChatOllama # type: ignore
	localModel = os.getenv("LocalModel")
	print(" *** Using Ollama with model " + localModel + ".")
	return ChatOllama(model=localModel)

def combineDocs(docs):
	return "\n\n".join(doc.page_content for doc in docs)

def askQuestion(question, conversationHistory):
	from SplitEmbedStore import getVectorStore
	from langchain_core.prompts import PromptTemplate
	from langchain_core.output_parsers.string import StrOutputParser
	from langchain_core.runnables import RunnableSequence, RunnablePassthrough
	llm = getLlm()

	standaloneQuestionTemplate = 'Given a question, convert it to a standalone question. You may also use the conversation history, if any, to improve on the standalone question. Question: {question}. Conversation history: {conversation_history}. Standalone question:'
	standaloneQuestionPrompt = PromptTemplate.from_template(standaloneQuestionTemplate)
	standaloneQuestionChain = RunnableSequence(standaloneQuestionPrompt, llm, StrOutputParser())

	vectorStoreRetriever = getVectorStore().as_retriever()
	retrieverChain = RunnableSequence(lambda x: x["standalone_question"], vectorStoreRetriever, combineDocs)
	
	answerTemplate = "Given a question and a context, provide an answer to the user. " + \
		"You may also use the conversation history, if any." + \
 		"We want this answer to be friendly, " + \
 		"only answer from the context provided and never make up answers, " + \
 		"apologise if you do not know the answer and advise the " + \
 		"user to email help@scrimba.com. Do not mention the context in the answer, since the user does not know about that. " + \
		"Question: {question}. Context: {context}. Conversation history: {conversation_history}. Answer: "
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

# question = 'What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.'
conversationHistory = ""
for i in range(5):
	question = input("How can I help you?")
	answer = askQuestion(question, conversationHistory)
	conversationHistory += "User: " + question + ". "
	conversationHistory += "AI: " + answer + ". "
	print(" *** Answer: ", answer)
