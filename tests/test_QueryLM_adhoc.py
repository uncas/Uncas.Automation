from uncas_automation.Tools.Ai.QueryLM import generateResponse, getModel, getTokenizer

def testQueryLM():
	modelFolder = "../../public/LLMs/dolly-v2-3b/"
	model = getModel(modelFolder)
	tokenizer = getTokenizer(modelFolder)

	# Sample similar to: "Excited to announce the release of Dolly, a powerful new language model from Databricks! #AI #Databricks"
	result = generateResponse("Write a tweet announcing Dolly, a large language model from Databricks.", model=model, tokenizer=tokenizer)
	print(result)

	result = generateResponse("Describe the big bang model to a 6 year old.", model=model, tokenizer=tokenizer)
	print(result)

	result = generateResponse("What are the most popular cat races?", model=model, tokenizer=tokenizer, max_new_tokens=2000)
	print(result)
