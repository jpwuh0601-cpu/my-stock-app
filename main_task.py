import sys
import os
import traceback
import argparse

# 確保當前目錄在系統路徑中，讓 Python 能順利找到 worker.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import worker
except ImportError as e:
    print(f"致命錯誤：無法匯入 worker 模組。請確認 worker.py 是否存在於 {current_dir}")
    print(f"錯誤詳情: {e}")
    sys.exit(1)

def run():
    """
    執行即時分析程式。
    此函數接收 --ticker 參數並立即調用 worker 進行單一股票分析，
    並將結果寫入 analysis_result.txt 以供前端讀取。
    """
    parser = argparse.ArgumentParser(description="金融數據即時分析工具")
    parser.add_argument('--ticker', type=str, required=True, help="指定要即時查詢的單一股票代號")
    args = parser.parse_args()

    try:
        print(f"正在執行單一標的即時分析: {args.ticker}")
        
        # 呼叫 worker 進行即時抓取與 AI 分析
        result = worker.get_ai_analysis(args.ticker)
        
        # 將結果寫入檔案，讓前端 app.py 可以讀取顯示
        output_file = os.path.join(current_dir, "analysis_result.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            
        print(f"標的 {args.ticker} 分析完成。結果已寫入 analysis_result.txt")
        
    except Exception as e:
        print("執行即時分析程序時發生錯誤:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run()
