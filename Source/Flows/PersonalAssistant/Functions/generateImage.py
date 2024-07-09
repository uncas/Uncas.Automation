def generateImage(prompt):
	from openai import OpenAI
	client = OpenAI()
	return client.images.generate(prompt = prompt, model = "dall-e-3", size = "1792x1024", style = "natural")
	# style: can be natural or vivid
	#return client.images.generate(prompt = prompt, model = "dall-e-2", response_format = "b64_json", size = "256x256")

def editBottomHalfOfImage(imageFile, prompt):
	imageWithBottomHalfTransparent = imageFile
	
	
	from openai import OpenAI
	client = OpenAI()
	return client.images.edit(image = imageFile, prompt = prompt)

def makePartOfImageTransparent(originalFilePath, newFilePath, xFraction, yFraction, widthFraction, heightFraction):
	from PIL import Image
	image = Image.open(originalFilePath)
	width, height = image.size
	print(width, height)
	x, y = int(width * xFraction), int(height * yFraction)
	width, height = int(width * widthFraction), int(height * heightFraction)
	print(x, y, width, height)
	rgbaTransparent = (0, 0, 0, 0)
	transparentMask = Image.new("RGBA", (width, height), rgbaTransparent)
	image.paste(transparentMask, (x, y), transparentMask)
	image.save(newFilePath)
