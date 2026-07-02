import json
import os
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    logging.info(f"開始抓取 {ticker_symbol} 即時數據...")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 獲取即時數據
        price = ticker.fast_info.last_price
        info = ticker.info
        
        # 抓取財報指標 (處理缺失值)
        eps = info.get("trailingEps", 0.0)
        pe = info.get("trailingPE", 0.0)
        bvps = info.get("bookValue", 0.0)
        
        # 整合數據
        data = {
            "price": price,
            "bvps": bvps,
            "financials": {"2025Q1": {"EPS": eps, "淨值": bvps}},
            "pe_ratio": pe,
            "margin_ratio": 1.25,
            "institutional_investors": [{"機構": "外資", "買賣超": 500}],
            "top_brokers": [{"券商": "凱基台北", "買進": 1000}],
            "ai_prediction": f"系統已自動更新，{ticker_symbol} 當前股價: {price}，EPS: {eps}"
        }

        # 寫入檔案
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info("數據寫入成功")
        
    except Exception as e:
        logging.error(f"數據抓取失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
