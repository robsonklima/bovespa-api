import os
import hashlib
from bson import json_util
from flask import Flask, request, json, jsonify
import yfinance as yf
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://app:Rkl2021@cluster0.pcxk9.mongodb.net/bovespa?retryWrites=true&w=majority")


@app.route('/stocks', methods=['GET'])
def getStocks():
    db = client['bovespa']
    collection = db['stocks']
    cursor = collection.find({}, {'_id': False})

    stocks = []
    for i, stock in enumerate(cursor):
        # if i == 1:
        msft = yf.Ticker(stock['name'] + ".SA")
        stock['info'] = msft.info
        stocks.append(stock)

    return jsonify(stocks)

@app.route("/stocks/<name>", methods=["GET"])
def getStock(name):
    db = client['bovespa']
    collection = db['stocks']
    stock = collection.find_one({'name': name}, {'_id': False})
    msft = yf.Ticker(stock['name'] + ".SA")
    stock['info'] = msft.info

    return json.loads(json_util.dumps(stock))

@app.route('/stocks', methods=['POST'])
def postStock():
    db = client['bovespa']
    collection = db['stocks']
    stock = request.json
    collection.replace_one({"name": stock['name']}, stock, upsert=True)
    return stock

@app.route("/stocks/<name>", methods=["DELETE"])
def deleteStock(name):
    db = client['bovespa']
    collection = db['stocks']
    collection.find_one_and_delete({'name': name})

    return jsonify({'name': name})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
