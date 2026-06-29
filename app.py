import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="專業投資決策儀表板", layout="wide")

st.title("📈 專業投資決策儀表板")

def load_and_validate_data():
    """載入並回測資料來源是否正確"""
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 簡單回測：檢查必要的關鍵欄位是否存在
            required_keys = ['price', 'bvps', 'financials', 'institutional_investors', 'news', 'technical_indicators']
            for key in required_keys:
                if key not in data:
                    st.error(f"資料檢核異常：缺少關鍵欄位 '{key}'，請檢查 worker.py 數據產出")
                    return None
            return data
    except Exception as e:
        st.error(f"無法讀取數據：{e}")
        return None

data = load_and_validate_data()

if data:
    update_date = data.get('update_date', '未知日期')
    st.caption(f"最後更新時間: {update_date}")

    # 1 & 2. 即時股價與每股淨值
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"${data.get('price', 0)}")
    col2.metric("每股淨值 (BVPS)", f"${data.get('bvps', 0)}")
    
    # 新增：AI 選股狀態與通知監控
    col3.metric("LINE 通知狀態", "已連線" if data.get('line_status') else "未連線")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["財務績效與預測", "籌碼與主力分析", "市場動態與AI監控", "技術與策略指標"])

    with tab1:
        st.subheader("每季財務報表 (去年至今年)")
        st.table(pd.DataFrame(data.get('financials', {})))
        
        st.subheader("年度財務預估")
        f_col1, f_col2, f_col3 = st.columns(3)
        f_col1.metric("預估今年營收", f"{data.get('est_revenue', 'N/A')}")
        f_col2.metric("預估 EPS", f"{data.get('est_eps', 'N/A')}")
        f_col3.metric("預估股利", f"{data.get('est_dividend', 'N/A')}")
            
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction', '無預測數據'))

    with tab2:
        st.subheader("三大法人買賣超 (近10日)")
        df_inst = pd.DataFrame(data.get('institutional_investors', []))
        def color_map(val):
            return f'color: {"red" if val > 0 else "green"}'
        if not df_inst.empty:
            st.dataframe(df_inst.style.applymap(color_map, subset=['買賣超']), use_container_width=True)
        
        st.subheader("籌碼面統計")
        col_a, col_b = st.columns(2)
        col_a.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")
        
        st.subheader("主力券商與自營商買賣統計")
        st.json(data.get('top_brokers', {}))

    with tab3:
        st.subheader("最新市場新聞與分析")
        for news in data.get('news', []):
            st.write(f"• {news}")
            
        st.subheader("黑天鵝警示系統")
        swan_data = data.get('black_swan_alert', {})
        if swan_data.get('is_triggered'):
            st.error(f"⚠️ 偵測到警示: {swan_data.get('reason')}")
        else:
            st.success("目前無異常市場風險。")

    with tab4:
        st.subheader("技術分析指標 (GPT AI 判讀)")
        st.write(data.get('technical_indicators', '目前無分析數據'))
        
        st.subheader("AI 選股邏輯建議")
        st.markdown(data.get('ai_stock_selection', '系統分析中...'))

else:
    st.warning("數據源尚未準備就緒，請等待自動化排程更新...")
