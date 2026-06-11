import os
import requests
import json

# Fetch API key from environment variable (GitHub Secret)
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise ValueError("Finnhub API key not found in environment variables.")

# List of stock symbols to track
COMPANIES = ["AAPL","ABBV","ACN","AMD","AMGN","AMZN","APP","ARM","ASML","AVGO","AXON","AXP","BA","BKNG","BKR","CAT","CCEP","CDNS","CEG","CHTR","CMCSA","COST","CPRT","CRM","CRWD","CSCO","CSX","CTAS","CTSH","CVX","DASH","DDOG","DIS","DXCM","EA","EXC","FANG","FAST","FER","FTNT","GEHC","GILD","GOOG","GOOGL","GS","HD","HON","IBM","IDXX","INSM","INTC","INTU","ISRG","JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LITE","LRCX","MAR","MCD","MCHP","MDLZ","MELI","META","MMM","MNST","MPWR","MRK","MRVL","MSFT","MSTR","MU","NFLX","NKE","NVDA","NXPI","ODFL","ORLY","PANW","PAYX","PCAR","PDD","PEP","PG","PLTR","PYPL","QCOM","REGN","ROP","ROST","SBUX","SHOP","SHW","SNDK","SNPS","STX","TMUS","TRI","TRV","TSLA","TTWO","TXN","UNH","V","VRSK","VRTX","VZ","WBD","WDAY","WDC","WMT","XEL","ZS"]

def fetch_stock_data(symbol):
    # Fetch stock price
    price_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    price_data = requests.get(price_url).json()

    # Fetch company name and logo
    logo_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
    logo_data = requests.get(logo_url).json()

    return {
        "symbol": symbol,
        "name": logo_data.get("name", symbol),
        "current_price": price_data["c"],
        "change": price_data["d"],
        "percentage_change": price_data["dp"],
        "logo": logo_data.get("logo", None)
    }

def format_change(change, percentage_change):
    if change >= 0:
        arrow = "↑"
        price_color = "green"
        percent_color = "green"
    else:
        arrow = "↓"
        price_color = "red"
        percent_color = "red"

    return f"({price_color}){arrow} {abs(change)} ({abs(percentage_change)}%)(/color)"

def main():
    stock_data = []
    formatted_output = []

    for company in COMPANIES:
        data = fetch_stock_data(company)
        stock_data.append(data)

        # Format the output line
        change_str = format_change(data["change"], data["percentage_change"])
        logo_str = f"[{data['logo']}]" if data["logo"] else ""
        line = f"{logo_str} {data['name']} {data['current_price']} {change_str}"
        formatted_output.append(line)

        print(line)

    # Save formatted data to a JSON file in the repository
    with open("stock_data.json", "w") as f:
        json.dump(stock_data, f, indent=2)
    print("\nStock data saved to stock_data.json")

if __name__ == "__main__":
    main()
