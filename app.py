import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據，若失敗則回傳空字典"""
    json_path = "market_data.json"
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    data = load_data()
    
    if not data:
        st.warning("⚠️ 正在載入或等待數據更新中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標顯示
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面：核心容錯邏輯
    st.subheader("🏦 三大法人與籌碼數據")
    
    # 取得數據，強制預設為空列表，避免 None 導致的 TypeError
    inst_data = data.get("institutional_investors")
    
    if inst_data is None:
        inst_data = []
    
    # 如果傳入的是單一字典，強轉為列表
    if isinstance(inst_data, dict):
        inst_data = [inst_data]
    
    # 檢查是否為正確的列表結構
    if isinstance(inst_data, list):
        try:
            # 使用 DataFrame 轉換，如果資料為空會產生空的 DataFrame
            df = pd.DataFrame(inst_data)
            
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("目前無籌碼數據。")
        except Exception as e:
            st.error(f"表格格式解析異常: {e}")
    else:
        st.info("資料格式不符合預期。")

    # AI 分析區塊
    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析結果。"))

    # 除錯區域
    with st.expander("🔍 除錯：查看原始 JSON 資料"):
        st.json(data)

if __name__ == "__main__":
    main()
