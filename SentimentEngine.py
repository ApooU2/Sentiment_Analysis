import os
from sec_api import SECApi

class SentimentEngine:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.sec_api = SECApi()

    def run(self):
        """
        Run the sentiment analysis engine using SEC filings data.
        """
        print(f"Fetching SEC filings data for {self.ticker}...")
        filings_data = self.sec_api.fetch_company_filings(self.ticker)
        
        if not filings_data:
            print(f"No SEC filings data available for {self.ticker}.")
            return
            
        print("Analyzing SEC filings...")
        analysis = self.sec_api.analyze_filings_sentiment(filings_data)
        
        print(f"\nAnalysis Results for {self.ticker}:")
        if analysis["status"] == "success":
            print(f"Total filings found: {analysis['total_filings']}")
            print("\nMost recent filings:")
            for filing in analysis["recent_filings"]:
                print(f"- {filing['filing_date']}: {filing['form_type']} - {filing['description']}")
        else:
            print(f"Analysis status: {analysis['status']}")

if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").upper()
    engine = SentimentEngine(ticker)
    engine.run()