import requests

def fetch_alpha_vantage_data(ticker, url, api_key):
	params = {
		"function": "TIME_SERIES_INTRADAY",
		"symbol": ticker,
		"interval": "5min",
		"apikey": api_key
	}
	response = requests.get(url, params=params)
	if response.status_code == 200:
		data = response.json()
		return data.get("Time Series (5min)", {})
	else:
		print("Error fetching Alpha Vantage data:", response.status_code)
		return {}

def calculate_ema(prices, period):
	multiplier = 2 / (period + 1)
	ema = [prices[0]]
	for price in prices[1:]:
		ema.append((price - ema[-1]) * multiplier + ema[-1])
	return ema

def calculate_macd(alpha_data):
	try:
		prices = [float(data["4. close"]) for data in alpha_data.values()]
		prices.reverse()
		ema12 = calculate_ema(prices, 12)
		ema26 = calculate_ema(prices, 26)
		macd_line = [ema12[i] - ema26[i] for i in range(len(ema12))]
		signal_line = calculate_ema(macd_line, 9)
		return macd_line, signal_line
	except Exception as e:
		print(f"Error calculating MACD: {e}")
		return [], []

def detect_macd_divergence(alpha_data):
	try:
		macd_line, signal_line = calculate_macd(alpha_data)
		if len(macd_line) < 2:
			return 0
		prices = [float(data["4. close"]) for data in alpha_data.values()]
		prices.reverse()
		if prices[-1] < prices[-2] and macd_line[-1] > macd_line[-2]:
			return 1
		elif prices[-1] > prices[-2] and macd_line[-1] < macd_line[-2]:
			return -1
		return 0
	except Exception as e:
		print(f"Error detecting MACD divergence: {e}")
		return 0

def analyze_alpha_vantage_sentiment(alpha_data):
	if not alpha_data:
		print("No Alpha Vantage data available for sentiment analysis.")
		return 0
	divergence = detect_macd_divergence(alpha_data)
	if divergence == 1:
		print("Bullish divergence detected")
		return 1
	elif divergence == -1:
		print("Bearish divergence detected")
		return -1
	else:
		print("No significant divergence detected")
		return 0