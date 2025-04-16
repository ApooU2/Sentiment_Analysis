import yfinance as yf
from textblob import TextBlob
import requests
from datetime import datetime
import os

class SentimentEngine:
    def __init__(self, ticker):
        self.ticker = ticker
        self.chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
        self.chatgpt_api_key = os.getenv("GPT_API_KEY")
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.alpha_vantage_url = "https://www.alphavantage.co/query"
        self.api_key = os.getenv("NEWS_API_KEY")
        self.alpha_vant_api_key = os.getenv("ALPHA_VANT_API_KEY")

    def fetch_stock_data(self):
        """
        Fetch stock data for the given ticker. Handle cases where no data is available.
        """
        stock = yf.Ticker(self.ticker)
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            data = stock.history(start=today, end=today)
            if data.empty:
                print(f"No stock data available for {self.ticker} on {today}.")
                return None
            return data
        except Exception as e:
            print(f"Error fetching stock data for {self.ticker}: {e}")
            return None

    def fetch_alpha_vantage_data(self):
        """
        Fetch intraday stock data from Alpha Vantage.
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.ticker,
            "interval": "5min",
            "apikey": self.alpha_vant_api_key
        }
        response = requests.get(self.alpha_vantage_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("Time Series (5min)", {})
        else:
            print("Error fetching Alpha Vantage data:", response.status_code)
            return {}

    def get_company_name(self):
        """
        Fetch the company's name associated with the stock ticker using yfinance.
        """
        try:
            stock = yf.Ticker(self.ticker)
            return stock.info.get("longName", self.ticker)  # Fallback to ticker if name is unavailable
        except Exception as e:
            print(f"Error fetching company name for {self.ticker}: {e}")
            return self.ticker

    def analyze_sentiment(self, texts):
        """
        Analyze sentiment from a list of texts using TextBlob.
        """
        sentiment_scores = []
        for text in texts:
            analysis = TextBlob(text)
            sentiment_scores.append(analysis.sentiment.polarity)
        if sentiment_scores:
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            return avg_sentiment
        return 0

    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        multiplier = 2 / (period + 1)
        ema = [prices[0]]  # First value is same as price
        
        for price in prices[1:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        return ema

    def calculate_macd(self, alpha_data):
        """Calculate MACD and signal line"""
        try:
            # Extract closing prices
            prices = [float(data["4. close"]) for data in alpha_data.values()]
            prices.reverse()  # Reverse to get chronological order

            # Calculate 12 and 26 period EMAs
            ema12 = self.calculate_ema(prices, 12)
            ema26 = self.calculate_ema(prices, 26)

            # Calculate MACD line
            macd_line = [ema12[i] - ema26[i] for i in range(len(ema12))]
            
            # Calculate signal line (9-period EMA of MACD)
            signal_line = self.calculate_ema(macd_line, 9)

            return macd_line, signal_line
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return [], []

    def detect_macd_divergence(self, alpha_data):
        """
        Detect bullish and bearish divergences using MACD.
        Returns: 1 for bullish divergence, -1 for bearish divergence, 0 for no divergence
        """
        try:
            macd_line, signal_line = self.calculate_macd(alpha_data)
            if len(macd_line) < 2:
                return 0

            # Get the last two MACD values and closing prices
            prices = [float(data["4. close"]) for data in alpha_data.values()]
            prices.reverse()

            # Bullish divergence: Price making lower lows but MACD making higher lows
            if prices[-1] < prices[-2] and macd_line[-1] > macd_line[-2]:
                return 1
            # Bearish divergence: Price making higher highs but MACD making lower highs
            elif prices[-1] > prices[-2] and macd_line[-1] < macd_line[-2]:
                return -1
            return 0

        except Exception as e:
            print(f"Error detecting MACD divergence: {e}")
            return 0

    def analyze_alpha_vantage_sentiment(self, alpha_data):
        """
        Analyze sentiment based on MACD divergence.
        """
        if not alpha_data:
            print("No Alpha Vantage data available for sentiment analysis.")
            return 0

        divergence = self.detect_macd_divergence(alpha_data)
        if divergence == 1:
            print("Bullish divergence detected")
            return 1
        elif divergence == -1:
            print("Bearish divergence detected")
            return -1
        else:
            print("No significant divergence detected")
            return 0

    def run(self):
        """
        Run the sentiment analysis engine using Alpha Vantage data.
        """
        print(f"Fetching Alpha Vantage data for {self.ticker}...")
        alpha_data = self.fetch_alpha_vantage_data()
        if not alpha_data:
            print(f"No Alpha Vantage data available for {self.ticker}.")
        else:
            print("Analyzing sentiment based on Alpha Vantage data...")
            alpha_sentiment = self.analyze_alpha_vantage_sentiment(alpha_data)
            print(f"Alpha Vantage sentiment score for {self.ticker}: {alpha_sentiment}")

if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").upper()
    engine = SentimentEngine(ticker)
    engine.run()