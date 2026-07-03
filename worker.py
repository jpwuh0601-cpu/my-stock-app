import yfinance as yf
import json
import datetime

def run_analysis_and_update():
    tickers = ["2330.TW", "2317.TW", "2454.TW"]
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="10d")
        last_price = hist['Close'].iloc[-1]
        
        data[symbol] = {
            "price": float(last_price),
            "history": hist[['Close']].reset_index().rename(columns={'Date': 'Date', 'Close': 'Close'}).to_dict(orient='records'),
            "ai_prediction": "目前數據已自動更新。請根據上方股價與技術指標進行判斷。"
        }
    
    with open("market_data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
