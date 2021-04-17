import os
import ssl
import hashlib
from bson import json_util
from flask import Flask, request, jsonify, json
import yfinance as yf
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://app:Rkl2021@cluster0.pcxk9.mongodb.net/bovespa?retryWrites=true&w=majority",
                     ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

@app.route('/stocks', methods=['POST'])
def stocks():
    sts = request.json
    stocks = []

    try:
        for i, quote in enumerate(sts):
            msft = yf.Ticker(quote['name'] + ".SA")
            stocks.append({
                'stock': msft.info
            })

        return jsonify(stocks)
    except:
        stocks.append({
            'errorMessage': 'Nao foi possivel carregar os registros',
            'error': True
        })
        return jsonify(stocks)

@app.route('/stocks/<stock>', methods=['GET'])
def stock(stock):
    stocks = []

    try:
        msft = yf.Ticker(stock + ".SA")
        stocks.append({
            'stock': msft.info
        })

        return jsonify(stocks)
    except:
        stocks.append({
            'errorMessage': 'Nao foi possivel carregar os registros',
            'error': True
        })
        return jsonify(stocks)

@app.route('/login/<email>/<password>', methods=['GET'])
def login(email, password):
    try:
        db = client['bovespa']
        collection = db['users']
        cursor = collection.find({'email': email, 'password': hashlib.md5(password.encode("utf-8")).hexdigest()})

        for document in cursor:
            return json.loads(json_util.dumps(document))

        return {}
    except Exception as ex:
        return ex


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
