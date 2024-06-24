def askQuestion(question):
	from SplitEmbedStore import getVectorStore
	from langchain_community.chat_models import ChatOllama
	from langchain_core.prompts import PromptTemplate
	from langchain_core.output_parsers.string import StrOutputParser
	llm = ChatOllama(model="llama3", temperature=0)
	vectorStoreRetriever = getVectorStore().as_retriever()
	standaloneQuestionTemplate = 'Given a question, convert it to a standalone question. Question: {question}. Standalone question:'
	standaloneQuestionPrompt = PromptTemplate.from_template(standaloneQuestionTemplate)
	chain = standaloneQuestionPrompt.pipe(llm).pipe(StrOutputParser()).pipe(vectorStoreRetriever)
	response = chain.invoke({ "question": question })
	return response

response = askQuestion('What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.')
print(response)



	#tweetTemplate = 'Generate a promotional tweet for a product, from this product description: {productDesc}'
	#tweetPrompt = PromptTemplate.from_template(tweetTemplate)
	#print(tweetPrompt)
