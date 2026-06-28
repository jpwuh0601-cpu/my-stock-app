import os
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime

def get_market_news():
    """抓取市場關鍵新聞摘要"""
    try:
        # 使用 yfinance 抓取大盤資訊
        ticker = yf.Ticker("^TWII")
        news = ticker.news
        if not news:
            return "目前無即時重大財經新聞。"
        
        # 提取前兩則新聞標題作為摘要
        summary = "\n".join([f"- {n['title']}" for n in news[:2]])
        return summary
    except Exception as e:
        return f"新聞抓取異常: {e}"

def run_smart_report():
    """執行智慧晨報任務"""
    try:
        # 1. 基礎健檢
        data = yf.download("^TWII", period="2d")
        change = data['Close'].pct_change().iloc[-1]
        status = "穩定" if change > -0.02 else "⚠️ 風險警告"
        
        # 2. 獲取新聞
        news_summary = get_market_news()
        
        # 3. 發送 LINE
        token = os.getenv("LINE_NOTIFY_TOKEN")
        if token:
            msg = (f"\n🌅 每日智慧晨報 ({datetime.now().strftime('%Y-%m-%d')})\n"
                   f"狀態: {status}\n\n"
                   f"關鍵市場動態:\n{news_summary}")
            requests.post("https://notify-api.line.me/api/notify", 
                          headers={"Authorization": f"Bearer {token}"}, 
                          data={"message": msg})
    except Exception as e:
        print(f"任務執行錯誤: {e}")

if __name__ == "__main__":
    run_smart_report()
