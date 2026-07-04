import sys
import os
import traceback
import argparse

# 確保當前目錄絕對路徑已被加入至系統路徑，解決匯入失敗問題
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    import worker
except ImportError as e:
    # 紀錄目錄資訊以便除錯
    print(f"致命錯誤：無法匯入 worker 模組。")
    print(f"當前工作目錄: {os.getcwd()}")
    print(f"腳本所在目錄: {current_dir}")
    print(f"系統路徑: {sys.path}")
    print(f"錯誤詳情: {e}")
    sys.exit(1)

def run():
    """
    修正版執行邏輯：確保任何錯誤都會寫入檔案，而不是崩潰退出。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True)
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        # 自動補全台股後綴
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在分析標的: {ticker_symbol}")
        
        # 呼叫 worker 進行分析
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 寫入成功結果
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            
    except Exception as e:
        # 將錯誤資訊記錄到檔案中，前端就能顯示出「分析失敗」的說明，而不是直接報錯
        error_msg = f"分析失敗: {str(e)}\n建議：請檢查代號是否正確，或稍後再試。"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
        # 這裡不呼叫 sys.exit(1)，避免導致網頁前端報錯退出

if __name__ == "__main__":
    run()
