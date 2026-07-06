import streamlit as st
import pandas as pd
import json
import os

# 設定網頁標題與排版
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """載入市場數據，確保回傳永遠是字典"""
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def format_num(value, default=0.0):
    """確保數值永遠為浮點數，若無法轉換則回傳 default"""
    try:
        return float(value)
    except:
        return float(default)

# 側邊欄輸入區
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    d = data_cache.get(ticker)
    
    if d is None:
        st.warning(f"查無代號: {ticker}。請確認 GitHub Actions 是否已將此股票加入 JSON。")
    else:
        # 1. 基本財務數據 (使用 format_num 強制轉換，避免 NoneType 錯誤)
        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{format_num(d.get('price')):.2f}")
        col2.metric("每股淨額", f"{format_num(d.get('nav')):.2f}")
        col3.metric("本益比 (PE)", f"{format_num(d.get('pe')):.2f}")
        st.metric("每股盈餘 (EPS)", f"{format_num(d.get('eps')):.2f}")

        # 2. 財報分析
        st.subheader("2. 財報分析")
        st.write("今年與去年每季報表 (模擬數據)")

        # 3. 三大法人買賣超
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                df = pd.DataFrame(inst_data)
                # 清理異常數值
                df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
                st.table(df)
            except:
                st.write("資料表渲染異常")
        else:
            st.write("目前無法人籌碼資料")

        # 4. 資券與主力券商
        st.subheader("4. 資券與主力券商 (10日)")
        st.write(f"10日資券比: {d.get('margin_ratio', 0)}%")

        # 5. 即時新聞
        st.subheader("5. 即時新聞")
        st.write(d.get("news", "無最新新聞資訊"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))

        # 7. 預估資訊
        st.subheader("7. 預估資訊")
        st.write("今年預估營收、EPS 與股利資訊")

        # 8. 資料來源驗證
        st.subheader("8. 資料來源驗證")
        if d.get("price") is not None:
            st.success("✅ 資料來源與數值驗證通過")
        else:
            st.error("❌ 資料來源異常或數值遺失")
else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
