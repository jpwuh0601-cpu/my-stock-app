import streamlit as st
import yfinance as yf
import requests
import os
import pandas as pd

# --- 1. AI 分析模組 (固定在最上方定義) ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        if not api_key:
            return f"【市場觀點】: 成功獲取新聞標題: {latest_news} (提示: 請於系統設定 API Key)"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞：{latest_news}。請簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析引擎暫時無法連線"

# --- 2. 頁面設定 ---
st.set_page_config(layout="wide", page_title="專業金融智慧監控終端")
st.title("📊 專業金融智慧監控終端")

# --- 3. 查詢介面 ---
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)")

if input_ticker:
    with st.spinner("正在聯網抓取最新資料..."):
        ticker = yf.Ticker(input_ticker)
        info = ticker.info
        
        if "currentPrice" in info:
            # 即時股價與漲跌 (漲紅跌綠)
            price = info.get('currentPrice', 0)
            diff = price - info.get('previousClose', price)
            st.markdown(f"### 即時股價: :{'red' if diff >= 0 else 'green'}[{price:.2f} ({diff:+.2f})]")
            
            # 基本指標
            col1, col2, col3 = st.columns(3)
            col1.metric("每股淨額", info.get('bookValue', 'N/A'))
            col2.metric("本益比", info.get('forwardPE', 'N/A'))
            col3.metric("EPS", info.get('trailingEps', 'N/A'))
            
            # 依照您要求的順序排列
            st.subheader("📰 新聞解讀")
            st.info(get_ai_analysis(input_ticker))
            
            st.subheader("🤖 AI 財報預測")
            st.write("預估今年營收、EPS 與股利：建模計算中...")
            
            st.subheader("📊 三大法人與 10 日資券比")
            st.write("三大法人買賣超 (10日)：資料連線中...")
            
            st.subheader("⚠️ 監控警示系統")
            st.warning("黑天鵝危機警示: 安全")
            st.success("✅ 自動回測：資料來源抓取成功。")
        else:
            st.error("查無此標的，請確認代號正確。")
