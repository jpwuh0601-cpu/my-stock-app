import sys
import os
import traceback
import argparse
import subprocess

# 1. 強制設定環境路徑
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. 預檢檢查：確認 yfinance 是否存在，若無則嘗試安裝 (針對環境異常)
try:
    import yfinance
except ImportError:
    print("警告：未檢測到 yfinance，嘗試自動補安裝...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance

# 3. 匯入 worker
try:
    import worker
except ImportError as e:
    print(f"致命錯誤：無法匯入 worker 模組。")
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
        error_msg = f"分析失敗: {str(e)}\n建議：請檢查代號是否正確，或稍後再試。"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run()
