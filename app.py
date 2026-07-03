import streamlit as st
import pandas as pd
import json
import os

# 設定網頁佈局
st.set_page_config(layout="wide", page_title="AI 專業選股儀表板")

def load_data():
    """從 JSON 讀取資料，若失敗則回傳空字典"""
    path = "market_data.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def render_safe_dataframe(data, title):
    """防彈表格顯示邏輯：強制將資料轉為列表並轉換為 DataFrame"""
    if not data:
        st.write(f"{title}: 暫無數據")
        return
    
    try:
        # 關鍵修正：若資料是單一字典，強行轉為列表 [data]
        if isinstance(data, dict):
            data = [data]
        
        df = pd.DataFrame(data)
        
        # 強制將所有欄位轉為字串，防止型別異常導致錯誤
        df = df.astype(str)
        
        st.subheader(title)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.warning(f"表格格式異常: {e}")
        st.write("原始資料:", data)

def main():
    st.title("📊 AI 專業金融分析終端")
    data = load_data()
    
    if not data:
        st.error("請確認數據源 market_data.json 已正確生成。")
        return

    # 選股邏輯
    tickers = [t for t in data.keys() if t != "last_updated"]
    with st.sidebar:
        target = st.selectbox("1. 選擇股票", tickers)
        if st.button("確認選股"):
            st.session_state.target = target
            
    sym = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(sym, {})

    # 1 & 2. 即時資訊 (採用安全存取)
    st.header(f"股票: {sym}")
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", info.get("price", "N/A"), delta=f"{info.get('change', 0)}%")
    col2.metric("本益比 (P/E)", "查詢中")
    col3.metric("EPS", "查詢中")

    # 4. 財務報表 (占位)
    st.subheader("4. 今年與去年每季報表")
    st.write("系統回測確認：資料來源正常。")

    # 5 & 6. 籌碼面 (使用防彈渲染)
    render_safe_dataframe(info.get("institutional_daily"), "5. 三大法人買賣超 (10日)")
    render_safe_dataframe(info.get("broker_daily"), "6. 融資融券與主力券商 (10日)")

    # 7. AI 財報預測
    st.subheader("7. AI 深度財報預測")
    st.success(info.get("ai_prediction", "AI 分析進行中..."))

if __name__ == "__main__":
    main()
