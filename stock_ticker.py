import os
import requests
import json

# Fetch API key from environment variable (GitHub Secret)
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise ValueError("Finnhub API key not found in environment variables.")

# List of stock symbols to track
COMPANIES = ["VZ", "AAPL", "MSFT"]

def fetch_stock_data(symbol):
    # Fetch stock price
    price_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    price_data = requests.get(price_url).json()

    # Fetch logo
    logo_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
    logo_data = requests.get(logo_url).json()

    return {
        "symbol": symbol,
        "current_price": price_data["c"],
        "change": price_data["d"],
        "percentage_change": price_data["dp"],
        "logo": logo_data.get("logo", None)
    }

def main():
    stock_data = []
    for company in COMPANIES:
        data = fetch_stock_data(company)
        stock_data.append(data)
        print(f"{data['symbol']}: ${data['current_price']} (${data['change']}, {data['percentage_change']}%)")
        if data["logo"]:
            print(f"Logo: {data['logo']}")

    # Save data to a JSON file in the repository
    with open("stock_data.json", "w") as f:
        json.dump(stock_data, f, indent=2)
    print("Stock data saved to stock_data.json")

if __name__ == "__main__":
    main()
