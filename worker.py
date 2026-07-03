import json
import logging
import yfinance as yf
import datetime
import time
import os
from openai import OpenAI

# 設定 OpenAI Client (使用 OpenRouter 兼容 API)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

logging.basicConfig(level=logging.INFO)
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]
DATA_FILE = "market_data.json"

def get_ai_analysis(symbol, data):
    """呼叫 AI 進行分析"""
    prompt = f"""
    請針對股票 {symbol} 提供簡短的投資分析。
    最新數據：價格 {data['price']}, EPS {data['eps']}, 本益比 {data['pe']}, 每股淨值 {data['bvps']}。
    請用繁體中文，用專業且客觀的語氣，整理出一句投資建議。
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析暫時無法取得: {e}"

def get_ticker_data(symbol):
    ticker = yf.Ticker(symbol)
    time.sleep(2)
    info = ticker.info
    data = {
        "price": float(ticker.fast_info.last_price),
        "eps": float(info.get("trailingEps", 0) or 0),
        "bvps": float(info.get("bookValue", 0) or 0),
        "pe": float(info.get("trailingPE", 0) or 0),
    }
    # 執行 AI 分析
    data["ai_prediction"] = get_ai_analysis(symbol, data)
    return data

def run_analysis_and_update():
    logging.info("開始執行階段四：整合 AI 快評...")
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for symbol in TICKER_LIST:
        data[symbol] = get_ticker_data(symbol)
            
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("AI 分析數據寫入完成。")

if __name__ == "__main__":
    run_analysis_and_update()
