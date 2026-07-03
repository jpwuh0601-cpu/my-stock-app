import json
import logging
import yfinance as yf
import os
import requests
from openai import OpenAI

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 設定要追蹤的股票清單
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]

def get_ai_analysis(ticker_symbol, data):
    """呼叫 OpenRouter/OpenAI 生成分析"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "AI 分析模組未設定 API Key。"

    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key.strip())
        prompt = f"請對 {ticker_symbol} 進行投資分析，數據如下: {data}"
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析失敗: {e}")
        return "分析暫時不可用。"

def run_analysis_and_update():
    all_results = {}
    
    for ticker_symbol in TICKER_LIST:
        try:
            logging.info(f"正在分析: {ticker_symbol}")
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1mo")
            price = ticker.fast_info.last_price
            
            data = {
                "price": price,
                "history": hist['Close'].reset_index().to_dict(orient='records'),
                "ai_prediction": ""
            }
            
            data["ai_prediction"] = get_ai_analysis(ticker_symbol, data)
            all_results[ticker_symbol] = data
            
        except Exception as e:
            logging.error(f"{ticker_symbol} 分析錯誤: {e}")
    
    # 將所有股票結果寫入同一個檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    logging.info("所有股票分析更新完成")

if __name__ == "__main__":
    run_analysis_and_update()
