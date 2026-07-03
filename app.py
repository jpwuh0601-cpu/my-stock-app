import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def render_table(info, key, title):
    """加入 NoneType 檢查，確保資料即使為空也不會崩潰"""
    data = info.get(key)
    
    # 強制檢查 data 是否為 None 或空的物件
    if data is None or data == []:
        st.write(f"{title}: 暫無籌碼細項資料")
        return

    # 若 data 是字串 (JSON 格式)，嘗試解析
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            st.write(f"{title}: 資料格式錯誤")
            return

    try:
        # 強制轉換為 DataFrame 並應用顏色樣式
        df = pd.DataFrame(data)
        st.subheader(title)
        
        # 簡單的紅綠色樣式 (判斷是否有數字欄位)
        def color_style(val):
            try:
                # 若是數字則判斷正負
                num = float(str(val).replace(',', ''))
                color = 'red' if num > 0 else ('green' if num < 0 else 'black')
                return f'color: {color}'
            except:
                return ''
                
        styled_df = df.style.applymap(color_style)
        st.dataframe(styled_df, use_container_width=True)
    except Exception as e:
        st.write(f"{title}: 表格繪製錯誤 ({e})")

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    
    if not data:
        st.info("資料載入中，請確認後台數據源。")
        return

    # 取得股票清單
    tickers = [t for t in data.keys() if t not in ["last_updated"]]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        
    info = data.get(target, {})
    
    st.header(f"股票: {target}")
    
    # 顯示漲跌 (確保不崩潰)
    price = info.get("price", 0)
    prev = info.get("prev_close", 0)
    diff = round(price - prev, 2)
    
    st.metric("即時股價", f"{price} 元", delta=f"{diff} 元")
    
    # 顯示法人與券商表
    render_table(info, "institutional_daily", "5. 三大法人 10 日買賣超細項")
    render_table(info, "broker_daily", "6. 主力券商 10 日買賣超細項")

    st.subheader("7. AI 深度財報分析")
    st.success(info.get("ai_prediction", "AI 分析中..."))

if __name__ == "__main__":
    main()
