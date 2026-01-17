# stock_price_checker.py
# Run with: python stock_price_checker.py

import yfinance as yf

def get_stock_price(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        return "Error: Please enter a stock code"

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if 'regularMarketPrice' not in info or info.get('regularMarketPrice') is None:
            # Fallback to history if info is incomplete (sometimes happens)
            hist = ticker.history(period="1d")
            if hist.empty:
                return f"Error: No data found for {symbol}"
            price = hist['Close'].iloc[-1]
            currency = info.get('currency', 'USD')
            name = info.get('shortName', symbol)
        else:
            price = info['regularMarketPrice']
            currency = info.get('currency', 'USD')
            name = info.get('shortName', symbol)

        change = info.get('regularMarketChange', 0)
        change_pct = info.get('regularMarketChangePercent', 0)

        change_sign = "+" if change >= 0 else ""
        change_color = "green" if change >= 0 else "red"

        return (
            f"{name} ({symbol})\n"
            f"Price: {price:.2f} {currency}\n"
            f"Change: {change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)\n"
            f"Last updated: {info.get('regularMarketTime', 'N/A')}"
        )
    except Exception as e:
        return f"Error: {str(e)}\nTry checking the ticker (e.g. 0700.HK, AAPL, 9988.HK)"

# Simple loop
print("Stock Price Checker (type 'exit' to quit)")
while True:
    ticker = input("\nEnter stock code (e.g. AAPL, 0700.HK): ").strip()
    if ticker.lower() in ['exit', 'quit', 'q']:
        break
    result = get_stock_price(ticker)
    print("\n" + result)
