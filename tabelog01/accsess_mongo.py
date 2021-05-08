from pymongo import MongoClient

client = MongoClient('localhost', 28017)
db = client['scraping_tabelog']  
collection = db['items']

for i, item in enumerate(collection.find()):
    print(item)
    break