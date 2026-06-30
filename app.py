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
            # 檢查基礎必要欄位
            required_keys = ['price', 'bvps', 'financials', 'institutional_investors', 'news', 'technical_indicators']
            
            for key in required_keys:
                if key not in data:
                    return None
            return data
    except Exception as e:
        return None

def get_scalar(val):
    """確保數值為有限標量，若為列表則取最後一項或轉換，過濾非有限值"""
    try:
        if isinstance(val, list):
            val = val[-1] if val else 0
        f = float(val)
        if math.isfinite(f):
            return f
        return 0.0
    except:
        return 0.0

data = load_and_validate_data()

if data:
    update_date = data.get('update_date', '未知日期')
    st.caption(f"最後更新時間: {update_date}")

    # 使用優化後的數值獲取函數，強制轉為 float 並檢查有限性
    price = get_scalar(data.get('price', 0))
    bvps = get_scalar(data.get('bvps', 0))

    col1, col2, col3 = st.columns(3)
    # 將 metric 改為數值顯示，以符合 Streamlit API 規範
    col1.metric("即時股價", value=f"${price:,.2f}")
    col2.metric("每股淨值 (BVPS)", value=f"${bvps:,.2f}")
    col3.metric("LINE 通知狀態", value="已連線" if data.get('line_status') else "未連線")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["財務績效與預測", "籌碼與主力分析", "市場動態與AI監控", "技術與策略指標"])

    with tab1:
        st.subheader("每季財務報表")
        st.table(pd.DataFrame(data.get('financials', {})))
        
        st.subheader("年度財務預估")
        f_col1, f_col2, f_col3 = st.columns(3)
        f_col1.metric("預估今年營收", value=f"{data.get('est_revenue', 0)}")
        f_col2.metric("預估 EPS", value=f"{data.get('est_eps', 0)}")
        f_col3.metric("預估股利", value=f"{data.get('est_dividend', 0)}")
            
        st.subheader("AI 財報預測")
        st.info(data.get('ai_prediction', '系統分析中...'))

    with tab2:
        st.subheader("三大法人買賣超")
        inst_data = data.get('institutional_investors', [])
        df_inst = pd.DataFrame(inst_data)
        if not df_inst.empty:
            st.dataframe(df_inst, use_container_width=True)
        
        st.subheader("籌碼面統計")
        col_a, col_b = st.columns(2)
        col_a.metric("資券比", value=f"{data.get('margin_ratio', 0)}%")

    with tab3:
        st.subheader("最新市場新聞與分析")
        for news in data.get('news', []):
            st.write(f"• {news}")
            
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
