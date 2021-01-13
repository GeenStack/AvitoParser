from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os


#Класс AvitoParser - парсит объявления с применением Chrome Webdriver в 
#безголовом режиме. Для работы распакуйте Chrome Webdriver в рабочую директорию вашего проекта.
#Класс протестирован на парсинге популярных товаров, предназначен для своевременного оповещения о новых объявлениях
#и работает абсолютно с любыми ссылками
class AvitoParser:
	def __init__(self, URL):
		self.URL = URL


	def get_page_source(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--no-sandbox")
		driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),chrome_options = chrome_options)
		driver.get(self.URL)
		html = driver.page_source
		driver.close()
		return BeautifulSoup(html, 'html.parser')


	def get_blocks(self):
		#Получить список обявлений со страницы
		html = self.get_page_source()
		container = html.select("div.iva-item-body-NPl6W")
		return container


	def get_url_from_block(self, block):
		#Получить ссылку на объявление
		url = block.find("a")
		return "https://www.avito.ru" + url["href"]


	def get_price_from_block(self, block):
		#Получить цену объявления
		price = block.findAll("meta")
		price = price[1]["content"]
		return price


	def get_date_from_block(self, block):
		#Получить дату объявлеия
		date = block.select_one("div.date-text-2jSvU")
		return date.text


	def get_pagination_limit(self):
		#Подготовка пагинации. Возвращает количество страниц
		html = self.get_page_source()
		pagination_limit_block = html.select("span.pagination-item-1WyVp")
		return int(pagination_limit_block[-2].text) 


	def get_dataset(self):
		#Получить датасет всех объявлений по ссылке. Датасет - список объявлений,
		#где каждое объявление представлено словарем в формате 
		#{"block_url":block_url, "block_price":block_price, "block_date":block_date}
		data_set = []
		pagination_limit = self.get_pagination_limit()
		for page in range(1, pagination_limit + 1):
			self.URL += "&p={}".format(str(page))
			container = self.get_blocks()
			for block in container:
				block_url = self.get_url_from_block(block)
				block_price = self.get_price_from_block(block)
				block_date = self.get_date_from_block(block)
				data_set.append({"block_url":block_url, "block_price":block_price, "block_date":block_date})
		return data_set

	#Вернуть датасет объявлений с первой страницы
	def get_first_page_dataset(self):
		data_set = []
		container = self.get_blocks()
		for block in container:
				block_url = self.get_url_from_block(block)
				block_price = self.get_price_from_block(block)
				block_date = self.get_date_from_block(block)
				data_set.append({"block_url":block_url, "block_price":block_price, "block_date":block_date})
		return data_set


