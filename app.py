import os
from flask import Flask, json
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)
API_key = 'SBAHO6UH7BX7GIBV'

@app.route('/symbols/<symbol>', methods=['GET'])
def symbols(symbol):
    ts = TimeSeries(key=API_key)
    data, meta_data = ts.get_symbol_search(symbol)
    return data.to_json(orient='records')[1:-1].replace('},{', '} {')

@app.route('/quotes/<symbol>', methods=['GET'])
def quotes(symbol):
    ts = TimeSeries(key=API_key)
    data, meta_data = ts.get_quote_endpoint(symbol)
    return json.dumps(data, indent=4)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)