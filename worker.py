import os
import json
import requests
import yfinance as yf
from datetime import datetime

def save_to_journal(ticker_symbol, report_content):
    """將每日分析存入 journal.json"""
    journal_file = "journal.json"
    
    # 讀取現有日記
    data = []
    if os.path.exists(journal_file):
        with open(journal_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []

    # 新增今日紀錄
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ticker": ticker_symbol,
        "content": report_content
    }
    data.append(entry)

    # 寫回檔案
    with open(journal_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_smart_report():
    ticker_symbol = "^TWII"
    ticker = yf.Ticker(ticker_symbol)
    
    # 簡單分析邏輯
    news = ticker.news
    news_summary = "\n".join([n.get('title', '') for n in news[:3]]) if news else "今日無重大新聞。"
    
    report = f"市場分析結果：\n{news_summary}"
    
    # 存檔
    save_to_journal(ticker_symbol, report)
    
    # 發送 LINE 通知
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if token:
        requests.post("https://notify-api.line.me/api/notify", 
                      headers={"Authorization": f"Bearer {token}"}, 
                      data={"message": f"\n📝 投資日記已更新！\n{report}"})

if __name__ == "__main__":
    run_smart_report()
