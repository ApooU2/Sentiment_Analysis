import os
import alpha_vantage_api as alpha_api
import yahoo_finance_api as yf_api
import textblob_sentiment as tb_sentiment

class SentimentEngine:
	# --- API Configuration ---
	def __init__(self, ticker):
		# --- API Configuration ---
		self.ticker = ticker
		self.chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
		self.chatgpt_api_key = os.getenv("GPT_API_KEY")
		self.news_api_url = "https://newsapi.org/v2/everything"
		self.alpha_vantage_url = "https://www.alphavantage.co/query"
		self.api_key = os.getenv("NEWS_API_KEY")
		self.alpha_vant_api_key = os.getenv("ALPHA_VANT_API_KEY")

	# --- Main Execution ---
	def run(self):
		"""
		Run the sentiment analysis engine using Alpha Vantage data.
		"""
		print(f"Fetching Alpha Vantage data for {self.ticker}...")
		alpha_data = alpha_api.fetch_alpha_vantage_data(self.ticker, self.alpha_vantage_url, self.alpha_vant_api_key)
		if not alpha_data:
			print(f"No Alpha Vantage data available for {self.ticker}.")
		else:
			print("Analyzing sentiment based on Alpha Vantage data...")
			alpha_sentiment = alpha_api.analyze_alpha_vantage_sentiment(alpha_data)
			print(f"Alpha Vantage sentiment score for {self.ticker}: {alpha_sentiment}")

		# Example usage for Yahoo Finance API:
		stock_data = yf_api.fetch_stock_data(self.ticker)
		if stock_data:
			company_name = yf_api.get_company_name(self.ticker)
			print(f"Company name: {company_name}")

		# Example usage for TextBlob Sentiment Analysis:
		# texts = [...] 
		# sentiment = tb_sentiment.analyze_sentiment(texts)
		# print(f"TextBlob sentiment score: {sentiment}")

if __name__ == "__main__":
	ticker = input("Enter the stock ticker: ").upper()
	engine = SentimentEngine(ticker)
	engine.run()