from alpha_vantage.timeseries import TimeSeries
import pandas as pd
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

def calculate_portfolio_value(selected_stocks, allocation_per_stock):
    portfolio_value = 0
    ALPHA_VANTAGE_API_KEY = '6GYSMEH5TM3A42X4'
    portfolio_composition = []

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

        # Print the values
        print(f"Symbol: {symbol}")
        print(f"Company Name: {company_name}")
        print(f"Current Price: {current_price}")
        print(f"Shares to Buy: {shares_to_buy}")
        print("Last 5 Days Closing Prices:")
        for date, price in result.items():
            print(f"{date}: {price}")
        print()

if __name__ == "__main__":
    # Set your selected stocks and allocation per stock
    selected_stocks = ['AAPL', 'GOOGL', 'MSFT']
    allocation_per_stock = 1000

    calculate_portfolio_value(selected_stocks, allocation_per_stock)
