import json
import logging
import yfinance as yf
import os
import requests

def send_line_notify(message, force=False):
    """加入強制發送參數 (force=True 代表賣出警告)"""
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        return
        
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token.strip()}"}
    try:
        requests.post(url, headers=headers, data={"message": message})
    except Exception as e:
        logging.error(f"LINE 發送失敗: {e}")

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="2d")
        
        # 計算前一日收盤價與今日股價的變動率
        prev_close = hist['Close'].iloc[-2]
        current_price = hist['Close'].iloc[-1]
        change_rate = (current_price - prev_close) / prev_close
        
        # 準備資料
        raw_data = {"price": current_price, "change": change_rate}
        
        # 執行 AI 分析 (省略呼叫細節)
        analysis = "系統運行正常。" 
        raw_data["ai_prediction"] = analysis
        
        # 儲存
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
        # 條件式告警：如果變動 > 3% 或 AI 建議賣出
        if abs(change_rate) >= 0.03 or "賣出" in analysis:
            msg = f"\n⚠️ 市場異常波動提醒\n股價變動: {change_rate:.2%}\n當前股價: {current_price:.2f}"
            send_line_notify(msg, force=True)
            
    except Exception as e:
        logging.error(f"執行錯誤: {e}")
