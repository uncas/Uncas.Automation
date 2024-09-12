import datetime
import os
import sys
import time
import urllib.parse

import bs4
from easai.utils.local_cache import LocalCache

from uncas_automation.Services.web_page_reader import read_web_page_html

class BilbasenSearcher:
	def __init__(self):
		self.last_timestamp = None
		self.cache = LocalCache("Data/BilbasenCache.db")
		pass

	def search(self, query):
		encoded_query = urllib.parse.quote_plus(query)
		url = "https://www.bilbasen.dk/brugt/bil?fuel=3&free=" + encoded_query
		return self.search_url(url)

	def search_url(self, url):
		key = "search_bilbasen: " + url
		lifetimeSeconds = 3600 * 24
		html = self.cache.get_or_add_with_lifetime(key, lambda: self.do_search_url(url), lifetimeSeconds)
		return self.parse_cars_from_search_result_html(html)

	def parse_cars_from_search_result_html(self, html):
		soup = bs4.BeautifulSoup(html, 'html.parser')
		cars = soup.select("article[class*=Listing_listing__]")
		result = []
		for car in cars:
			link = car.select("a[class*=Listing_link__]")[0]["href"]
			make_model_div = car.select("div[class*=Listing_makeModel__]")[0]
			make_model = make_model_div.find("h3").text
			make = make_model.split(" ")[0]
			model = make_model.replace(make, "").strip()
			variant = make_model_div.text.replace(make_model, "")
			price = car.select("div[class*=Listing_price__]")[0].text.replace("kr.", "").replace(" ", "").replace(".", "").strip()
			details_items = car.select("ul[class*=ListingDetails_list__]")[0].find_all("li")
			date = None
			range = None
			mileage = None
			fuel = None
			km_per_liter = None
			for details_item in details_items:
				details_item_text = details_item.text.strip()
				if "km/l" in details_item_text:
					km_per_liter = details_item_text.replace("km/l", "").strip()
				elif "/" in details_item_text:
					date = details_item_text
				elif "km rækkevidde" in details_item_text:
					range = details_item_text.replace(" km rækkevidde", "").strip()
				elif "km" in details_item_text:
					mileage = details_item_text.replace(" km", "").replace(".", "").strip()
				else:
					fuel = details_item_text
			location = car.select("div[class*=Listing_location__]")[0].text
			description = car.select("div[class*=Listing_description__]")[0].text.lower()
			features_list = []
			if "apple carplay" in description:
				features_list.append("apple carplay")
			result.append({"make": make, "model": model, "variant": variant, "price": price, "date": date, "mileage": mileage, "range": range, "fuel": fuel, "location": location, "features_list": features_list, "link": link, "km_per_liter": km_per_liter})
		#pagination_next = soup.find("a", {"data-e2e": "pagination-next"})
		#if pagination_next is not None:
		#	pagination_next_disabled = pagination_next.has_attr("disabled")
		#	if pagination_next_disabled:
		#		return result
		#	next_page_url = pagination_next.get("href")
		#	if next_page_url is not None:
		#		next_page_url = "https://www.bilbasen.dk" + next_page_url
		#		result = result + self.search_url(next_page_url)
		return result

	def do_search_url(self, url) -> str:
		now_timestamp = datetime.datetime.now().timestamp()
		min_seconds_between_searches = 10
		if self.last_timestamp is not None:
			time_to_sleep = min_seconds_between_searches - (now_timestamp - self.last_timestamp)
			if time_to_sleep > 0:
				print("Sleeping for", str(time_to_sleep), " seconds")
				time.sleep(time_to_sleep)
		print("Searching bilbasen for: " + url)
		html = read_web_page_html(url)
		self.last_timestamp = datetime.datetime.now().timestamp()
		return html

	def parse_car_from_car_page_html(self, html) -> dict:
		soup = bs4.BeautifulSoup(html, 'html.parser')
		link = soup.find("meta", {"property": "og:url"})["content"]
		def get_expanded_and_collapsed(soup, css_class):
			return soup.find_all("tr", {"class": css_class}) + \
				   soup.find_all("tr", {"class": css_class + " collapsed-mode"})

		facts_and_info_rows = soup.find_all("tr", {"class": "bas-MuiTableRow-root bas-MuiCarFactsComponent-tableRowRoot facts-shown"})
		facts_and_info_rows+= soup.find_all("tr", {"class": "bas-MuiTableRow-root bas-MuiCarFactsComponent-tableRowRoot facts-collapsed"})
		facts_and_info_rows+= get_expanded_and_collapsed(soup, "bas-MuiTableRow-root bas-MuiCarModelInformationComponent-tableRowRoot facts-shown")
		facts_and_info_rows+= soup.find_all("tr", {"class": "bas-MuiTableRow-root bas-MuiCarModelInformationComponent-tableRowRoot facts-collapsed"})
		facts_and_info = []
		for detail_row in facts_and_info_rows:
			key = detail_row.find("th").text
			value = detail_row.find("td").text
			facts_and_info.append({ "key": key, "value": value })
		equipment_rows = get_expanded_and_collapsed(soup, "bas-MuiTableRow-root bas-MuiCarEquipmentComponent-equipmentRow equipment-shown")
		equipment = []
		for equipment_row in equipment_rows:
			equipment.append(equipment_row.find("th").text)
			equipment.append(equipment_row.find("td").text)
		return { "link": link, "facts_and_info": facts_and_info, "equipment": equipment }

	def get_htmls_from_files_in_folder(self, folder) -> list:
		htmls = []
		for file in os.listdir(folder):
			if not file.lower().endswith('.html'):
				continue
			with open(folder + "/" + file, "r") as fileStream:
				htmls.append(fileStream.read())
		return htmls

	def get_cars_from_search_result_files(self):
		folder = "../../../Downloads/car-research/bilbasen-search-results"
		htmls = self.get_htmls_from_files_in_folder(folder)
		cars_details = self.get_cars_from_car_page_files()
		terms_to_remove_from_values = [" cm"]
		cars = []
		for html in htmls:
			cars += self.parse_cars_from_search_result_html(html)
		for car in cars:
			matching_car_details = [car_detail for car_detail in cars_details if car_detail["link"] == car["link"]]
			if len(matching_car_details) > 0:
				car_details = matching_car_details[0]
				for fact_or_info in car_details["facts_and_info"]:
					value = fact_or_info["value"]
					for term in terms_to_remove_from_values:
						value = value.replace(term, "")
					car[fact_or_info["key"].lower()] = value
				for equipment in car_details["equipment"]:
					if not equipment.lower() in car["features_list"]:
						car["features_list"].append(equipment.lower())
				width = int(car["bredde"])
				length = int(car["længde"])
				height = int(car["højde"])
				car["box_volume"] = width * length * height / 100 / 100 / 100
		return cars

	def get_cars_from_car_page_files(self):
		folder = "../../../Downloads/car-research/bilbasen-car-pages"
		htmls = self.get_htmls_from_files_in_folder(folder)
		return [self.parse_car_from_car_page_html(html) for html in htmls]