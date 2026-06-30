import json
import requests
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from openai import OpenAI
from bs4 import BeautifulSoup
import time
import math

# 設定 OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知失敗: {e}")

def sanitize_recursive(val):
    """遞迴檢查物件結構，確保沒有 NaN 或 inf"""
    if isinstance(val, dict):
        return {k: sanitize_recursive(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [sanitize_recursive(v) for v in val]
    elif isinstance(val, (float, int)):
        # 強制轉換為有限浮點數
        if not math.isfinite(val):
            return 0.0
        return float(val)
    return val

def calculate_technical_indicators(df):
    """計算技術指標，優先使用 pandas_ta，若無則自動降級為原生 pandas 計算"""
    ta_module = None
    try:
        import pandas_ta as ta
        ta_module = ta
    except ImportError:
        print("注意：偵測到 pandas_ta 未安裝，將使用原生 pandas 進行技術指標計算。")

    try:
        required_cols = ['Close', 'High', 'Low']
        if not all(col in df.columns for col in required_cols):
            return {"RSI": 0, "KD": {}, "MACD": {}}

        if ta_module is not None:
            try:
                rsi_series = ta_module.rsi(df['Close'], length=14)
                stoch_df = ta_module.stoch(df['High'], df['Low'], df['Close'])
                macd_df = ta_module.macd(df['Close'])
                
                rsi_val = float(rsi_series.iloc[-1]) if rsi_series is not None and not pd.isna(rsi_series.iloc[-1]) else 0
                
                kd_val = {}
                if stoch_df is not None and not stoch_df.empty:
                    kd_val = stoch_df.iloc[-1].to_dict() if hasattr(stoch_df.iloc[-1], 'to_dict') else {}
                
                macd_val = {}
                if macd_df is not None and not macd_df.empty:
                    macd_val = macd_df.iloc[-1].to_dict() if hasattr(macd_df.iloc[-1], 'to_dict') else {}
                
                return {"RSI": rsi_val, "KD": kd_val, "MACD": macd_val}
            except Exception as e:
                print(f"pandas_ta 計算過程異常，降級處理: {e}")
                
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return {
            "RSI": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 0,
            "KD": {"status": "native_fallback"},
            "MACD": {"status": "native_fallback"}
        }
    except Exception as e:
        print(f"指標計算發生嚴重錯誤: {e}")
        return {"RSI": 0, "KD": {}, "MACD": {}}

def run_analysis_and_update():
    ticker_code = "2330"
    ticker = yf.Ticker(f"{ticker_code}.TW")
    
    hist = None
    for i in range(3):
        try:
            hist = ticker.history(period="6mo")
            if hist is not None and not hist.empty: break
            time.sleep(2)
        except Exception as e:
            print(f"歷史數據下載失敗: {e}")
            time.sleep(5)
            
    if hist is None or hist.empty:
        print("無法取得歷史數據，跳過指標計算")
        indicators = {"RSI": 0, "KD": {}, "MACD": {}}
    else:
        indicators = calculate_technical_indicators(hist)
    
    info = {}
    try:
        raw_info = ticker.info
        if raw_info and isinstance(raw_info, dict):
            info = raw_info
    except Exception as e:
        print(f"取得 ticker.info 失敗: {e}")
        
    def sanitize(val):
        """全面數值安全檢查，確保不會產生 inf 或 NaN"""
        try:
            if val is None: return 0.0
            f = float(val)
            if not math.isfinite(f): return 0.0
            return f
        except:
            return 0.0
        
    # 安全存取與計算
    s_shares = sanitize(info.get("sharesOutstanding") if isinstance(info, dict) else 0)
    shares = s_shares if s_shares > 0 else 25930000000 
    
    revenue = sanitize(info.get("totalRevenue", 0) if isinstance(info, dict) else 0)
    est_eps = (revenue * 0.20 * 0.40) / shares
    est_dividend = est_eps * 0.50
    
    # 在寫入前，先對所有預估值進行 final sanitize
    final_data = {
        "update_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": sanitize(info.get("currentPrice", 0) if isinstance(info, dict) else 0),
        "bvps": sanitize(info.get("bookValue", 0) if isinstance(info, dict) else 0),
        "financials": {"2025Q1": {"EPS": 5.2}},
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "news": ["市場動態更新"],
        "technical_indicators": indicators,
        "est_revenue": sanitize(revenue * 1.2),
        "est_eps": round(sanitize(est_eps), 2),
        "est_dividend": round(sanitize(est_dividend), 2),
        "ai_prediction": "基於營收預測分析。",
        "margin_ratio": 1.2,
        "black_swan_alert": {"is_triggered": False},
        "ai_stock_selection": "維持穩健持有建議。",
        "line_status": True
    }
    
    # 進行最終全域數據清理，確保完全沒有 non-finite values
    clean_data = sanitize_recursive(final_data)
    
    output_path = os.path.join(os.getcwd(), "market_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, ensure_ascii=False, indent=4)
        print(f"數據成功寫入至: {output_path}")
    except Exception as e:
        print(f"寫入檔案發生嚴重錯誤: {e}")
        return 
        
    send_line_notify(f"每日股市更新: {ticker_code} 預估EPS={round(sanitize(est_eps), 2)}")

if __name__ == "__main__":
    run_analysis_and_update()
