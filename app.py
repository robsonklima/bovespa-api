import os
from flask import Flask, request, jsonify
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)
API_key = '0244'

@app.route('/quotes', methods=['POST'])
def quotes():
    ts = TimeSeries(key=API_key)
    quotes = request.json
    stocks_formatted = []

    for i, quote in enumerate(quotes):
        q, meta_data = ts.get_quote_endpoint(quote['symbol'] + '.SAO')
        s, meta_data = ts.get_symbol_search(quote['symbol'])
        stocks_formatted.append({'symbol': next(iter(s.to_dict(orient='record'))), 'quote': q})

    return jsonify(stocks_formatted)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)