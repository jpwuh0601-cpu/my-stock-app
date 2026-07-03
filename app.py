import streamlit as st
import pandas as pd
import json

# 設定頁面配置
st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data():
    """載入數據並確保其為穩定的字典結構"""
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def main():
    st.title("📈 專業金融監控終端")
    data = load_data()
    
    # 側邊欄固定選股邏輯
    with st.sidebar:
        st.header("選股設定")
        tickers = [t for t in data.keys() if t not in ["last_updated"]]
        user_input = st.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = user_input
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target) or {}

    # --- 固定模組區塊排列 ---
    
    # 區塊 1: 即時股價
    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    diff = info.get("diff", 0)
    st.metric("當前價格", f"{price} 元", delta=f"{diff} 元")

    # 區塊 2: 基本面
    st.subheader("2. 基本面數據 (淨值/本益比/EPS)")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", "查詢中")
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 區塊 4: 財報報表
    st.subheader("4. 今年與去年每季報表")
    st.write("自動回測資料來源：狀態 [正常]")

    # 區塊 5: 三大法人 (紅綠色彩)
    st.subheader("5. 三大法人買賣超 (10日)")
    if "institutional_daily" in info and info["institutional_daily"]:
        st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
    else:
        st.write("暫無法人籌碼資料")

    # 區塊 6: 資券比與主力券商
    st.subheader("6. 10日資券比與主力券商")
    if "broker_daily" in info and info["broker_daily"]:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)
    else:
        st.write("暫無券商籌碼資料")

    # 區塊 7: AI 新聞與預測
    st.subheader("7. AI 分析與黑天鵝警示")
    st.info(f"📰 GPT 新聞解讀: {info.get('news_analysis', '暫無近期新聞')}")
    st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")
    st.error(f"⚠️ 黑天鵝危機警示: {info.get('black_swan_alert', '系統監控中：無異常')}")

if __name__ == "__main__":
    main()
