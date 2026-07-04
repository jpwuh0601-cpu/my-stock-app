import streamlit as st
import json
import os
import plotly.express as px
import yfinance as yf
import logging

# 設定日誌以利除錯
logging.basicConfig(level=logging.INFO)

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 讀取 JSON 數據
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"讀取 JSON 失敗: {e}")
    return {}

data = load_data()

# --- 手動查詢區塊 ---
st.subheader("🔍 手動查詢股票")
custom_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="請輸入代號並按下 Enter")

# 決定要查詢的目標
target_ticker = custom_ticker if custom_ticker else "2330.TW"

# 強制執行即時查詢
try:
    ticker_obj = yf.Ticker(target_ticker)
    info = ticker_obj.info
    
    # 檢查是否確實抓到價格 (避免 Yahoo API 回傳空物件)
    if "currentPrice" not in info and "regularMarketPrice" in info:
        info["currentPrice"] = info["regularMarketPrice"]
        
    if "currentPrice" in info:
        st.success(f"已成功載入 {target_ticker} 資訊")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
        c2.metric("本益比", f"{info.get('forwardPE', 0) or 0:.2f}")
        c3.metric("EPS", f"{info.get('trailingEps', 0) or 0:.2f}")
        
        # 顯示 AI 分析 (來自 JSON 備份)
        if target_ticker in data:
            st.subheader("🤖 AI 顧問分析")
            st.info(data[target_ticker].get("ai_prediction", "AI 分析數據待命中..."))
        else:
            st.warning("此標的目前未在自動化清單中，僅顯示即時市場數據。")

        # 繪製走勢圖
        hist = ticker_obj.history(period="1mo")
        if not hist.empty:
            fig = px.line(hist, y="Close", title=f"{target_ticker} 近期走勢")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("暫無近一個月歷史數據")
            
    else:
        st.error(f"無法取得代號 '{target_ticker}' 的市場資訊，請確認輸入格式是否正確（必須包含 .TW 等後綴）。")

except Exception as e:
    logging.error(f"YFinance 查詢失敗: {e}")
    st.error("系統連線至 Yahoo Finance 發生異常，請確認網絡環境。")
