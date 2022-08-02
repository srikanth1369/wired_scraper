# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os


class WiredPipeline:

    DB_URI = os.environ.get("SCRAPERS_DB_URL", "mongodb://localhost:27017")


    def __init__(self):
        self.conn = pymongo.MongoClient(self.DB_URI) # made data base connetion.
        db = self.conn["wired"]  # database_name: medium.
        self.collection = db["wired_tb"] # table name: medium_tb and we are  strong properties of the table insdie collection

    def process_item(self, item, spider):
        item = dict(item)
        self.collection.insert_one(item)
        item.pop('_id')
        return item

