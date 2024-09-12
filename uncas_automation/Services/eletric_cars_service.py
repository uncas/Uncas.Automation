import urllib.request
import certifi

from bs4 import BeautifulSoup 

def get_electric_cars_in_denmark():
	url = "https://blog.bilbasen.dk/elbiler-i-danmark-2021-353560/"
	userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
	req = urllib.request.Request(url)
	req.add_header('User-Agent', userAgent)
	cafile= certifi.where()
	r = urllib.request.urlopen(req, cafile=cafile)
	html = r.read()
	html_text = html.decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	#from easai.assistant.assistant import Assistant, run_assistant, get_user_prompt
	#assistant = Assistant()
	#example = "{'Make': 'Aiways', 'Model': 'U5', 'Price': '325.000 kr.', 'Km': '410 km'}"
	#messages = [get_user_prompt("From the following html context I want you to provide BeautifulSoup (from the python library bs4) code that can help me parse the html and get a list of items with the following properties: make, model, price, km. For example: " + example + ". Here is the HTML: " + html_text)]
	#result = run_assistant(messages=messages, assistant=assistant)
	#print(result)
	vehicle_sections = soup.find_all('h3')
	vehicles = []
	for vehicle in vehicle_sections:
		vehicle_name = vehicle.get_text(strip=True)
		# Split the vehicle name into make and model (assuming the first word is make and the rest is model)
		parts = vehicle_name.split(' ', 1)
		make = parts[0]
		model = parts[1] if len(parts) > 1 else ''
		# Try to find the next <p> tags to get price and km
		details = vehicle.find_next_siblings('p', limit=2)
		if details and len(details) == 2:
			price_text = details[0].get_text(strip=True)
			km_text = details[1].get_text(strip=True)
			# Extract the price and km
			price = price_text.replace('Pris:', '').strip()
			km = km_text.replace('Rækkevidde:', '').strip()
			prices = price.split('/')
			kms = km.split('/')
			for variant_index in range(len(prices)):
				price = prices[variant_index].replace(".", "").replace("kr", "").strip()
				km = kms[variant_index].replace("km", "").strip()
				vehicles.append({'Make': make, 'Model': model, 'Km': km, 'Price': price})
	return vehicles
#	return soup.get_text()
