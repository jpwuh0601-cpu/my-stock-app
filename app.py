import streamlit as st
import pandas as pd
import json
import os

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    """獲取絕對路徑以確保讀取成功"""
    # 取得 app.py 所在的絕對目錄
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案讀取失敗: {e}")
            return {}
    else:
        # 如果找不到檔案，在頁面上顯示路徑，協助除錯
        st.error(f"找不到數據檔。請檢查檔案是否位於: {file_path}")
        return {}

def main():
    data = load_data()
    if not data:
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心財務指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}", delta=f"{float(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面分析：強型態轉換
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if inst_data:
        df = pd.DataFrame(inst_data)
        # 顯示表格
        st.dataframe(df, use_container_width=True)
    else:
        st.write("暫無法人數據")

if __name__ == "__main__":
    main()
