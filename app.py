import streamlit as st
import pandas as pd
import json
import os

# 設定頁面樣式
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def get_abs_path():
    """獲取絕對路徑，確保讀取的是正確的檔案"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")

def load_data():
    """讀取市場數據，增加路徑顯示以利除錯"""
    json_path = get_abs_path()
    if not os.path.exists(json_path):
        return None, f"檔案不存在於: {json_path}"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data, None
    except Exception as e:
        return None, str(e)

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 載入資料
    data, error = load_data()
    
    if error:
        st.error(f"讀取錯誤: {error}")
        return

    # 核心指標 (改為使用 .get 避免 KeyError)
    price = data.get("price", 0)
    st.metric("即時股價", f"{float(price):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    
    # 這裡我們不強制要求該鍵必須存在，若不存在顯示友善提示
    if "institutional_investors" in data:
        raw = data["institutional_investors"]
        try:
            # 確保資料為列表
            df_source = raw if isinstance(raw, list) else [raw]
            df = pd.DataFrame(df_source)
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製失敗: {e}")
    else:
        st.warning("目前 json 檔案中找不到 'institutional_investors' 欄位。")
        st.write("目前的鍵值有:", list(data.keys()))

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析。"))

    # 除錯區塊
    with st.expander("🔍 系統路徑與原始資料"):
        st.write("讀取路徑:", get_abs_path())
        st.json(data)

if __name__ == "__main__":
    main()
