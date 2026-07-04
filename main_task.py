import sys
import os
import traceback
import argparse

# 確保當前目錄在系統路徑中
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import worker
except ImportError as e:
    print(f"致命錯誤：無法匯入 worker 模組: {e}")
    sys.exit(1)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True)
    args = parser.parse_args()

    try:
        # 自動補全台股後綴 (若輸入為 4-6 位數字)
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit():
            ticker_symbol += ".TW"
            
        print(f"正在分析: {ticker_symbol}")
        
        # 呼叫 worker 進行分析
        result = worker.get_ai_analysis(ticker_symbol)
        
        output_file = os.path.join(current_dir, "analysis_result.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            
    except Exception as e:
        # 將錯誤寫入檔案，讓前端顯示錯誤訊息而非崩潰
        with open(os.path.join(current_dir, "analysis_result.txt"), "w", encoding="utf-8") as f:
            f.write(f"分析失敗: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
