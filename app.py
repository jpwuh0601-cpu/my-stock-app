import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("⚠️ 數據檔案尚未生成或格式錯誤，請稍候。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標 (確保即使 key 不存在也不會報錯)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：絕對防禦顯示邏輯
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors")
    
    # 防禦：如果不是列表或字典，直接跳過表格顯示
    if isinstance(inst_data, (list, dict)):
        try:
            # 強制轉為列表結構，確保 DataFrame 能正確解析
            df_source = inst_data if isinstance(inst_data, list) else [inst_data]
            df = pd.DataFrame(df_source)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"表格格式異常，無法解析。")
            st.write("原始數據結構:", inst_data)
    else:
        st.info("目前無籌碼數據。")

    # 新聞與預測
    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據"))
    st.subheader("最新市場新聞")
    st.write(data.get("news", "暫無新聞"))

if __name__ == "__main__":
    main()
