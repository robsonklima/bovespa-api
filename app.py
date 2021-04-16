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

    try:
        for i, quote in enumerate(quotes):
            q, meta_data = ts.get_quote_endpoint(quote['symbol'] + '.SAO')
            s, meta_data = ts.get_symbol_search(quote['symbol'])
            sy = next(iter(s.to_dict(orient='record')))
            if len(q) > 0 and len(q) > 0:
                stocks_formatted.append({
                    'symbol': {
                        "symbol": sy['1. symbol'],
                        "name": sy['2. name'],
                        "type": sy['3. type'],
                        "region": sy['4. region'],
                        "marketOpen": sy['5. marketOpen'],
                        "marketClose": sy['6. marketClose'],
                        "timezone": sy['7. timezone'],
                        "currency": sy['8. currency'],
                        "matchScore": sy['9. matchScore']
                    },
                    'quote': {
                        "symbol": q['01. symbol'],
                        "open": q['02. open'],
                        "high": q['03. high'],
                        "low": q['04. low'],
                        "price": q['05. price'],
                        "volume": q['06. volume'],
                        "latestTradingDay": q['07. latest trading day'],
                        "previousClose": q['08. previous close'],
                        "change": q['09. change'],
                        "changePercent": q['10. change percent']
                    },
                    'errorMessage': None,
                    'error': False
                })
            else:
                stocks_formatted.append({
                    'errorMessage': 'Nao foi possivel carregar os registros',
                    'error': True
                })
        return jsonify(stocks_formatted)
    except:
        stocks_formatted.append({
            'errorMessage': 'Nao foi possivel carregar os registros',
            'error': True
        })
        return jsonify(stocks_formatted)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
