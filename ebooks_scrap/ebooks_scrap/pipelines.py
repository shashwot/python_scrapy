from openpyxl import Workbook
from pymongo import MongoClient
from itemadapter import ItemAdapter


class EbooksScrapPipeline:

    # FOR EXCEL SHEET

    # def open_spider(self, spider):
    #     self.workbook = Workbook()
    #     self.sheet = self.workbook.active
    #     self.sheet.title = "ebooks"
    #     self.sheet.append(spider.cols)

    # def process_item(self, item, spider):
    #     self.sheet.append([ item['title'], item['price'] ])
    #     return item

    # def close_spider(self, spider):
    #     self.workbook.save("ebooks.xlsx")


    # For DB (MONGO)
    def open_spider(self, spider):
        self.client = MongoClient(host="localhost",
                        port=27017, 
                        username="root", 
                        password="example",
                        authSource="admin"
                    )
        self.collection = self.client.get_database("ebook").get_collection("travel")

    def process_item(self, item, spider):
        self.collection.insert_one(
            # {
            #     "title": item['title'],
            #     "price": item['price']
            # }
            # Can also be written as :
            ItemAdapter(item).asdict()
        )
        return item
    
    def close_spider(self, spider):
        self.client.close()

