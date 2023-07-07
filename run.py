from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import json
from time import sleep


load_dotenv()


def write_to_jsonl(filename, data):
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'a', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class Scraping:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        #with proxy code doesnt work.
        #chrome_options.add_argument(f'--proxy-server={os.getenv("PROXY")}')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = os.getenv("INPUT_URL")
        self.data = []

    def get_data(self):
        quotes = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="quotesPlaceholder"]/div[@class="quote"]')))
        for quote in quotes:
            quote_data = {'text': "", 'by': "", 'tags': []}
            quote_data['text'] = quote.find_element(by=By.XPATH, value='./span[@class="text"]').text.strip('“').strip('”')
            quote_data['by'] = quote.find_element(by=By.XPATH, value='.//small[@class="author"]').text
            quote_tags = quote.find_elements(by=By.XPATH, value='./div[@class="tags"]/a')
            for tag in quote_tags:
                quote_data['tags'].append(tag.text)
            self.data.append(quote_data)

    def next_page(self):
        #delay clicking button - more human behaviour
        #website doesnt block program without it so if performance is an issue it can be deleted
        sleep(1)
        try:
            self.driver.find_element(By.XPATH, '//li[@class="next"]/a').click()
        except:
            print('That was the last page.')
            return False

    def main(self):
        self.driver.get(self.url)
        print('First page.')
        while True:
            self.get_data()
            if self.next_page() == False:
                write_to_jsonl(os.getenv("OUTPUT_FILE"), self.data)
                break
            print('Next page.')


Scraping = Scraping()
Scraping.main()