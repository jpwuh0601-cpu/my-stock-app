import json
import logging
import yfinance as yf
import os
import shutil
from openai import OpenAI

# 設定日誌
logging.basicConfig(level=logging.INFO)

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"
BACKUP_FILE = "market_data.json.bak"

def get_ai_analysis(ticker_symbol, data):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "AI 分析模組未設定。"
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key.strip())
        prompt = f"請分析 {ticker_symbol}，股價: {data.get('price')}。簡短建議。"
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI 分析 {ticker_symbol} 失敗: {e}")
        return "分析暫時不可用。"

def run_analysis_and_update():
    # 1. 建立當前數據備份
    if os.path.exists(DATA_FILE):
        shutil.copy2(DATA_FILE, BACKUP_FILE)
    
    all_results = {}
    
    # 2. 輪詢處理 (故障隔離)
    for ticker_symbol in TICKER_LIST:
        try:
            logging.info(f"開始處理: {ticker_symbol}")
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1mo")
            price = ticker.fast_info.last_price
            
            all_results[ticker_symbol] = {
                "price": price,
                "history": hist['Close'].reset_index().to_dict(orient='records'),
                "ai_prediction": get_ai_analysis(ticker_symbol, {"price": price})
            }
        except Exception as e:
            logging.error(f"股票 {ticker_symbol} 處理失敗，跳過此項: {e}")
    
    # 3. 原子寫入 (寫入暫存檔後再更名)
    if all_results:
        tmp_file = DATA_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        os.replace(tmp_file, DATA_FILE)
        logging.info("數據寫入完成，系統穩定。")
    else:
        logging.error("沒有成功獲取任何數據，保留舊檔案以維持儀表板運作。")

if __name__ == "__main__":
    run_analysis_and_update()
