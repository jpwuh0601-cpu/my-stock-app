import streamlit as st
import json
import os

st.set_page_config(layout="wide")

def load_data(filepath):
    if not os.path.exists(filepath):
        st.error(f"檔案不存在: {filepath}")
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"解析 JSON 失敗: {e}")
        return {}

def main():
    st.title("📈 AI 金融監控終端")
    
    data = load_data("market_data.json")
    
    # 除錯：查看目前 JSON 中到底有什麼 Key
    if st.sidebar.checkbox("顯示除錯資料清單"):
        st.sidebar.write("目前資料庫 Key:", list(data.keys()))

    with st.sidebar:
        ticker_input = st.text_input("輸入股票代號 (例如: 1301)", "1301")
        
        if st.button("確認選股"):
            # 自動補全邏輯
            target = ticker_input if ".TW" in ticker_input else f"{ticker_input}.TW"
            st.session_state.target = target
            st.rerun()

    target = st.session_state.get("target", "2330.TW")
    info = data.get(target)

    if not info:
        st.error(f"找不到標的: {target}。請檢查 market_data.json 是否確實包含此代號。")
        st.info("提示：GitHub Actions 執行完畢後，請確認生成的 JSON 是否為空。")
    else:
        st.success(f"成功載入: {target}")
        st.metric("股價", info.get("price", "無資料"))
        st.write("AI 分析:", info.get("ai_prediction", "無"))

if __name__ == "__main__":
    main()
