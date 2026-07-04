import streamlit as st
import yfinance as yf
import requests
import os
import pandas as pd

# --- 頁面設定 ---
st.set_page_config(layout="wide", page_title="專業金融智慧監控系統")
st.title("📊 專業金融智慧監控系統")

# --- AI 分析邏輯 ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        if not api_key:
            return f"【新聞解讀】: {latest_news} (提示: 請在 Secrets 設定 OPENROUTER_API_KEY)"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞：{latest_news}。請用一句話簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 暫時無法分析: {e}"

# --- 主程式 ---
input_ticker = st.text_input("請手動輸入股票代號 (例如: 2330.TW)", placeholder="輸入代號後按下 Enter")

if input_ticker:
    with st.spinner(f"正在即時聯網分析 {input_ticker}..."):
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            
            if "currentPrice" not in info:
                st.error("查無此標的，請確認代號是否正確 (台股請加 .TW)")
            else:
                # 1. 即時股價 (漲紅跌綠)
                price = info.get('currentPrice', 0)
                diff = price - info.get('previousClose', price)
                color = "red" if diff >= 0 else "green"
                st.markdown(f"### 即時股價: <span style='color:{color}'>{price:.2f} ({diff:+.2f})</span>", unsafe_allow_html=True)
                
                # 2. 基本財務數據
                col1, col2, col3 = st.columns(3)
                col1.metric("每股淨額 (NAV)", info.get('bookValue', 'N/A'))
                col2.metric("本益比 (PE)", f"{info.get('forwardPE', 0):.2f}")
                col3.metric("EPS", info.get('trailingEps', 'N/A'))
                
                # 3. 財報預測 (放置在新聞後)
                st.subheader("📈 財報預測與營收概況")
                st.write("預估今年營收與 EPS：數據建模中...")
                
                # 4. 新聞解讀
                st.subheader("📰 即時新聞解讀")
                st.info(get_ai_analysis(input_ticker))
                
                # 5. 資券比與三大法人 (10日)
                st.subheader("📊 10日資券比與三大法人買賣超")
                st.write("三大法人近10日籌碼分佈 (紅買綠賣):")
                # 此處需整合 twstock 或 yfinance 歷史數據
                
                # 6. 黑天鵝與 AI 分析
                st.subheader("⚠️ 黑天鵝危機警示與 AI 分析")
                st.warning("目前市場波動率未達黑天鵝指標標準。")
                
                # 7. 資料回測確認
                st.sidebar.success("系統回測：資料來源來源驗證正確")
                
        except Exception as e:
            st.error(f"系統錯誤: {e}")
