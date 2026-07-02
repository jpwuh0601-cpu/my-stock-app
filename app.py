```python
import streamlit as st
import pandas as pd
import json
import os

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="AI 智能金融監控終端",
    layout="wide"
)

# =========================
# 載入 JSON 數據
# =========================
def load_data():
    json_path = "market_data.json"

    if not os.path.exists(json_path):
        return {}

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        st.error("JSON 格式錯誤")
        return {}

    except Exception as e:
        st.error(f"讀取失敗：{e}")
        return {}

# =========================
# 主程式
# =========================
def main():

    data = load_data()

    if not data:
        st.warning("正在載入市場數據...")
        return

    # =========================
    # 標題
    # =========================
    st.title("📈 AI 智能金融監控終端")

    # =========================
    # 即時價格
    # =========================
    st.subheader("即時市場資訊")

    cols = st.columns(5)

    try:
        price = float(data.get("price", 0))
    except:
        price = 0

    cols[0].metric(
        label="即時股價",
        value=f"{price:,.2f}"
    )

    st.divider()

    # =========================
    # 三大法人 / 籌碼
    # =========================
    st.subheader("🏦 三大法人與籌碼數據")

    raw = data.get("institutional_investors", [])

    try:

        # -------------------------
        # 統一格式
        # -------------------------
        if isinstance(raw, dict):
            data_list = [raw]

        elif isinstance(raw, list):
            data_list = raw

        else:
            data_list = []

        # -------------------------
        # 過濾非法資料
        # -------------------------
        clean_list = []

        for item in data_list:
            if isinstance(item, dict):
                clean_list.append(item)

        # -------------------------
        # 建立 DataFrame
        # -------------------------
        if len(clean_list) > 0:

            df = pd.DataFrame(clean_list)

            # 修正 index
            df.reset_index(drop=True, inplace=True)

            # 顯示表格
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("目前無籌碼數據。")

    except Exception as e:
        st.error(f"表格解析失敗：{e}")

    st.divider()

    # =========================
    # AI 分析
    # =========================
    st.subheader("🤖 AI 智能分析")

    ai_text = data.get("ai_prediction", "暫無 AI 分析資料")

    st.write(ai_text)

    # =========================
    # 原始 JSON（除錯模式）
    # =========================
    with st.expander("查看原始 JSON 資料"):

        st.json(data)

# =========================
# 執行
# =========================
if __name__ == "__main__":
    main()
```
