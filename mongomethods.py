import pymongo
import dns, os

client1 = pymongo.MongoClient(os.environ['MONGO'])

db1 = client1.db_name

my_collection = db1.collection_name



def reading(user_id):
   return my_collection.find_one({"_id": str(user_id)})['data'].values()