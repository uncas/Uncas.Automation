def combineDocs(docs):
	return "\n\n".join(doc.page_content for doc in docs)

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
	docs = chain.invoke({ "question": question })
	answerTemplate = "Given a question and a context, provide an answer to the user. " + \
 		"We want this answer to be friendly, " + \
 		"only answer from the context provided and never make up answers, " + \
 		"apologise if you do not know the answer and advise the " + \
 		"user to email help@scrimba.com. Question: {question}. Context: {context}. Answer: "
	answerPrompt = PromptTemplate.from_template(answerTemplate)
	answerChain = answerPrompt.pipe(llm)
	context = combineDocs(docs)
	print(" *** Context: ", context)
	answer = answerChain.invoke({ "question": question, "context": context })
	return answer.content

response = askQuestion('What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.')
print(" *** Answer ", response)
