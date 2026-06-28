import os
import json
import yfinance as yf
from openai import OpenAI
from datetime import datetime

# 初始化 OpenAI 客戶端，API Key 會從 GitHub Secrets 自動抓取
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculate_technical_indicators(ticker_symbol):
    """計算 RSI 與 MACD 等技術指標"""
    df = yf.download(ticker_symbol, period="3mo", interval="1d")
    
    # 計算 RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 計算 MACD
    ema12 = df['Close'].ewm(span=12).mean()
    ema26 = df['Close'].ewm(span=26).mean()
    df['MACD'] = ema12 - ema26
    
    return df.iloc[-1]

def get_ai_analysis(news_list, indicators):
    """呼叫 OpenAI 進行市場分析"""
    prompt = f"請擔任專業財經分析師。根據最近的新聞標題: {news_list}，以及技術指標 RSI={indicators['RSI']:.2f}, MACD={indicators['MACD']:.2f}，提供市場情緒評估與操作策略建議。"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_smart_report():
    """執行分析並儲存至 journal.json"""
    ticker_symbol = "^TWII"  # 加權指數
    ticker = yf.Ticker(ticker_symbol)
    
    # 獲取指標與新聞
    indicators = calculate_technical_indicators(ticker_symbol)
    news = [n['title'] for n in ticker.news[:3]]
    
    # 取得 AI 分析內容
    analysis = get_ai_analysis(news, indicators)
    
    # 準備儲存資料
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "analysis": analysis
    }
    
    journal_file = "journal.json"
    data = []
    
    # 讀取現有資料
    if os.path.exists(journal_file):
        with open(journal_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
                
    # 加入新紀錄
    data.append(entry)
    
    # 寫回檔案
    with open(journal_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"分析完成，紀錄已更新至 {journal_file}")

if __name__ == "__main__":
    run_smart_report()
