import yfinance as yf
from datetime import datetime

def fetch_stock_data(ticker):
	stock = yf.Ticker(ticker)
	today = datetime.now().strftime('%Y-%m-%d')
	try:
		data = stock.history(start=today, end=today)
		if data.empty:
			print(f"No stock data available for {ticker} on {today}.")
			return None
		return data
	except Exception as e:
		print(f"Error fetching stock data for {ticker}: {e}")
		return None

def get_company_name(ticker):
	try:
		stock = yf.Ticker(ticker)
		return stock.info.get("longName", ticker)
	except Exception as e:
		print(f"Error fetching company name for {ticker}: {e}")
		return ticker