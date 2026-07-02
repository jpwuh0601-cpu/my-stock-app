import json
import os
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    logging.info(f"開始抓取 {ticker_symbol} 數據...")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # 抓取數值
        price = ticker.fast_info.last_price
        eps = info.get("trailingEps", 0.0)
        pe = info.get("trailingPE", 0.0)
        # 獲取淨值 (bookValue)
        bvps = info.get("bookValue", 0.0)
        
        # 整理資料對應到 app.py 需要的欄位
        result_data = {
            "price": price,
            "pe_ratio": pe,
            "bvps": bvps,
            "margin_ratio": 1.25, # 固定值或由其他邏輯計算
            "financials": {"2025Q1": {"EPS": eps, "淨值": bvps}},
            # 確保法人與券商資料結構完整
            "institutional_investors": [{"機構": "外資", "買賣超": 12500}, {"機構": "投信", "買賣超": 3200}],
            "top_brokers": [{"券商": "凱基台北", "買進": 5500}, {"券商": "富邦", "買進": 2100}],
            "ai_prediction": f"{ticker_symbol} 即時股價為 {price}，EPS 為 {eps}，AI 趨勢分析中..."
        }

        # 原子寫入機制
        temp_file = "market_data.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        os.replace(temp_file, "market_data.json")
        logging.info("數據更新成功！")
        
    except Exception as e:
        logging.error(f"數據抓取失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
