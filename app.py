import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def render_table(info, key, title):
    # 防禦層：如果 info 為 None 或非字典，直接跳過
    if not isinstance(info, dict):
        return
    
    data = info.get(key)
    if data and isinstance(data, list):
        try:
            df = pd.DataFrame(data)
            st.subheader(title)
            st.dataframe(df.astype(str), use_container_width=True)
        except Exception as e:
            st.warning(f"{title} 渲染錯誤: {e}")
    else:
        st.write(f"{title}: 暫無籌碼數據")

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    
    if not data:
        st.info("資料讀取中，請確認 GitHub Actions 是否完成...")
        return

    # 安全獲取股票清單
    tickers = [t for t in data.keys() if t not in ["last_updated"]]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        
    # 安全獲取股票資訊
    info = data.get(target)
    if info is None:
        info = {}

    st.header(f"股票: {target}")
    
    # 強制檢查 info 結構
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(float(price) - float(prev), 2)
    
    st.metric("即時股價", f"{price} 元", delta=f"{diff} 元")
    
    # 呼叫渲染
    render_table(info, "institutional_daily", "5. 三大法人買賣超細項")
    render_table(info, "broker_daily", "6. 主力券商買賣超細項")

    st.subheader("7. AI 深度財報分析")
    st.success(info.get("ai_prediction", "AI 分析中..."))

if __name__ == "__main__":
    main()
