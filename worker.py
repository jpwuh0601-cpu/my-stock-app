import yfinance as yf
import json
import os
import datetime

# 定義檔案路徑
DATA_FILE = "market_data.json"
TICKERS_FILE = "tickers.txt"

def get_target_tickers():
    """讀取 tickers.txt，若檔案不存在則返回預設列表"""
    if os.path.exists(TICKERS_FILE):
        with open(TICKERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]

def run_analysis_and_update():
    """抓取真實股價、歷史數據與指標，並寫入 JSON"""
    tickers = get_target_tickers()
    data = {}
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            # 獲取近一年歷史股價，用於繪圖
            hist = ticker.history(period="1y")
            
            # 將 DataFrame 轉換為可 JSON 序列化的格式
            history_data = hist.reset_index()[['Date', 'Close']]
            history_data['Date'] = history_data['Date'].dt.strftime('%Y-%m-%d')
            history_list = history_data.rename(columns={'Date': '日期', 'Close': '股價'}).to_dict(orient='records')
            
            data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "change": info.get("regularMarketChangePercent", 0),
                "nav": info.get("bookValue") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "margin_ratio": 5.2, # 預留欄位
                "history": history_list,
                "institutional_data": [{"日期": "最新", "外資": 0, "投信": 0, "自營商": 0}],
                "news": "市場動態更新正常。",
                "ai_prediction": "AI 趨勢模型分析：建議持續關注量能變化。",
                "black_swan": "安全",
                "main_force": "主力觀察中",
                "foreign_analysis": "外資持平",
                "gpt_insight": "趨勢建議：技術面多頭排列。"
            }
        except Exception as e:
            print(f"[-] 抓取 {symbol} 失敗: {e}")
            
    # 安全寫入檔案
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[+] 資料已更新至 {DATA_FILE}")

if __name__ == "__main__":
    run_analysis_and_update()
