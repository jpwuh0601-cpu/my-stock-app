import json
import logging
import yfinance as yf
import os
import requests

# 設定基礎日誌
logging.basicConfig(level=logging.INFO)

def send_line_notify(message):
    """發送 LINE Notify 通知"""
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        logging.warning("未偵測到 LINE_NOTIFY_TOKEN，跳過通知")
        return
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    try:
        requests.post(url, headers=headers, data=payload)
        logging.info("LINE 通知已發送")
    except Exception as e:
        logging.error(f"LINE 通知發送失敗: {e}")

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        # 抓取資料
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        
        # 準備資料結構
        raw_data = {
            "price": price,
            "bvps": info.get("bookValue", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "margin_ratio": 1.25,
            "eps_forecast": info.get("trailingEps", 0),
            "institutional_investors": [{"機構": "外資", "買賣超": 500}, {"機構": "投信", "買賣超": 200}],
            "ai_prediction": "AI 分析：台積電市場表現穩健，建議持續關注。",
            "news": "最新半導體市場分析報告。"
        }
        
        # 儲存到 JSON
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
        # 發送 LINE 通知
        msg = f"\n📈 台積電即時監控\n目前股價: {price:.2f}\n本益比: {info.get('trailingPE', 0):.2f}\n分析: {raw_data['ai_prediction']}"
        send_line_notify(msg)
        
        logging.info("數據抓取並更新完成")
            
    except Exception as e:
        logging.error(f"執行錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
