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

def render_table(info, key, title):
    """檢查 key 是否存在，且確實有資料"""
    data = info.get(key)
    if data and isinstance(data, list) and len(data) > 0:
        try:
            df = pd.DataFrame(data)
            st.subheader(title)
            st.dataframe(df.astype(str), width=None)
        except Exception as e:
            st.write(f"表格繪製失敗: {e}")
    else:
        st.write(f"{title}: 暫無籌碼資料 (請等待 worker.py 完成更新)")

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("尚未載入資料，請確認 GitHub Actions 是否執行成功。")
        return

    # 過濾系統欄位
    tickers = [t for t in data.keys() if t not in ["last_updated"]]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    current_target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(current_target, {})
    
    st.header(f"股票代號: {current_target}")
    
    # 顯示 AI 分析 (檢查是否有 ai_prediction 或其他欄位)
    if "ai_prediction" in info:
        st.info(f"AI 分析: {info['ai_prediction']}")
    else:
        st.write(f"目前價格: {info.get('price', '未知')}")
        
    # 顯示表格
    render_table(info, "institutional_daily", "三大法人買賣超")
    render_table(info, "broker_daily", "主力券商買賣超")

if __name__ == "__main__":
    main()
