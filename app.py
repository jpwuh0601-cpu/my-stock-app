import streamlit as st
import random
from worker import fetch_stock_data

# 智慧型參考價格表 (當網路抓取失敗時使用)
REALISTIC_BASE_PRICES = {
    "2330.TW": 750, "2317.TW": 200, "2454.TW": 950,
    "1301.TW": 60,  "6770.TW": 150, "1504.TW": 40
}

def get_fallback_data(ticker):
    price = REALISTIC_BASE_PRICES.get(ticker, 100) # 預設給 100 元
    return {
        "price": price, 
        "change": round(random.uniform(-1, 1), 2),
        "nav": round(price * 0.8), 
        "pe": round(random.uniform(10, 25), 1), 
        "eps": round(price * 0.05, 1),
        "status": "simulated"
    }

st.title("📈 專業股市決策儀表板")

# 選擇器
ticker_input = st.text_input("輸入股票代號 (例: 1301):", "1301")
if st.button("查詢"):
    ticker = f"{ticker_input}.TW" if "." not in ticker_input else ticker_input
    
    with st.spinner("載入中..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.warning(f"目前無法即時連線 (使用模擬數據模式): {data['error']}")
            s = get_fallback_data(ticker)
        else:
            s = data
            st.success("✅ 已載入即時市場行情")

    # 顯示數據
    st.metric("即時股價", f"{s['price']} 元")
    st.write(f"數據來源: {'即時行情' if s.get('status') == 'live' else '行情參考值'}")
    
    # ... 其餘顯示代碼保持原樣 ...
