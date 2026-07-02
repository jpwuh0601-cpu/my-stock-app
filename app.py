import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    json_path = "market_data.json"
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    data = load_data()
    if not data:
        st.warning("⚠️ 數據載入中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 顯示即時股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面資料處理
    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")
    
    # 【關鍵修正】：無論 raw 是什麼，強制轉為列表 List
    try:
        if isinstance(raw, dict):
            # 如果是單一字典，放入列表中
            df_source = [raw]
        elif isinstance(raw, list):
            # 如果已經是列表，直接使用
            df_source = raw
        else:
            df_source = []
            
        if df_source:
            # 建立 DataFrame 並顯式指定索引，徹底避免 scalar values 錯誤
            df = pd.DataFrame(df_source)
            # 強制處理所有列為字串，避免 Pandas 類型推斷崩潰
            df = df.astype(str)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"表格解析失敗: {e}")
        st.write("原始資料內容:", raw)

    # AI 分析
    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析。"))

if __name__ == "__main__":
    main()
