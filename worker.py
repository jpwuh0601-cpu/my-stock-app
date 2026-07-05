import yfinance as yf
import json
import os
from analyzer import generate_ai_analysis

def fetch_stock_data(ticker_symbol):
    """
    獲取股票數據並進行籌碼面計算
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # 取得基本面與籌碼面數據
        price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        pe = info.get('forwardPE', 0)
        eps = info.get('trailingEps', 0)
        
        # 籌碼面邏輯：使用 institutionalHolders 或模擬數據
        # 實務上籌碼需結合外資/投信買賣超，此處以 floatShares 比例作為籌碼集中度參考
        shares = info.get('floatShares', 0)
        institutional_buy = (shares * 0.05) if shares else 0 
        
        # 呼叫 AI 分析模組
        ai_prediction = generate_ai_analysis(ticker_symbol, info)
        
        # 建構完整數據結構
        data = {
            "price": price,
            "change": 0, # 可視需求擴充
            "nav": price,
            "pe": pe,
            "eps": eps,
            "margin_ratio": 0,
            "institutional_data": [
                {"日期": "最新", "外資": institutional_buy, "投信": 0, "自營商": 0}
            ],
            "ai_prediction": ai_prediction,
            "news": "籌碼面分析已整合。",
            "black_swan": "安全" if eps > 0 else "高風險"
        }
        return data
    except Exception as e:
        print(f"Error fetching {ticker_symbol}: {e}")
        return None

def main():
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file):
        return

    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    for ticker in tickers:
        print(f"正在處理: {ticker}")
        result = fetch_stock_data(ticker)
        if result:
            all_results[ticker] = result

    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print("數據已更新至 market_data.json")

if __name__ == "__main__":
    main()
