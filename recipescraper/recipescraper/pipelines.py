# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from json import dumps


class RecipescraperPipeline:
    
    def __init__(self):
        self.conn = sqlite3.connect('recipes.db')
        self.curs = self.conn.cursor()
        self.create_table()
    
    
    def create_table(self):
        self.curs.execute("""DROP TABLE IF EXISTS food_recipes""")
        self.curs.execute("""CREATE TABLE food_recipes(
            name TEXT,
            ingredients TEXT, 
            direction TEXT
                )""")
            
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.curs.execute("""INSERT OR IGNORE INTO food_recipes VALUES(?,?,?)""",
                          (item['Name'], 
                           dumps(item['Ingredients']), 
                           dumps(item['Direction'])
                           ))
        self.conn.commit()