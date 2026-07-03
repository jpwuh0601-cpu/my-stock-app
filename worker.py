import json
import logging
import yfinance as yf
import os
import requests
from openai import OpenAI

# ... (保留原有的 get_ai_analysis 與 send_line_notify) ...

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 抓取最近 30 天的歷史股價
        hist = ticker.history(period="1mo")
        # 將歷史數據轉換為可 JSON 序列化的格式
        history_data = hist['Close'].reset_index().to_dict(orient='records')
        
        price = ticker.fast_info.last_price
        
        raw_data = {
            "price": price,
            "history": history_data, # 新增歷史數據
            "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        }
        
        raw_data["ai_prediction"] = get_ai_analysis(raw_data)
        
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
        logging.info("歷史數據與分析更新完成")
    except Exception as e:
        logging.error(f"執行錯誤: {e}")
