import json
import logging
import yfinance as yf
import os
import shutil
import datetime
from openai import OpenAI

# 設定日誌
logging.basicConfig(level=logging.INFO)

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_financials(ticker):
    """抓取財報基本面數據"""
    info = ticker.info
    return {
        "bvps": info.get("bookValue", 0),
        "pe_ratio": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0),
        "revenue_growth": info.get("revenueGrowth", 0)
    }

def get_ai_analysis(ticker_symbol, data):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: return "AI 分析模組未設定。"
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key.strip())
        prompt = f"分析 {ticker_symbol}，股價: {data.get('price')}，EPS: {data.get('eps')}。給予投資建議。"
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析失敗: {e}")
        return "分析暫時不可用。"

def run_analysis_and_update():
    all_results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for ticker_symbol in TICKER_LIST:
        try:
            ticker = yf.Ticker(ticker_symbol)
            fin = get_financials(ticker)
            price = ticker.fast_info.last_price
            
            all_results[ticker_symbol] = {
                "price": price,
                "bvps": fin["bvps"],
                "pe": fin["pe_ratio"],
                "eps": fin["eps"],
                "history": ticker.history(period="1mo")['Close'].reset_index().to_dict(orient='records'),
                "ai_prediction": get_ai_analysis(ticker_symbol, {"price": price, "eps": fin["eps"]})
            }
        except Exception as e:
            logging.error(f"股票 {ticker_symbol} 處理失敗: {e}")
    
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    os.replace(tmp_file, DATA_FILE)
    logging.info("數據更新完成。")

if __name__ == "__main__":
    run_analysis_and_update()
