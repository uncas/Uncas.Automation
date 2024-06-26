from dotenv import load_dotenv # type: ignore
load_dotenv()

def getLlm():
	import os
	llmType = os.getenv('LlmType')
	if llmType == "OpenAi":
		from langchain_openai import ChatOpenAI # type: ignore
		model = "gpt-3.5-turbo"
		print(" *** Using OpenAI with model " + model + ".")
		return ChatOpenAI(model=model, temperature=0)
	
	from langchain_community.chat_models import ChatOllama # type: ignore
	localModel = os.getenv("LocalModel")
	print(" *** Using Ollama with model " + localModel + ".")
	return ChatOllama(model=localModel, temperature=0)

def combineDocs(docs):
	return "\n\n".join(doc.page_content for doc in docs)

def askQuestion(question):
	from SplitEmbedStore import getVectorStore
	from langchain_core.prompts import PromptTemplate
	from langchain_core.output_parsers.string import StrOutputParser
	from langchain_core.runnables import RunnableSequence, RunnablePassthrough
	llm = getLlm()

	standaloneQuestionTemplate = 'Given a question, convert it to a standalone question. Question: {question}. Standalone question:'
	standaloneQuestionPrompt = PromptTemplate.from_template(standaloneQuestionTemplate)
	standaloneQuestionChain = RunnableSequence(standaloneQuestionPrompt, llm, StrOutputParser())

	vectorStoreRetriever = getVectorStore().as_retriever()
	retrieverChain = RunnableSequence(lambda x: x["standalone_question"], vectorStoreRetriever, combineDocs)
	
	answerTemplate = "Given a question and a context, provide an answer to the user. " + \
 		"We want this answer to be friendly, " + \
 		"only answer from the context provided and never make up answers, " + \
 		"apologise if you do not know the answer and advise the " + \
 		"user to email help@scrimba.com. Do not mention the context in the answer, since the user does not know about that. " + \
		"Question: {question}. Context: {context}. Answer: "
	answerPrompt = PromptTemplate.from_template(answerTemplate)
	answerChain = RunnableSequence(answerPrompt, llm, StrOutputParser())

	chain = RunnableSequence(
		{
        	"standalone_question": standaloneQuestionChain,
        	"original_input": RunnablePassthrough()
    	},
		{
        	"context": retrieverChain,
        	"question": lambda previousOutput: previousOutput["original_input"]["question"]
    	},
		answerChain
	)

	result = chain.invoke({ "question": question })
	return result

response = askQuestion('What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.')
print(" *** Answer: ", response)
