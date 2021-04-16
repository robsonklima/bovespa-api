import os
from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)
API_key = '0244'


@app.route('/quotes', methods=['POST'])
def quotes():
    qs = request.json
    stocks = []

    try:
        for i, quote in enumerate(qs):
            msft = yf.Ticker(quote['symbol'] + ".SA")
            stocks.append({
                'quote': msft.info
            })

        return jsonify(stocks)
    except:
        stocks.append({
            'errorMessage': 'Nao foi possivel carregar os registros',
            'error': True
        })
        return jsonify(stocks)

@app.route('/quotes/<quote>', methods=['GET'])
def quote(quote):
    qs = request.json
    stocks = []

    try:
        msft = yf.Ticker(quote + ".SA")
        stocks.append({
            'quote': msft.info
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
