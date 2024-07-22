# Model here: https://huggingface.co/gpt2

Gpt2Path = "../../public/LLMs/Gpt2Model"

def generateText(model, input):
	from transformers import pipeline
	generator = pipeline('text-generation', model=model)
	result = generator(input, max_length=100, num_return_sequences=5)
	return result[0]["generated_text"]

# Not very good, but funny...

if __name__ == "__main__":
	input = "What is the big bang?"
	print(generateText(Gpt2Path, input))
