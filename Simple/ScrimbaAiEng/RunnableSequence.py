from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnableSequence

llm = ChatOllama(model="llama3", temperature=0)

punctuationTemplate = "Given a sentence, add punctuation where needed. sentence: {sentence} sentence with punctuation:"
punctuationPrompt = PromptTemplate.from_template(punctuationTemplate)

grammarTemplate = "Given a sentence correct the grammar. sentence: {punctuated_sentence} sentence with correct grammar: "
grammarPrompt = PromptTemplate.from_template(grammarTemplate)

chain = RunnableSequence(
    punctuationPrompt,
    llm,
    StrOutputParser(),
#	lambda prevResult: print("D: ", prevResult),
#    {punctuated_sentence: prevResult => prevResult},
    grammarPrompt,
    llm,
    StrOutputParser())

response = chain.invoke({
    "sentence": 'i dont liked mondays',
    "language": 'french'
})

print(response)