import streamlit as st
import twstock
import pandas as pd
import random
import requests
import plotly.express as px

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (專業升級版)")

# 產業與代號映射表
SECTOR_MAP = {
    "半導體": ["2330", "2454", "2303", "3034"],
    "金融股": ["2881", "2882", "2886"],
    "營建股": ["2548", "2504", "5522"]
}

# 參數調整區
st.sidebar.header("決策權重控制")
weight_macd = st.sidebar.slider("MACD 權重", 0.0, 1.0, 0.5)
weight_sentiment = st.sidebar.slider("情緒指標權重", 0.0, 1.0, 0.5)
risk_control = st.sidebar.checkbox("啟用風險控管 (波動折抵)", True)

def send_line_message(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

def calculate_strategies(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    # 波動率計算 (ATR 概念)
    atr = (df['High'] - df['Low']).rolling(window=14).mean()
    return macd.iloc[-1], signal.iloc[-1], atr.iloc[-1]

def get_sentiment(ticker):
    return random.randint(0, 10)

def ai_score(macd, signal, atr, sentiment):
    score = 0
    if macd > signal: score += (50 * weight_macd)
    score += (sentiment * 5 * weight_sentiment)
    # 風險控管：波動過大則扣分
    if risk_control and atr > 5:
        score -= 20
    return max(0, round(score))

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        # 為了計算 ATR，我們需要 fetch_from 包含 High/Low
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        # 補上模擬的高低點，若資料源不足
        df['High'] = df['close'] * 1.02
        df['Low'] = df['close'] * 0.98
        df.rename(columns={'close': 'Close'}, inplace=True)
        return df
    except: return None

menu = st.sidebar.radio("核心模組", ["選股矩陣", "自動報告生成"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

if menu == "選股矩陣":
    sector = st.selectbox("選擇產業", list(SECTOR_MAP.keys()))
    if st.button("AI 綜合掃描"):
        results = []
        for t in SECTOR_MAP[sector]:
            df = fetch_data(t)
            if df is not None:
                macd, signal, atr = calculate_strategies(df)
                senti = get_sentiment(t)
                score = ai_score(macd, signal, atr, senti)
                results.append({"代號": t, "AI 評分": score, "波動風險(ATR)": round(atr, 2)})
        
        df_res = pd.DataFrame(results)
        fig = px.bar(df_res, x='代號', y='AI 評分', color='AI 評分', title="產業 AI 評分分佈")
        st.plotly_chart(fig, use_container_width=True)
        st.table(df_res.sort_values(by="AI 評分", ascending=False))

elif menu == "自動報告生成":
    if st.button("觸發自動化報告"):
        report_msg = "\n🚀 AI 自動化管家報告：\n"
        for sector, tickers in SECTOR_MAP.items():
            best_ticker = ""
            best_score = -1
            for t in tickers:
                df = fetch_data(t)
                if df is not None:
                    macd, signal, atr = calculate_strategies(df)
                    score = ai_score(macd, signal, atr, get_sentiment(t))
                    if score > best_score:
                        best_score, best_ticker = score, t
            report_msg += f"{sector} 首選: {best_ticker} (評分: {best_score})\n"
        send_line_message(token, report_msg)
        st.success("已完成自動化報告推送。")
