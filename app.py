import streamlit as st
import json
import os

# 設定頁面，降低瀏覽器載入負擔
st.set_page_config(page_title="金融儀表板", layout="centered")

def load_data(filepath):
    """防禦性讀取 JSON 數據"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title("📈 金融儀表板 (極簡版)")
    
    # 載入數據
    data = load_data("market_data.json")
    
    # 輸入選股
    target = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if "error" in data:
        st.error(f"檔案讀取異常: {data['error']}")
        return

    # 顯示數據
    info = data.get(target)
    
    if not info:
        st.info("尚未搜尋到資料，請確認股票代號或等待自動化任務 (GitHub Actions) 更新。")
    else:
        st.header(f"股票代號: {target}")
        
        # 顯示核心數據
        st.metric("即時股價", f"{info.get('price', 0)} 元")
        
        st.subheader("AI 分析摘要")
        st.write(info.get('ai_prediction', '分析中...'))
        
        if st.checkbox("顯示原始資料"):
            st.json(info)

if __name__ == "__main__":
    main()
