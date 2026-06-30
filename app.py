import streamlit as st
import pandas as pd
import json
import os
import math

st.set_page_config(page_title="專業投資決策儀表板", layout="wide")

st.title("📈 專業投資決策儀表板")

def load_and_validate_data():
    """載入並檢核資料來源，若檔案不存在或為空則回傳預設結構"""
    file_path = "market_data.json"
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 確保 data 為字典結構
            if not isinstance(data, dict):
                return None
            
            # 檢查基礎必要欄位
            required_keys = ['price', 'bvps', 'financials', 'institutional_investors', 'news', 'technical_indicators']
            
            for key in required_keys:
                if key not in data:
                    return None
            return data
    except Exception as e:
        return None

def get_scalar(val):
    """確保數值為有限標量，並強制轉換為 float，過濾非有限值，並支援 pandas Series"""
    try:
        if val is None:
            return 0.0
        # 如果是 pandas Series，取最後一個值
        if isinstance(val, pd.Series):
            val = val.iloc[-1]
        # 如果是列表，取最後一個值
        if isinstance(val, list):
            val = val[-1] if val else 0
        
        f = float(val)
        if math.isfinite(f):
            return f
        return 0.0
    except (ValueError, TypeError, AttributeError):
        return 0.0

data = load_and_validate_data()

if data:
    update_date = data.get('update_date', '未知日期')
    st.caption(f"最後更新時間: {update_date}")

    # 使用優化後的數值獲取函數
    price = get_scalar(data.get('price', 0))
    bvps = get_scalar(data.get('bvps', 0))
    est_revenue = get_scalar(data.get('est_revenue', 0))
    est_eps = get_scalar(data.get('est_eps', 0))
    est_dividend = get_scalar(data.get('est_dividend', 0))
    margin_ratio = get_scalar(data.get('margin_ratio', 0))

    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", value=f"${price:,.2f}")
    col2.metric("每股淨值 (BVPS)", value=f"${bvps:,.2f}")
    col3.metric("LINE 通知狀態", value="已連線" if data.get('line_status') else "未連線")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["財務績效與預測", "籌碼與主力分析", "市場動態與AI監控", "技術與策略指標"])

    with tab1:
        st.subheader("每季財務報表")
        # 確保 financials 存在且為字典或數據框格式，否則顯示空表格
        financials = data.get('financials')
        if isinstance(financials, dict):
            st.table(pd.DataFrame(financials))
        else:
            st.write("目前無財務報表數據。")
        
        st.subheader("年度財務預估")
        f_col1, f_col2, f_col3 = st.columns(3)
        f_col1.metric("預估今年營收", value=f"{est_revenue:,.0f}")
        f_col2.metric("預估 EPS", value=f"{est_eps:,.2f}")
        f_col3.metric("預估股利", value=f"{est_dividend:,.2f}")
            
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction', '系統分析中...'))

    with tab2:
        st.subheader("三大法人買賣超")
        inst_data = data.get('institutional_investors', [])
        if isinstance(inst_data, list) and len(inst_data) > 0:
            df_inst = pd.DataFrame(inst_data)
            st.dataframe(df_inst, use_container_width=True)
        else:
            st.write("目前無籌碼分析數據。")
        
        st.subheader("籌碼面統計")
        col_a, col_b = st.columns(2)
        col_a.metric("資券比", value=f"{margin_ratio:.2f}%")

    with tab3:
        st.subheader("最新市場新聞與分析")
        news_list = data.get('news', [])
        if isinstance(news_list, list):
            for news in news_list:
                st.write(f"• {news}")
        else:
            st.write("目前無新聞資訊。")
            
        st.subheader("黑天鵝警示系統")
        swan_data = data.get('black_swan_alert', {})
        if isinstance(swan_data, dict) and swan_data.get('is_triggered'):
            st.error(f"⚠️ 偵測到警示")
        else:
            st.success("目前無異常市場風險。")

    with tab4:
        st.subheader("技術分析指標 (GPT AI 判讀)")
        st.write(data.get('technical_indicators', '目前無分析數據'))
        
        st.subheader("AI 選股邏輯建議")
        st.markdown(data.get('ai_stock_selection', '系統分析中...'))

else:
    st.warning("數據源尚未更新，請確保 GitHub Actions 已成功執行並產生 market_data.json。")
    st.info("系統正處於初始化階段，請稍候排程任務完成。")
