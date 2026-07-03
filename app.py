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
    # 這裡加入多重防禦：確保 info 是字典且 key 存在
    if not isinstance(info, dict):
        return
    
    data = info.get(key)
    if data and isinstance(data, list):
        try:
            df = pd.DataFrame(data)
            st.subheader(title)
            st.dataframe(df.astype(str), use_container_width=True)
        except Exception as e:
            st.write(f"{title} 渲染錯誤: {e}")
    else:
        st.write(f"{title}: 暫無數據")

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    
    if not data:
        st.info("資料讀取中，請確認後台數據源。")
        return

    # 安全地取得股票列表
    tickers = [t for t in data.keys() if t not in ["last_updated"]]
    
    with st.sidebar:
        user_input = st.text_input("輸入股票代號", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = user_input
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    
    # 核心修正：強制確保 info 是一個字典，即使沒有資料也要回傳空字典
    info = data.get(target)
    if not isinstance(info, dict):
        info = {}

    st.header(f"股票: {target}")
    
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(float(price) - float(prev), 2)
    
    st.metric("即時股價", f"{price} 元", delta=f"{diff} 元")
    
    render_table(info, "institutional_daily", "5. 三大法人買賣超細項")
    render_table(info, "broker_daily", "6. 主力券商買賣超細項")

    st.subheader("7. AI 深度財報分析與新聞")
    st.info(f"📰 新聞解讀: {info.get('news_analysis', '暫無近期新聞')}")
    st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")
    st.error(f"⚠️ 黑天鵝警示: {info.get('black_swan_alert', '系統監控中：無異常')}")

if __name__ == "__main__":
    main()
