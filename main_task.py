import sys
import os
import traceback
import argparse

# 強制將當前目錄放入 sys.path，確保 worker.py 可以被找到
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run():
    """
    優化後的執行邏輯：
    改採更穩定的匯入方式，並在檔案層級進行錯誤防禦。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True)
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        # 於函數內部執行匯入，避免全域變數載入失敗導致程式直接崩潰
        import worker
        
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在分析標的: {ticker_symbol}")
        
        # 呼叫 worker 進行分析
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 寫入成功結果
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            
    except ImportError as ie:
        error_msg = f"匯入錯誤 (ImportError): {str(ie)}\n可能是 yfinance 或 worker 未正確安裝。請檢查 requirements.txt。"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
    except Exception as e:
        error_msg = f"分析失敗: {str(e)}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run()
