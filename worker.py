import os
import yfinance as yf
import requests
from openai import OpenAI

# 安全讀取環境變數 (GitHub Actions 會提供)
api_key = os.environ.get("OPENAI_API_KEY")
line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

client = OpenAI(api_key=api_key)

def run_auto_analysis(ticker="2330.TW"):
    # 抓取數據
    df = yf.download(ticker, period="1mo", progress=False)
    
    if df.empty:
        return

    # 計算技術指標
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    last_price = df['Close'].iloc[-1].item()
    
    # 讓 AI 根據數據分析
    prompt = f"股票 {ticker}, 最新價 {last_price:.2f}, 20日均線 {sma_20:.2f}。請從技術面分析其趨勢，並給出買賣觀點。"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    analysis_text = response.choices[0].message.content
    
    # 發送至 LINE
    msg = f"\n【智能投資管家報告】\n標的: {ticker}\n最新價: {last_price:.2f}\n20日均線: {sma_20:.2f}\n\n分析建議:\n{analysis_text}"
    requests.post("https://notify-api.line.me/api/notify", 
                  headers={"Authorization": f"Bearer {line_token}"}, 
                  data={"message": msg})

if __name__ == "__main__":
    run_auto_analysis("2330.TW")
