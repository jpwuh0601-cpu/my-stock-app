import yfinance as yf
import json
import os
import pandas as pd
from analyzer import generate_ai_analysis

def fetch_real_institutional_data(ticker_symbol):
    """取得三大法人模擬數據 (未來可替換為真實爬蟲)"""
    # 此處保留為 API 結構，方便未來替換為 twstock 或證交所爬蟲
    return [{"日期": "最新", "外資": 1500, "投信": 200, "自營商": -50}]

def fetch_real_broker_data(ticker_symbol):
    """
    獲取券商分點明細
    此為爬蟲邏輯架構，未來可擴充至玩股網等來源
    """
    try:
        # 預留位置：此處可使用 requests + BeautifulSoup 進行解析
        return [{"日期": "最新", "券商": "元大-台北", "買賣張數": 120},
                {"日期": "最新", "券商": "凱基-台北", "買賣張數": -50}]
    except Exception as e:
        print(f"券商資料抓取失敗: {e}")
        return []

def fetch_stock_data(ticker_symbol):
    """
    獲取股票數據並進行深度分析
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # 取得股價與基本面數據
        price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        # 取得籌碼與券商數據
        inst_data = fetch_real_institutional_data(ticker_symbol)
        broker_data = fetch_real_broker_data(ticker_symbol)
        
        # 呼叫 AI 分析模組進行深度運算
        ai_prediction = generate_ai_analysis(ticker_symbol, info, institutional_data=inst_data, broker_data=broker_data)
        
        return {
            "price": price,
            "institutional_data": inst_data,
            "broker_data": broker_data,
            "ai_prediction": ai_prediction
        }
    except Exception as e:
        print(f"處理 {ticker_symbol} 失敗: {e}")
        return None

def main():
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file): 
        print("未找到 tickers.txt")
        return
        
    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    for ticker in tickers:
        print(f"正在處理: {ticker}")
        result = fetch_stock_data(ticker)
        if result: 
            all_results[ticker] = result

    # 寫入 market_data.json 供看板顯示
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print("數據已更新至 market_data.json")

if __name__ == "__main__":
    main()
