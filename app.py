import streamlit as st
import pandas as pd
import json
import os
import numpy as np

# 頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def clean_data(val):
    """
    數據過濾器：處理任何異常結構。
    將 NaN, Inf, None, 空字串 統一轉換為 0.0。
    若傳入的是列表或 Series，取出第一個有效值。
    """
    if val is None:
        return 0.0
    try:
        # 如果是列表或陣列，取第一個值
        if isinstance(val, (list, np.ndarray, pd.Series)):
            val = val[0] if len(val) > 0 else 0.0
            
        # 轉換為 float，排除無法轉換的異常
        f = float(val)
        if np.isnan(f) or np.isinf(f):
            return 0.0
        return f
    except:
        return 0.0

def load_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def main():
    data = load_data()
    
    if data is None:
        st.warning("⚠️ 數據檔案載入失敗，正在等待後端更新...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # --- 核心指標 ---
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{clean_data(data.get('price')):,.2f}", delta=f"{clean_data(data.get('change')):+.2f}")
    cols[1].metric("每股淨值", f"{clean_data(data.get('bvps')):.2f}")
    cols[2].metric("本益比", f"{clean_data(data.get('pe_ratio')):.2f}")
    cols[3].metric("10日資券比", f"{clean_data(data.get('margin_ratio')):.2f}%")
    cols[4].metric("預估 EPS", f"{clean_data(data.get('eps_forecast')):.2f}")
    
    st.divider()

    # --- 籌碼面 ---
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    # 這裡確保即使 inst_data 格式奇怪也能顯示
    try:
        df = pd.DataFrame(inst_data)
        # 強制將所有數值列轉為數值，非數值欄位轉為 0
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
        st.dataframe(df, width=1000) # 已根據警告更新為 width 參數
    except:
        st.info("籌碼數據目前無法以表格呈現，正在修正資料來源格式。")

    # --- AI 分析 ---
    st.subheader("AI 智能分析")
    st.info(data.get("ai_prediction", "暫無 AI 分析結果。"))

if __name__ == "__main__":
    main()
