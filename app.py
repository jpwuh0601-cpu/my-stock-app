import streamlit as st
import yfinance as yf
import requests
import os
import json

# --- 1. 資料讀取 ---
def get_stock_metrics(ticker_symbol):
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(ticker_symbol, {})
    return {}

# --- 2. 頁面設定 ---
st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# --- 3. 查詢介面 ---
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)")

if input_ticker:
    ticker = yf.Ticker(input_ticker)
    info = ticker.info
    metrics = get_stock_metrics(input_ticker)
    
    if "currentPrice" in info:
        # A. 即時股價顯示
        price = info.get('currentPrice', 0)
        diff = price - info.get('previousClose', price)
        st.markdown(f"### 即時股價: :{'red' if diff >= 0 else 'green'}[{price:.2f} ({diff:+.2f})]")
        
        # B. 財務指標矩陣
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨額", f"{info.get('bookValue', 0):.2f}")
        col2.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
        col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
        
        # C. 籌碼與資券分析 (視覺化呈現)
        st.subheader("📊 法人籌碼與資券分析")
        chip = metrics.get('chip_data', {'資券比': 0, '法人買賣超': 0})
        buy_sell = chip.get('法人買賣超', 0)
        
        c1, c2 = st.columns(2)
        c1.metric("法人買賣超", buy_sell, delta_color="normal")
        c2.metric("10日資券比", f"{chip.get('資券比', 0)}%")
        
        # D. AI 顧問報告
        st.subheader("🤖 AI 顧問深度分析")
        ai_insight = metrics.get('ai_insight', "AI 正在進行深度財報評估...")
        st.success(ai_insight)
        
        # E. 風險監控與回測
        st.subheader("⚠️ 監控警示系統")
        alert_status = metrics.get('black_swan', "檢查中...")
        st.warning(f"當前狀態: {alert_status}")
        st.caption("✅ 自動回測系統：數據源更新時間 - " + metrics.get('last_updated', '未知'))
    else:
        st.error("查無此標的資訊，請檢查代號是否正確。")
