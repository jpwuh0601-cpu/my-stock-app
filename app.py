import streamlit as st
import pandas as pd
import json
import os
import ast

st.set_page_config(layout="wide", page_title="AI 專業選股儀表板")

def load_data():
    path = "market_data.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def render_table(info, key, title):
    """加入字串格式反序列化功能"""
    data = info.get(key)
    
    # 處理特殊情況：如果資料是字串，嘗試將其轉換為物件
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            try:
                data = ast.literal_eval(data)
            except:
                data = None
    
    # 若為單一字典，強制轉為列表
    if isinstance(data, dict):
        data = [data]
        
    if data and isinstance(data, list):
        try:
            df = pd.DataFrame(data)
            st.subheader(title)
            # 強制字串顯示，確保不報錯
            st.dataframe(df.astype(str), use_container_width=True)
        except Exception as e:
            st.write(f"表格格式無法解析: {e}")
    else:
        st.write(f"{title}: 暫無籌碼數據 (請檢查數據格式)")

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    
    if not data:
        st.info("資料載入中，請確認 GitHub Actions 已執行完畢。")
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    sym = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(sym, {})
    
    st.header(f"股票: {sym}")
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", info.get("price", "N/A"), delta=f"{info.get('change', 0)}%")
    col2.metric("本益比", "N/A")
    col3.metric("EPS", "N/A")

    st.subheader("7. AI 深度財報預測")
    st.success(info.get("ai_prediction", "AI 分析進行中..."))

    render_table(info, "institutional_daily", "5. 三大法人買賣超 (10日)")
    render_table(info, "broker_daily", "6. 主力券商買賣超 (10日)")

if __name__ == "__main__":
    main()
