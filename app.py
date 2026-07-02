import streamlit as st
import pandas as pd
import json
import os

# 設定頁面樣式
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def main():
    data = load_data()
    
    if not data:
        st.warning("⚠️ 數據檔案載入中，請稍候...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標 (顯示股價)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面數據
    st.subheader("🏦 三大法人籌碼分析")
    inst_data = data.get("institutional_investors")
    
    try:
        if isinstance(inst_data, list) and len(inst_data) > 0:
            df = pd.DataFrame(inst_data)
            # 將欄位名稱進行繁體優化 (如果需要)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"表格顯示錯誤: {e}")

    # AI 分析區塊
    st.subheader("🤖 AI 智能預測")
    st.success(data.get("ai_prediction", "暫無 AI 分析。"))

    # 原始資料除錯
    with st.expander("查看原始 JSON"):
        st.json(data)

if __name__ == "__main__":
    main()
