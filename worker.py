import json
import yfinance as yf
import logging

def run_analysis_and_update():
    ticker_symbol = "2330.TW"
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 抓取近 30 天歷史數據
        hist = ticker.history(period="1mo")
        
        # 轉為 Plotly 可用的格式
        history_data = {
            "dates": hist.index.strftime('%Y-%m-%d').tolist(),
            "closes": hist['Close'].tolist()
        }
        
        # 讀取現有資料並更新
        data = {"price": ticker.fast_info.last_price, "history": history_data}
        
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
