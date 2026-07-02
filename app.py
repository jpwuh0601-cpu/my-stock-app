import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("正在載入資料中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：強制清洗，將所有數據轉為「字串」再進入表格
    st.subheader("三大法人與籌碼數據")
    raw_inst = data.get("institutional_investors")
    
    try:
        if isinstance(raw_inst, list) and len(raw_inst) > 0:
            # 關鍵步驟：強制將每一個項目轉換為「純文字字典」
            clean_list = []
            for item in raw_inst:
                if isinstance(item, dict):
                    clean_list.append({str(k): str(v) for k, v in item.items()})
            
            if clean_list:
                df = pd.DataFrame(clean_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("籌碼數據目前無法解析。")
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"表格顯示錯誤: {e}")

    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無數據"))

if __name__ == "__main__":
    main()
