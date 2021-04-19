import os
import hashlib
from bson import json_util
from flask import Flask, request, json, jsonify
import yfinance as yf
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://app:Rkl2021@cluster0.pcxk9.mongodb.net/bovespa?retryWrites=true&w=majority")


@app.route('/login/<email>/<password>', methods=['GET'])
def login(email, password):
    try:
        db = client['bovespa']
        collection = db['users']
        cursor = collection.find({'email': email, 'password': hashlib.md5(password.encode("utf-8")).hexdigest()},
                                 {'_id': False, 'password': False})

        for document in cursor:
            return json.loads(json_util.dumps(document))

        return {}
    except Exception as ex:
        return ex

@app.route('/stocks', methods=['GET'])
def getStocks():
    db = client['bovespa']
    collection = db['stocks']
    cursor = collection.find({}, {'_id': False})

    stocks = []
    for i, stock in enumerate(cursor):
        #if i == 1:
        msft = yf.Ticker(stock['name'] + ".SA")
        stock['info'] = msft.info
        stocks.append(stock)

    return jsonify(stocks)

@app.route('/users/<email>', methods=['GET'])
def getUser(email):
    try:
        db = client['bovespa']
        collection = db['users']
        cursor = collection.find({'email': email}, {'_id': False, 'password': False})

        for i, document in enumerate(cursor):
            for i, stock in enumerate(document['stocks']):
                msft = yf.Ticker(document['stocks'][i]['name'] + ".SA")
                document['stocks'][i]['info'] = msft.info
                #document['wallet'][i]['regularMarketPrice'] = msft.info['regularMarketPrice']
                #document['wallet'][i]['logo_url'] = msft.info['logo_url']

            return json.loads(json_util.dumps(document))
        return {}
    except Exception as ex:
        return ex

@app.route('/users', methods=['POST'])
def putUser():
    db = client['bovespa']
    collection = db['users']
    user = request.json
    collection.replace_one({"email": user['email']}, user, upsert=True)
    return user


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
