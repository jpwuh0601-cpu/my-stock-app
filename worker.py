import os
import requests
import yfinance as yf
from datetime import datetime

def get_market_sentiment():
    """抓取市場數據並產出摘要"""
    try:
        # 抓取台股大盤資料
        ticker = yf.Ticker("^TWII")
        data = ticker.history(period="5d")
        news = ticker.news
        
        if data.empty:
            return "市場數據讀取失敗。"
        
        # 計算簡單的技術趨勢
        last_price = data['Close'].iloc[-1]
        change = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100
        
        # 整理新聞摘要 (取前兩則)
        news_summary = ""
        if news:
            news_summary = "\n📰 今日頭條：\n" + "\n".join([f"- {n['title']}" for n in news[:2]])
        
        status = "穩定" if change > -1 else "⚠️ 風險警告"
        
        msg = (f"📊 每日股市健檢 ({datetime.now().strftime('%Y-%m-%d')})\n"
               f"指數收盤: {last_price:.2f} ({change:+.2f}%)\n"
               f"市場狀態: {status}\n"
               f"{news_summary}")
        return msg
        
    except Exception as e:
        return f"健檢系統異常：{str(e)}"

def send_to_line(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    requests.post("https://notify-api.line.me/api/notify", 
                  headers=headers, data={"message": message})

if __name__ == "__main__":
    content = get_market_sentiment()
    send_to_line(content)
