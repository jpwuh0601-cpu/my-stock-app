import os
import requests
import twstock
import pandas as pd
import logging
import json
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定日誌紀錄格式，方便在 GitHub Actions 查看執行狀況
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 從環境變數讀取金鑰 (配合 Streamlit/GitHub Secrets 環境)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
WATCHLIST = os.getenv("WATCHLIST", "2330,2881,2603,2454").split(",")

# 初始化 OpenAI 客戶端 (使用 OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
) if OPENAI_API_KEY else None

def get_fundamental_data(ticker):
    """取得個股基本面數據"""
    try:
        stock_obj = yf.Ticker(f"{ticker}.TW")
        info = stock_obj.info
        return {"EPS": info.get("trailingEps", "N/A"), "PE_Ratio": info.get("trailingPE", "N/A")}
    except:
        return {"EPS": "N/A", "PE_Ratio": "N/A"}

def fetch_stock_data(ticker):
    """抓取技術與基本面數據，並包含7日趨勢記憶"""
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(datetime.now().year, datetime.now().month)
        df = pd.DataFrame(data).tail(10)
        
        current_price = df['close'].iloc[-1]
        price_trend = df['close'].pct_change().tail(7).mean() * 100
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=7).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        fundamentals = get_fundamental_data(ticker)
        
        return {
            "ticker": ticker, 
            "price": current_price, 
            "7day_trend": f"{price_trend:.2f}%",
            "rsi": f"{rsi:.2f}",
            "eps": fundamentals["EPS"],
            "pe": fundamentals["PE_Ratio"]
        }
    except Exception as e:
        logging.error(f"數據擷取異常 {ticker}: {str(e)}")
        return {"ticker": ticker, "error": "數據異常"}

def get_ai_insight(report_data):
    """AI 深度決策分析"""
    if not client: return "AI 分析功能未配置 API Key"
    
    prompt = f"""
    請擔任專業投資顧問，根據以下數據進行深度市場分析：
    {json.dumps(report_data, ensure_ascii=False)}
    要求：請檢查 PE 與 EPS 趨勢，針對表現異常的股票給予警示，並總結市場狀況。
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析發生錯誤: {str(e)}"

def send_line_message(content):
    """透過 LINE Notify 推送分析結果"""
    if not LINE_TOKEN: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": f"\n{content}"}
    requests.post(url, headers=headers, data=payload)

if __name__ == "__main__":
    logging.info("開始每日自動化分析任務...")
    report_data = [fetch_stock_data(t) for t in WATCHLIST]
    ai_summary = get_ai_insight(report_data)
    send_line_message(ai_summary)
    logging.info("分析任務完成。")
