import csv
import unittest

from dotenv import load_dotenv

from uncas_automation.Services.eletric_cars_service import get_electric_cars_in_denmark

class CarsInDkIntegrationTests(unittest.TestCase):
	def test_get_electric_cars_in_denmark(self):
		load_dotenv(override = True)
		cars = get_electric_cars_in_denmark()
		print(len(cars))
		print(cars[0])
		csv_file = "Output/cars.csv"
		with open(csv_file, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = cars[0].keys())
			writer.writeheader()
			for car in cars:
				writer.writerow(car)

	