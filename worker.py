import json
import time
import os
import yfinance as yf
import requests

def get_ai_analysis(ticker_symbol):
    """直接在 Worker 內部執行 AI 分析，不再依賴外部檔案"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "未偵測到 OPENROUTER_API_KEY，請檢查 Secrets 設定。"

    ticker = yf.Ticker(ticker_symbol)
    try:
        # 抓取財報數據
        info = ticker.info
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        prompt = f"""
        請針對股票 {ticker_symbol} 進行財報分析。
        EPS: {info.get('trailingEps', 'N/A')}
        本益比 (PE): {info.get('forwardPE', 'N/A')}
        最新新聞: {latest_news}
        
        請依照以下格式輸出：
        【投資觀點】：(買入/觀望/賣出)
        【核心理由】：(簡短說明)
        【風險點】：(列出1-2個關鍵風險)
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response_data = response.json()
        
        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content']
        else:
            return "AI 分析服務回傳格式異常。"
            
    except Exception as e:
        return f"AI 分析發生錯誤: {str(e)}"

def run_analysis_and_update():
    # 確保路徑指向當前腳本所在的目錄
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tickers_path = os.path.join(base_dir, "tickers.txt")
    output_path = os.path.join(base_dir, "market_data.json")
    
    if not os.path.exists(tickers_path):
        print(f"致命錯誤：找不到 {tickers_path}")
        return

    with open(tickers_path, "r", encoding="utf-8") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    market_data = {}
    print(f"開始分析 {len(tickers)} 檔股票...")
    
    for symbol in tickers:
        try:
            print(f"正在分析: {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            market_data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "ai_prediction": get_ai_analysis(symbol),
                "black_swan": "安全",
                "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            # 延遲以避免 Yahoo API 限制
            time.sleep(3)
        except Exception as e:
            print(f"處理 {symbol} 時發生錯誤: {e}")
            
    # 寫入 JSON 檔案
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)
    print("數據已更新至 market_data.json")

if __name__ == "__main__":
    run_analysis_and_update()
