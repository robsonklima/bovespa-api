import ssl
from pymongo import MongoClient
from bson.objectid import ObjectId
import yfinance as yf
import hashlib

client = MongoClient("mongodb+srv://app:Rkl2021@cluster0.pcxk9.mongodb.net/bovespa?retryWrites=true&w=majority",
                     ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

db = client['bovespa']
collection = db['stocks']

#INSERT
#collection.insert_one({'email': 'teste@teste.com', 'password': hashlib.md5(b'bovespa2020').digest(),
#                       'role': 'CLIENT',
#                       'wallet': [{'name': 'VALE3'}, {'name': 'AZUL4'}]})

db = client['bovespa']
collection = db['stocks']
cursor = collection.find({}, {'_id': False})

for i, stock in enumerate([{'name': 'CSNA3'}, {'name': 'WEGE3'}, {'name': 'PRIO3'}, {'name': 'MGLU3'}, {'name': 'BRAP4'}, {'name': 'VALE3'}, {'name': 'USIM5'}, {'name': 'B3SA3'}, {'name': 'SUZB3'}, {'name': 'RENT3'}]):
    collection.insert_one(stock)


#SELECT
#cursor = collection.find({'email': 'robsonklima@gmail.com', 'password': hashlib.md5("bovespa".encode("utf-8")).hexdigest()}, {'_id': False})
#for document in cursor:
#      print(document)

#cursor = db['stocks'].find({}, {'_id': False})
#for document in cursor:
#      print(document)

#UPDATE
#collection.update_one({'email': 'robsonklima@gmail.com'},
#                      {"$set": {'password': hashlib.md5("bovespa".encode("utf-8")).hexdigest(),
#                                'role': 'ADMIN', 'name': 'Robson Lima',
#                                'wallet': [{'name': 'ABEV'}, {'name': 'VALE3'},
#                                           {'name': 'BBDC3'}, {'name': 'BBAS3'}]}})

#DELETE
#collection.delete_many({'email':'teste@teste.com'})

#REPLACE
#obj = {
#    "email": "robsonklima@gmail.com",
#    "password": "e3e0cf8ee39f353e5519a32cb954e5b9",
#   "wallet": [{
#       "name": "VALE3"
#    }],
#    "role": "ADMIN",
#    "name": "Robson de Lima"
#}

#result = collection.replace_one({"email": 'robsonklima@gmail.com'}, obj, upsert=True)
