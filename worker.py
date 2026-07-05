import yfinance as yf
import json
# 導入您新建的 analyzer 模組，確保該檔案位於同一目錄下
from analyzer import generate_ai_analysis 

def get_ai_analysis_data(ticker_symbol):
    """
    獲取完整數據、計算指標並呼叫 analyzer 模組進行 AI 分析
    確保回傳的欄位結構完美對接前端 app.py 的需求
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # 1. 取得 AI 分析觀點 (呼叫 analyzer.py 中的函式)
        # 傳入 info 字典，analyzer 將根據其中的基本面數據與指標進行分析
        analysis_prompt = generate_ai_analysis(ticker_symbol, info)
        
        # 2. 彙整數據，確保欄位對齊 app.py 的 metric 與 info 讀取邏輯
        # 確保即使獲取失敗也有預設值，避免 app.py 報錯
        data = {
            "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
            "eps": info.get('trailingEps', 0),
            "pe": info.get('forwardPE', 0),
            # 簡單的財務安全判斷邏輯，作為安全等級參考
            "black_swan": "安全" if info.get('trailingEps', 0) > 0 else "高風險", 
            "ai_prediction": analysis_prompt, 
            "news": "最新市場數據已整合 RSI 與 KD 技術指標分析。"
        }
        return data
        
    except Exception as e:
        print(f"處理 {ticker_symbol} 時發生錯誤: {e}")
        # 返回一個錯誤狀態的字典，確保自動化流程不會中斷
        return {
            "price": 0, "eps": 0, "pe": 0, "black_swan": "未知",
            "ai_prediction": "無法取得分析數據，請稍後再試。",
            "news": "更新失敗。"
        }
