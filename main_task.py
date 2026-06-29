import os
import yfinance as yf
import pandas_ta as ta
import openai
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 1. 設定環境變數 (確保 GitHub Secrets 已設定)
openai.api_key = os.getenv("OPENAI_API_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
user_id = os.getenv("USER_ID")

def get_market_analysis(ticker="2330.TW"):
    # 抓取台股資料
    df = yf.download(ticker, period="3mo")
    df['RSI'] = ta.rsi(df['Close'], length=14)
    last_rsi = df['RSI'].iloc[-1]
    
    # 技術分析警示判斷
    rsi_alert = "✅ 技術指標正常"
    if last_rsi < 30:
        rsi_alert = "⚠️ [黑天鵝警示] RSI 過低 (超賣)，建議留意風險！"
    elif last_rsi > 70:
        rsi_alert = "⚠️ [市場警示] RSI 過高 (超買)，注意回調。"

    # AI 決策引擎 (將 RSI 數值丟給 GPT 分析)
    prompt = f"個股 {ticker} 目前 RSI 指標為 {last_rsi:.2f}。請從技術分析角度，並結合國際金融情勢，給出一個精簡的投資建議與黑天鵝預警。"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}]
        )
        ai_analysis = response.choices[0].message.content
    except Exception as e:
        ai_analysis = "AI 分析目前無法取得。"

    return f"{rsi_alert}\n\n【AI 分析】\n{ai_analysis}"

# 執行任務並推送到 LINE
if __name__ == "__main__":
    message = get_market_analysis("2330.TW")
    line_bot_api.push_message(user_id, TextSendMessage(text=message))
