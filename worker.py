import json
import yfinance as yf
import datetime

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW"]

def get_籌碼屬性(張數):
    return "大戶" if abs(張數) >= 400 else "散戶"

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 模擬數據：此處您未來可替換為真實的 API 資料
        inst_data = [
            {"法人": "外資", "買賣超(張)": 1200, "屬性": get_籌碼屬性(1200)},
            {"法人": "投信", "買賣超(張)": 300, "屬性": get_籌碼屬性(300)},
            {"法人": "自營商", "買賣超(張)": -500, "屬性": get_籌碼屬性(-500)}
        ]
        broker_data = [
            {"券商名稱": "凱基-台北", "買賣超(張)": 550, "屬性": get_籌碼屬性(550)},
            {"券商名稱": "元大-總公司", "買賣超(張)": 420, "屬性": get_籌碼屬性(420)},
            {"券商名稱": "富邦-建國", "買賣超(張)": 80, "屬性": get_籌碼屬性(80)}
        ]
        
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChangePercent", 0),
            "institutional_data": inst_data,
            "broker_data": broker_data
        }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
