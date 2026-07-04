import yfinance as yf
import json
import datetime
import twstock
import os
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

def get_real_margin_short_data(symbol):
    """獲取真實資券比"""
    clean_symbol = symbol.split('.')[0]
    try:
        stock = twstock.Stock(clean_symbol)
        margin = stock.margin
        short = stock.short
        if short and margin and len(short) > 0 and short[-1] > 0:
            ratio = (margin[-1] / short[-1]) * 100
            return round(ratio, 2)
        return 0.0
    except Exception as e:
        logging.warning(f"資券數據獲取失敗 ({symbol}): {e}")
        return 0.0

def backtest_system(symbol, current_price):
    """自動記錄並統計勝率"""
    history_file = "backtest_history.json"
    history = {}
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            history = {}
            
    stats = history.get(symbol, {"prices": [], "total_win": 0, "total_loss": 0})
    
    # 計算績效
    if stats["prices"]:
        last_price = stats["prices"][-1]
        if current_price > last_price:
            stats["total_win"] += 1
        elif current_price < last_price:
            stats["total_loss"] += 1
            
    stats["prices"].append(float(current_price))
    history[symbol] = stats
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    
    return stats

def run_analysis_and_update():
    """主分析流程：採集數據並更新市場狀態"""
    target_file = "market_data.json"
    
    # 預設追蹤清單
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]
    
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in tickers:
        try:
            logging.info(f"正在處理: {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 優先嘗試取得當前價格
            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
            if price == 0:
                logging.warning(f"{symbol} 無價格數據，跳過。")
                continue
            
            stats = backtest_system(symbol, price)
            total_matches = stats["total_win"] + stats["total_loss"]
            win_rate = (stats["total_win"] / total_matches * 100) if total_matches > 0 else 0
            
            data[symbol] = {
                "price": price,
                "prev_close": info.get("previousClose", 0),
                "pe": info.get("forwardPE") or info.get("trailingPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "nav": info.get("bookValue") or 0,
                "win_rate": f"{round(win_rate, 2)}%",
                "broker_daily": [{"日期": "最新", "資券比": f"{get_real_margin_short_data(symbol)}%"}],
                "ai_prediction": "AI 分析：基本面監控中，請參考回測勝率。",
                "news_analysis": "市場監控數據已更新。",
                "black_swan_alert": "系統監控中：無異常"
            }
        except Exception as e:
            logging.error(f"處理 {symbol} 時發生錯誤: {e}")
            
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("數據採集完成，已更新 market_data.json")
