import os
import yfinance as yf
import pandas_ta as ta
import openai
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 設定 OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_market(ticker_symbol):
    # 1. 取得數據與技術指標
    df = yf.download(ticker_symbol, period="1mo")
    df['RSI'] = ta.rsi(df['Close'], length=14)
    current_rsi = df['RSI'].iloc[-1]
    
    # 2. 技術指標警示邏輯
    alert_msg = ""
    if current_rsi < 30:
        alert_msg = "⚠️ [技術警示] RSI 過低 (超賣)，可能反彈。"
    elif current_rsi > 70:
        alert_msg = "⚠️ [技術警示] RSI 過高 (超買)，注意回調。"

    # 3. 簡單模擬新聞情緒 (實際應用可接爬蟲)
    news_sentiment = "市場情緒目前平穩，無重大黑天鵝跡象。"
    
    # 4. GPT 綜合分析
    prompt = f"個股 {ticker_symbol}, RSI: {current_rsi:.2f}, 新聞情緒: {news_sentiment}。請給予投資分析與黑天鵝風險評估。"
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    ai_analysis = response.choices[0].message.content

    return f"{alert_msg}\n\n{ai_analysis}"

# 發送通知
line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
report = analyze_market("2330.TW")
line_bot_api.push_message(os.getenv("USER_ID"), TextSendMessage(text=report))
