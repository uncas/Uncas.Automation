from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough

llm = ChatOllama(model="llama3", temperature=0)

punctuationTemplate = "Given a sentence, add punctuation where needed. sentence: {sentence} sentence with punctuation: "
punctuationPrompt = PromptTemplate.from_template(punctuationTemplate)
punctuationChain = RunnableSequence(punctuationPrompt, llm, StrOutputParser())

grammarTemplate = "Given a sentence, correct the grammar. sentence: {punctuated_sentence} sentence with correct grammar: "
grammarPrompt = PromptTemplate.from_template(grammarTemplate)
grammarChain = RunnableSequence(grammarPrompt, llm, StrOutputParser())

translationTemplate = "Given a sentence, translate it into {language}. sentence: {grammatically_correct_sentence}. translated sentence: "
translationPrompt = PromptTemplate.from_template(translationTemplate)
translationChain = RunnableSequence(translationPrompt, llm, StrOutputParser())

chain = RunnableSequence(
	{
        "punctuated_sentence": punctuationChain,
        "original_input": RunnablePassthrough()
    },
    {
        "grammatically_correct_sentence": grammarChain,
        "language": lambda original_input: original_input["original_input"]["language"]
    },
	translationChain
)

response = chain.invoke({
    "sentence": 'i dont liked mondays',
    "language": 'french'
})

print(response)
