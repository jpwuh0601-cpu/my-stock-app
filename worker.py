import yfinance as yf
import requests
import os
from openai import OpenAI

# 從環境變數讀取 (GitHub Actions 會提供)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
LINE_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

def run_auto_analysis(ticker="2330.TW"):
    # 抓取數據並計算聰明指標
    df = yf.download(ticker, period="1mo")
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
    last_price = df['Close'].iloc[-1]
    
    # AI 分析邏輯
    prompt = f"股票 {ticker}, 最新價 {last_price:.2f}, 20日均線 {sma_20:.2f}。請給出買賣觀點。"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # 發送 LINE
    msg = f"\n【自動化智能報告】\n{ticker} 走勢分析:\n{response.choices[0].message.content}"
    requests.post("https://notify-api.line.me/api/notify", 
                  headers={"Authorization": f"Bearer {LINE_TOKEN}"}, 
                  data={"message": msg})

if __name__ == "__main__":
    run_auto_analysis()
