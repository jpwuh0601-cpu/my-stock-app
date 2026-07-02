import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取並強制清洗數據結構"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # 確保回傳的是字典
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("⚠️ 正在載入資料中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標顯示
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面顯示：加入空值轉型處理
    st.subheader("三大法人與籌碼數據")
    
    # 這裡的關鍵修正：如果 inst_data 為 None，強制轉為空列表 []
    inst_data = data.get("institutional_investors")
    if inst_data is None:
        inst_data = []
    
    try:
        # 強制轉換並處理可能的單一字典情況
        if isinstance(inst_data, dict):
            df = pd.DataFrame([inst_data])
        elif isinstance(inst_data, list):
            df = pd.DataFrame(inst_data)
        else:
            df = None
            
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("目前無籌碼數據。")
    except Exception:
        st.error("表格數據格式無法辨識。")

    # 新聞與分析
    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析"))

if __name__ == "__main__":
    main()
