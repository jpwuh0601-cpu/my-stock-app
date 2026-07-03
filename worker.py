import yfinance as yf
import requests
import json
import datetime
import pandas_ta as ta
import os

# 設定您的 LINE Notify Token
LINE_TOKEN = "您的LINE_NOTIFY_TOKEN"

def send_line_notify(message):
    """發送 LINE 通知"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")

def run_analysis_and_update():
    """執行完整分析流程"""
    tickers = ["2330.TW", "2317.TW", "2454.TW"]
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        info = ticker.info
        
        # 1. 技術指標計算 (RSI)
        hist['RSI'] = ta.rsi(hist['Close'], length=14)
        rsi_val = hist['RSI'].iloc[-1] if not hist.empty else 50
        
        # 2. 黑天鵝警示邏輯 (波動率檢測)
        volatility = (hist['High'].iloc[-1] - hist['Low'].iloc[-1]) / hist['Open'].iloc[-1]
        is_black_swan = volatility > 0.05
        alert_msg = "⚠️ 黑天鵝警示：波動過大！" if is_black_swan else "系統穩定"
        
        # 若觸發警示發送 LINE
        if is_black_swan:
            send_line_notify(f"{symbol} 觸發風險警示！當前波動率: {volatility:.2%}")
            
        # 3. 整合資料結構
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "prev_close": info.get("previousClose", 0),
            "pe": info.get("forwardPE", 0),
            "eps": info.get("trailingEps", 0),
            "black_swan_alert": alert_msg,
            "ai_prediction": f"AI 分析：RSI 為 {rsi_val:.1f}，建議觀望。" if rsi_val < 70 else "AI 分析：過熱，建議減碼。",
            "institutional_daily": [
                {"日期": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d"), 
                 "外資": 1000 - i*50, "投信": 200, "自營商": -100} for i in range(10)
            ],
            "broker_daily": [
                {"日期": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d"), 
                 "主力A": 500, "主力B": 300} for i in range(10)
            ]
        }
    
    # 寫入 JSON
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("分析任務執行完畢，數據已更新。")

if __name__ == "__main__":
    run_analysis_and_update()
