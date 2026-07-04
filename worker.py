import yfinance as yf
import twstock
import json
import datetime

def run_analysis_and_update():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    data = {}
    
    # 獲取今日日期用於格式化
    today = datetime.date.today()
    
    for symbol in tickers:
        try:
            stock_code = symbol.replace(".TW", "")
            stock = twstock.Stock(stock_code)
            
            # 獲取近 3 日籌碼 (使用 twstock 模擬或自行擴充 API)
            # 在實際應用中，您可以從財報 API 獲取更詳細的數據
            institutional_data = [
                {"日期": (today - datetime.timedelta(days=2)).strftime("%m-%d"), "外資": 1500, "投信": 300, "自營商": -100},
                {"日期": (today - datetime.timedelta(days=1)).strftime("%m-%d"), "外資": 2000, "投信": 450, "自營商": 50},
                {"日期": today.strftime("%m-%d"), "外資": -500, "投信": 150, "自營商": 200}
            ]
            
            ticker_yf = yf.Ticker(symbol)
            info = ticker_yf.info
            
            data[symbol] = {
                "price": info.get("currentPrice") or 0,
                "change": round(info.get("regularMarketChangePercent", 0), 2),
                "eps": info.get("trailingEps") or 0,
                "pe": info.get("forwardPE") or 0,
                "nav": info.get("bookValue") or 0,
                "black_swan": "安全" if info.get("regularMarketChangePercent", 0) > -3 else "⚠️ 高風險警示",
                "institutional_data": institutional_data
            }
        except Exception as e:
            print(f"[-] 處理 {symbol} 失敗: {e}")
            
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
