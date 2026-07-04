import yfinance as yf
import requests
import json
import os
import datetime

# 從環境變數讀取 LINE Token，若讀不到則使用預設值（需在 Secrets 設定）
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def send_line_notify(message):
    """發送訊息至 LINE Notify"""
    if not LINE_TOKEN:
        print("[-] 未設定 LINE_TOKEN，無法發送通知")
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    requests.post(url, headers=headers, data={"message": message})

def run_analysis_and_update():
    # 讀取股票清單
    try:
        with open("tickers.txt", "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    except:
        tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

    data = {}
    today = datetime.date.today()
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price_change = info.get("regularMarketChangePercent", 0)
            
            # 1. 基礎數據
            current_data = {
                "price": info.get("currentPrice") or 0,
                "change": round(price_change, 2),
                "eps": info.get("trailingEps") or 0,
                "pe": info.get("forwardPE") or 0,
                "nav": info.get("bookValue") or 0,
                "black_swan": "安全"
            }
            
            # 2. 模擬法人數據 (實際應用可對接 twstock)
            # 這裡建立 3 日籌碼數據供邏輯判斷使用
            institutional_data = [
                {"日期": (today - datetime.timedelta(days=2)).strftime("%m-%d"), "外資": -100, "投信": 50, "自營商": -20},
                {"日期": (today - datetime.timedelta(days=1)).strftime("%m-%d"), "外資": -200, "投信": -10, "自營商": -30},
                {"日期": today.strftime("%m-%d"), "外資": -500, "投信": -80, "自營商": -10}
            ]
            current_data["institutional_data"] = institutional_data
            
            # 3. 邏輯判斷：連續 3 日外資賣超則觸發告警
            is_selling_streak = all(day['外資'] < 0 for day in institutional_data)
            if is_selling_streak or price_change <= -3.0:
                current_data["black_swan"] = "⚠️ 高風險警示"
                send_line_notify(f"【⚠️ 警報】{symbol} 出現風險訊號！跌幅: {round(price_change, 2)}%，外資連續賣超。")
            
            data[symbol] = current_data
            
        except Exception as e:
            print(f"[-] 處理 {symbol} 失敗: {e}")
            
    # 寫入結果
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("[+] 資料已更新並寫入 market_data.json")

if __name__ == "__main__":
    run_analysis_and_update()
