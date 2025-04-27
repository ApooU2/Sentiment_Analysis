import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class SECApi:
    def __init__(self):
        self.base_url = "https://data.sec.gov/api/edgar"
        self.headers = {
            "User-Agent": "YourName yourname@email.com",  # Replace with your details
            "Accept": "application/json",
        }

    def fetch_company_filings(self, ticker: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch recent SEC filings for a company using the SEC EDGAR API.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            Optional[List[Dict[str, Any]]]: List of filing data or None if request fails
        """
        try:
            # Get company CIK number
            response = requests.get(
                f"https://www.sec.gov/files/company_tickers.json",
                headers=self.headers
            )
            response.raise_for_status()
            companies = response.json()
            
            # Find CIK for the ticker
            cik = None
            for entry in companies.values():
                if entry['ticker'].upper() == ticker.upper():
                    cik = str(entry['cik_str']).zfill(10)
                    break
            
            if not cik:
                print(f"Could not find CIK for ticker {ticker}")
                return None
            
            # Fetch company filings
            url = f"{self.base_url}/company/{cik}/filings"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error fetching SEC data: {e}")
            return None

    def analyze_filings_sentiment(self, filings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze recent filings to determine company status and important changes.
        
        Args:
            filings (List[Dict[str, Any]]): List of SEC filings
            
        Returns:
            Dict[str, Any]: Analysis results including filing types and dates
        """
        if not filings:
            return {"status": "No filings found"}
            
        recent_filings = []
        for filing in filings.get('filings', {}).get('recent', [])[:5]:
            recent_filings.append({
                "form_type": filing.get('form'),
                "filing_date": filing.get('filingDate'),
                "description": filing.get('description', ''),
            })
            
        return {
            "status": "success",
            "recent_filings": recent_filings,
            "total_filings": len(filings.get('filings', {}).get('recent', [])),
        }