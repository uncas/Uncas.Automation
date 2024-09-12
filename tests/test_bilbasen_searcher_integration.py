import unittest

from uncas_automation.Services.Google.GoogleSheetsService import replace_data_in_sheet
from uncas_automation.Services.bilbasen_searcher import BilbasenSearcher

class CarsInDkIntegrationTests(unittest.TestCase):
	#def test_get_electric_cars_in_denmark(self):
	#	searcher = BilbasenSearcher()
	#	queries = ["Aiways", "Audi", "BMW", "BYD", "Citroën", "Ford", "Honda", "Hyundai", "Mazda", "MG4", "MG", "Nissan", "Opel", "Peugeot", "Renault", "Skoda", "Tesla", "Toyota", "Volvo", "VW"]
	#	for query in queries:
	#		cars = searcher.search(query)
	#		print("Number of cars: ", len(cars), " for ", query)
	
	@unittest.skip("Skip")
	def test_parse_cars_from_search_result_html(self):
		searcher = BilbasenSearcher()
		file = "tests/data/bilbasen_search_result.html"
		with open(file, "r") as fileStream:
			html = fileStream.read()
		cars = searcher.parse_cars_from_search_result_html(html)
		self.assertEqual(len(cars), 30)
		car = cars[0]
		self.assertEqual(car["make"], "Kia")
		self.assertEqual(car["model"], "e-Niro")
		features = car["features"]
		self.assertIn("apple carplay", features)
	
	@unittest.skip("Skip")
	def test_parse_car_from_car_page_html(self):
		searcher = BilbasenSearcher()
		file = "tests/data/bilbasen_car_page.html"
		with open(file, "r") as fileStream:
			html = fileStream.read()

		car = searcher.parse_car_from_car_page_html(html)

		print(car["url"])
		print("FACTS AND INFO:")
		for item in car["facts_and_info"]:
			print(item["key"], "=", item["value"])
		print("EQUIPMENT:")
		for equipment in car["equipment"]:
			print(equipment)

	def test_import_cars_to_sheet(self):
		google_account_alias = "olelynge"
		document_id = "10EaLc2LSgLBrfsEzER3NVw563IUttojQ13WpMs-UEXE"
		sheet_id = "BilbasenSearch"

		searcher = BilbasenSearcher()
		cars = searcher.get_cars_from_search_result_files()
		print("Number of cars: ", len(cars))
		sorted_cars = sorted(cars, key=lambda d: d['make'] + d['model'] + d['variant'])
		fields = ["Make", "Model", "Variant", "Date", "Mileage", "Price", 
			"Range", "Fuel", "Location", "Features", "Link", "Modelår",
			"Batterikapacitet", "Energiforbrug", 
			"Hjemmeopladning AC", "Hurtig opladning DC", "Ydelse", 
			"Acceleration", "Tophastighed", "Type", "Bagagerumsstørrelse", 
			"Bredde", "Længde", "Højde", "Nypris", "Km_per_liter", "Box_volume", "Periodisk afgift", "Vægt?"]
		data = [fields]
		for car in sorted_cars:
			car["features"] = ", ".join(car["features_list"])
			car_data = []
			for field in fields:
				if field.lower() in car:
					car_data.append(car[field.lower()])
				else:
					car_data.append("")
			data.append(car_data)
		replace_data_in_sheet(google_account_alias, document_id, sheet_id, data)