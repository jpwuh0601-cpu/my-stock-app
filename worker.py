import json
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        prev_close = ticker.fast_info.previous_close
        change = price - prev_close # 計算漲跌價
        
        result_data = {
            "price": price,
            "change": change,  # 漲跌價
            "bvps": info.get("bookValue", 0.0),
            "financials": {"2025Q1": {"EPS": info.get("trailingEps", 0.0)}},
            "pe_ratio": info.get("trailingPE", 0.0),
            "margin_ratio": 1.25,
            "institutional_investors": [{"機構": "外資", "買賣超": 12500}],
            "top_brokers": [{"券商": "凱基台北", "買進": 5500}],
            "ai_prediction": f"台積電最新股價 {price}，漲跌 {change:.2f}"
        }

        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
