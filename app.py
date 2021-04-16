import os
from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)
API_key = '0244'


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
