import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def render_safe_df(info, key, title):
    """徹底安全的表格顯示：檢查 key 是否存在且非 None"""
    # 使用 .get() 安全存取，如果不存在則返回 None
    data = info.get(key)
    
    if data:
        try:
            df = pd.DataFrame(data)
            # 將所有數據強制轉為字串，避免型別衝突
            df = df.astype(str)
            st.subheader(title)
            st.dataframe(df, width=None)
        except Exception as e:
            st.write(f"{title}: 格式轉換錯誤 ({e})")
    else:
        st.write(f"{title}: 暫無籌碼細項數據 (數據尚未寫入 JSON)")

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("資料載入中或數據尚未生成，請稍候...")
        return

    # 過濾掉最後更新時間欄位
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    current_target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(current_target, {})
    
    st.subheader(f"分析目標: {current_target}")
    
    # 檢查並顯示 AI 預測（這是 json 中一定有的欄位）
    st.info(f"AI 分析摘要: {info.get('ai_prediction', '無分析資料')}")
    
    # 顯示表格，使用安全渲染器
    render_safe_df(info, "institutional_daily", "三大法人 10 日買賣超")
    render_safe_df(info, "broker_daily", "主力券商 10 日買賣超")

if __name__ == "__main__":
    main()
