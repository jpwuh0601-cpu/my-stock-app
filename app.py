import streamlit as st
import pandas as pd
import json
import os

# 設定頁面樣式
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

def ensure_string_dataframe(data_list):
    """將所有數據強制轉為字串，防止 Pandas 類型推斷錯誤"""
    if not data_list:
        return pd.DataFrame()
    
    # 強制將每個項目內的數值轉為字串，確保二維結構統一
    clean_data = []
    for item in data_list:
        if isinstance(item, dict):
            clean_data.append({str(k): str(v) for k, v in item.items()})
    
    return pd.DataFrame(clean_data)

def main():
    data = load_data()
    
    if not data:
        st.warning("⚠️ 正在載入或等待數據更新中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：增加 float 轉換保護
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：使用統一格式化函數
    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors", [])
    
    try:
        # 將輸入正規化
        if isinstance(raw, dict):
            data_list = [raw]
        elif isinstance(raw, list):
            data_list = raw
        else:
            data_list = []
            
        df = ensure_string_dataframe(data_list)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"表格顯示異常: {e}")

    # AI 分析區塊
    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析結果。"))

    # 除錯區域
    with st.expander("查看原始 JSON 資料"):
        st.json(data)

if __name__ == "__main__":
    main()
