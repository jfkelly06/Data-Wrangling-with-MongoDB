##Insert cleaned into MongoDB
    #In command prompt:
        #establish mongo daemon- mongod
        #mongoimport --db osm --collection map --file NY-CT.xml.json

##Query MongoDB from Command Prompt
    #start mongo
    #use osm

    #DataSize -100,832,096
db.map.dataSize()

    #Number of Users
db.map.distinct("created.user").length

   #nodes-561,808
db.map.find( { type: "node" } ).length()

    #ways-57,810
db.map.find( { type: "way" } ).length()


#Query MongoDB from Python Shell
from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.osm

    #5 Most Popular Ammenities-
db.map.aggregate([{ "$group" : { "_id" : "$amenity",
"count" : { "$sum" : 1 }}}, { "$sort" : { "count" : -1 }}, {"$limit" : 10}])   


    #restaurant name and cuisine
db.map.aggregate([{"$match": {"amenity": "restaurant"}},
                  {"$project":{"_id": "$name", "cuisine": "$cuisine"}},
{"$limit" : 5}])
                  
    #most popular cusine              
db.map.aggregate([{"$match": {"amenity": "restaurant"}},
                  { "$group" : { "_id" : "$cuisine",
"count" : { "$sum" : 1 }}}, { "$sort" : { "count" : -1 }}, {"$limit" : 5}])  