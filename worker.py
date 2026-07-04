import yfinance as yf
import requests
import json
import os
import datetime

# 從環境變數讀取 API 金鑰
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_sentiment(news_title):
    """呼叫 OpenRouter AI 進行新聞情緒分析"""
    if not OPENROUTER_API_KEY:
        return "AI 分析功能未啟用 (請檢查 API Key)"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{news_title}。請用一句話簡短總結市場觀點。"}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception:
        return "分析暫時中斷"

def run_analysis_and_update():
    # 1. 讀取 tickers.txt 並合併預設清單，去重處理
    default_tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r") as f:
            file_tickers = [line.strip() for line in f if line.strip()]
            tickers = list(set(default_tickers + file_tickers))
    else:
        tickers = default_tickers

    data = {}
    today = datetime.date.today()
    
    # 2. 迴圈處理每一支股票
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            news = ticker.news
            
            # 獲取基礎數據
            price = info.get("currentPrice") or 0
            change = round(info.get("regularMarketChangePercent", 0), 2)
            latest_news = news[0]['title'] if news else "目前無最新新聞"
            
            # 獲取 AI 情緒分析
            ai_prediction = get_ai_sentiment(latest_news)
            
            # 籌碼模擬數據 (未來可擴充為從 API 抓取真實法人數據)
            institutional_data = [
                {"日期": (today - datetime.timedelta(days=2)).strftime("%m-%d"), "外資": 100, "投信": 50, "自營商": -20},
                {"日期": (today - datetime.timedelta(days=1)).strftime("%m-%d"), "外資": -200, "投信": 10, "自營商": -30},
                {"日期": today.strftime("%m-%d"), "外資": -150, "投信": -40, "自營商": -50}
            ]
            
            # 存入資料字典
            data[symbol] = {
                "price": price,
                "change": change,
                "eps": info.get("trailingEps") or 0,
                "pe": info.get("forwardPE") or 0,
                "nav": info.get("bookValue") or 0,
                "news": latest_news,
                "ai_prediction": ai_prediction,
                "institutional_data": institutional_data,
                "black_swan": "⚠️ 高風險警示" if change <= -3 else "安全"
            }
        except Exception as e:
            print(f"[-] 無法抓取 {symbol}: {e}")
            
    # 3. 寫入 JSON 檔案供前端讀取
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[+] 資料分析完成，共處理 {len(data)} 支標的")

if __name__ == "__main__":
    run_analysis_and_update()
