from flask import Flask, request, render_template
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import json
#6GYSMEH5TM3A42X4
app = Flask(__name__)
mapping = {
    'AAPL': 'Apple Inc.',
    'GOOGL': 'Alphabet Inc. (Google)',
    'MSFT': 'Microsoft Corporation',
    'V': 'Visa Inc.',
    'JNJ': 'Johnson & Johnson',
    'WMT': 'Walmart Inc.'
}

def get_historical_data(api_key, symbol):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
    return data

def suggest_stocks(strategy):
    ethical_investing_portfolio = ['AAPL', 'GOOGL', 'MSFT']
    value_investing_portfolio = ['V', 'JNJ', 'WMT']

    if strategy == 'Ethical Investing':
        return ethical_investing_portfolio
    elif strategy == 'Value Investing':
        return value_investing_portfolio
    else:
        return None

def calculate_allocation(invest_amount, selected_stocks):
    allocation_per_stock = invest_amount / len(selected_stocks)
    return allocation_per_stock

def calculate_portfolio_value(selected_stocks, allocation_per_stock):
    portfolio_value = 0
    portfolio_composition = []
    ALPHA_VANTAGE_API_KEY = '6GYSMEH5TM3A42X4'
    # Inside your calculate_portfolio_value function
    for symbol in selected_stocks:
        stock_data = get_historical_data(ALPHA_VANTAGE_API_KEY, symbol)
        current_price = float(stock_data['4. close'].iloc[0])
        shares_to_buy = int(allocation_per_stock / current_price)
        portfolio_value += shares_to_buy * current_price
        company_name = mapping.get(symbol, 'N/A')

        stock_data['date'] = pd.to_datetime(stock_data.index)
        stock_data.set_index('date', inplace=True)

        last_5_days_data = stock_data.head(5)
        result = last_5_days_data['4. close'].to_dict()

        # Convert Timestamp keys to strings
        result_str_keys = {key.strftime('%Y-%m-%d'): value for key, value in result.items()}
        #result_str_keys = {key.tz_localize('UTC').tz_convert('America/New_York').strftime('%Y-%m-%d'): value for key, value in result.items()}
        # Add detailed information to the portfolio_composition list
        composition_item = {
            "symbol": symbol,
            "company_name": company_name,
            "current_price": current_price,
            "shares_to_buy": shares_to_buy,
            "result": result_str_keys
        }
        portfolio_composition.append(composition_item)
    return portfolio_value, portfolio_composition


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        print("Received POST request")
        invest_amount = float(request.form.get('invest_amount'))
        strategy = request.form.get('strategy')

        if invest_amount < 5000:
            tempData = {"error": "Minimum investment amount is $5000."}
            return render_template('index.html', **tempData)

        selected_stocks = suggest_stocks(strategy)
        if not selected_stocks:
            tempData = {"error": "Invalid Strategy"}
            return render_template('index.html', **tempData)
        print("selected_stocks: {selected_stocks}")
        allocation_per_stock = calculate_allocation(invest_amount, selected_stocks)
        print("allocation_per_stock: {allocation_per_stock}")
        portfolio_value, portfolio_composition = calculate_portfolio_value(selected_stocks, allocation_per_stock)
        print("selected_stocks: {selected_stocks}, allocation_per_stock: {allocation_per_stock}, portfolio_composition: {portfolio_composition}")
        tempData = {
            "selected_stocks": selected_stocks,
            "allocation_per_stock": allocation_per_stock,
            "portfolio_composition": portfolio_composition,
            "portfolio_value": portfolio_value, "error":"success"
        }
        return render_template('index.html', **tempData)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
