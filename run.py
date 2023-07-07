from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import json

# load .env file
load_dotenv()

PROXY = os.getenv("PROXY")


def write_to_jsonl(filename, data):
    with open(filename, 'a', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class Scraping:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = os.getenv("INPUT_URL")
        self.driver.get(self.url)
        self.data = []

    def get_data(self):
        while True:
            quotes = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="quotesPlaceholder"]/div[@class="quote"]')))
            print(len(quotes))
            for quote in quotes:
                quote_data = {'text': "", 'by': "", 'tags': []}
                quote_data['text'] = quote.find_element(by=By.XPATH, value='./span[@class="text"]').text.strip('“').strip('”')
                quote_data['by'] = quote.find_element(by=By.XPATH, value='.//small[@class="author"]').text
                quote_tags = quote.find_elements(by=By.XPATH, value='./div[@class="tags"]/a')
                for tag in quote_tags:
                    quote_data['tags'].append(tag.text)
                print(quote_data)
                self.data.append(quote_data)
            #if next cant be clicked it means that's last page
            try:
                self.driver.find_element(By.XPATH, '//li[@class="next"]/a').click()
            except:
                write_to_jsonl(os.getenv("OUTPUT_FILE"), self.data)
                break
            #self.options = self.driver.find_elements_by_xpath('//ul[@aria-expanded="true"]/li')


Scraping = Scraping()
Scraping.get_data()