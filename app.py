import streamlit as st
import yfinance as yf
import requests
import os

# --- 頁面設定 ---
st.set_page_config(layout="wide", page_title="即時金融查詢終端")
st.title("🔍 專業金融即時查詢終端")

# --- AI 分析邏輯 ---
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        if not api_key:
            return f"【最新新聞】: {latest_news} (提示: 請在 Streamlit Secrets 設定 OPENROUTER_API_KEY)"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{latest_news}。請用一句話簡短總結市場觀點。"}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 暫時無法分析: {e}"

# --- 使用 Form 來確保輸入完整 ---
with st.form(key='ticker_form'):
    input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)")
    submit_button = st.form_submit_button(label='開始分析')

if submit_button and input_ticker:
    with st.spinner(f"正在即時聯網分析 {input_ticker}..."):
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            
            if "currentPrice" not in info:
                st.error("查無此標的，請確認代號是否正確 (台股請加 .TW)")
            else:
                # 顯示即時指標
                col1, col2, col3 = st.columns(3)
                col1.metric("即時價格", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("EPS", info.get("trailingEps", "N/A"))
                col3.metric("本益比", info.get("forwardPE", "N/A"))
                
                # 顯示 AI 分析
                st.subheader("🤖 AI 市場解讀")
                st.info(get_ai_analysis(input_ticker))
                
                # 顯示趨勢圖
                st.subheader("📈 近期走勢")
                hist = ticker.history(period="1mo")
                if not hist.empty:
                    st.line_chart(hist['Close'])
                else:
                    st.warning("查無歷史成交資訊。")
        except Exception as e:
            st.error(f"系統發生錯誤: {e}")
