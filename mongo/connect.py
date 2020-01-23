import pymongo
import re
connection = pymongo.MongoClient('mongodb+srv://mongoproject:priya123@cluster0-jvyqt.mongodb.net/test?retryWrites=true&w=majority')
import json
database = connection['hospitals']
collection = database['data']
from bson.json_util import dumps
from geopy.geocoders import Nominatim
print('connection created')

def get_data(query):
    desc_exp = re.compile("\\b" + query + ".*", re.IGNORECASE)
    myregx = { "NAICS_DESC": { "$regex": str(query) +'.*'}}
    
    
    doc = collection.find(myregx)
    total = collection.count(myregx)
    
         
    print(total)
   
    return dumps(doc)

def get_multiple_data1(query):
    
    myregx = { "ID": int(query) }
    
    
    doc = collection.find(myregx)
    total = collection.count(myregx)
    
         
    print(total)
   
    return dumps(doc)



def get_geo_info(STATE):
    
    geo_loc = Nominatim(user_agent="mongoproject")
    location = geo_loc.geocode({'STATE'})
    return location.latitude, location.longitude



