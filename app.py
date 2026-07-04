import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import requests
import os
import datetime

# --- AI 分析核心邏輯 ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        if not api_key:
            return f"【{ticker_symbol} 最新標題】: {latest_news} (提示: 請於 App Settings 設定 API Key 以啟動 AI 分析)"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{latest_news}。請用一句話簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析引擎暫時無法連線: {e}"

# --- 前端介面邏輯 ---
st.set_page_config(layout="wide", page_title="即時金融查詢終端")
st.title("🔍 專業金融即時查詢終端")

# 手動輸入查詢區
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)", placeholder="輸入代號後按下 Enter")

if input_ticker:
    with st.spinner(f"正在即時聯網分析 {input_ticker}..."):
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            
            # 檢查代號有效性
            if "currentPrice" not in info:
                st.error("查無此標的，請確認代號是否正確 (台股請加 .TW)")
            else:
                # 顯示基本指標
                col1, col2, col3 = st.columns(3)
                col1.metric("即時價格", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("EPS (每股盈餘)", info.get("trailingEps", "N/A"))
                col3.metric("本益比 (PE)", info.get("forwardPE", "N/A"))
                
                # 顯示 AI 分析
                st.subheader("🤖 AI 市場解讀")
                st.info(get_ai_analysis(input_ticker))
                
                # 顯示走勢圖
                st.subheader("📈 近期走勢")
                hist = ticker.history(period="1mo")
                st.line_chart(hist['Close'])
                
        except Exception as e:
            st.error(f"查詢失敗: {e}")
            
st.sidebar.markdown("### 系統說明")
st.sidebar.write("本系統為「純即時查詢模式」，完全聯網讀取 Yahoo Finance 資料，無須依賴背景排程。")
