import json
import os
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    ticker_symbol = "2330.TW"  # 您可以設定為動態變數
    logging.info(f"開始抓取 {ticker_symbol} 數據...")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # 獲取即時股價 (使用 fast_info 較快且穩)
        price = ticker.fast_info.last_price
        
        # 獲取 EPS (若無則預設為 0)
        eps = info.get("trailingEps", 0.0)
        pe_ratio = info.get("trailingPE", 0.0)
        bvps = info.get("bookValue", 0.0)
        
        result_data = {
            "price": price,
            "pe_ratio": pe_ratio,
            "bvps": bvps,
            "margin_ratio": 1.25, # 此數值若無法由 yf 取得，維持固定或由 AI 計算
            "est_eps": eps,
            "institutional_10d": [{"機構": "外資", "10日累計": 12500}],
            "brokers_10d": [{"券商": "凱基台北", "10日累計": 5500}],
            "ai_prediction": f"{ticker_symbol} 即時股價為 {price}，EPS 為 {eps}，AI 趨勢分析中..."
        }

        temp_file = "market_data.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        os.replace(temp_file, "market_data.json")
        logging.info("數據更新成功！")
        
    except Exception as e:
        logging.error(f"抓取數據失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
