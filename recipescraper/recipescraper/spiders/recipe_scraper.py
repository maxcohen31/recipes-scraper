import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from sys import path
from scrapy.loader import ItemLoader
from csv import DictWriter
from json import loads
from time import sleep

# fixing 'ModuleNotFoundError' error
path.append('/home/maxcohen/Desktop/foodscraper/recipescraper')
from recipescraper.items import RecipescraperItem


class SpiderFood(scrapy.Spider):
    name = 'spider_food'
    
    start_urls = [
        'https://www.food.com/recipe/all/editor-pick?pn='
    ]
    
    allowed_domains = [
        'food.com'
        ]
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    
    # being gentle on the site
    settings = {
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
    }
    
    def __init__(self):
        
        print('[+]Creating the csv file...[+]')
        sleep(1)
        try:
            with open('food.csv', 'w') as food:
                food.write('Name,Ingredients,Direction\n')
                print('[+]csv file successfully created![+]')
                sleep(0.5)
        except OSError as e:
            print(f'csv file already exists! --> {e}')
            sleep(0.5)
            
    # spider's entry point
    def start_requests(self):
        # dealing with 'Load More' button
        for page in range(1, 5):
            next_page = f"{self.start_urls[0]+str(page)}"
            yield Request(
                url=next_page,
                headers=self.headers,
                callback=self.parse
            )
            
    def parse(self, response):
        
        print('\n*****PARSING*****\n')
        
        json_items = loads(response.xpath("//script[@type='application/ld+json']/text()").get())
        # loop over the links
        links = [json_items['itemListElement'][i]['url'] for i in range(8)]
        
        for link in links:
            yield Request(url=link, headers=self.headers, callback=self.fetch_details)
            
    def fetch_details(self, response):
        
        print("\n*****EXTRACTING DATA******\n")
        
        # loading the response to a json dict
        res = loads(response.xpath("//script[@type='application/ld+json']/text()").get())
        instructions = res['recipeInstructions']
        list_of_instructions = []
        counter = 0
        while len(instructions) > counter:
            list_of_instructions.append(instructions[counter]['text'])
            counter += 1
        
        name = res['name']
        ingredients = res['recipeIngredient']

        features = {
            'Name': name,
            'Ingredients': ingredients,
            'Direction': list_of_instructions
        }
        
        # writing the data into a csv file
        with open('food.csv', 'a') as food_csv:
            csv_writer = DictWriter(food_csv, fieldnames=features.keys())
            csv_writer.writerow(features)
        
        
# main driver
if __name__ == '__main__':
    
    process = CrawlerProcess()
    process.crawl(SpiderFood)
    process.start()