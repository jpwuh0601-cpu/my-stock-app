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
    執行分析程式。現在支援透過參數輸入單一股票代號，
    若無參數，則維持預設的 tickers.txt 批次模式。
    """
    parser = argparse.ArgumentParser(description="金融數據分析工具")
    parser.add_argument('--ticker', type=str, help="指定要查詢的單一股票代號")
    args = parser.parse_args()

    try:
        if args.ticker:
            print(f"正在執行單一標的分析: {args.ticker}")
            # 這裡可以根據需要調整 worker 以支援單一標的快速分析
            worker.get_ai_analysis(args.ticker)
            print(f"標的 {args.ticker} 分析完成。")
        else:
            print("未指定代號，啟動預設批次分析程序...")
            worker.run_analysis_and_update()
            print("批次分析程序已順利完成。")
    except Exception as e:
        print("執行分析程序時發生錯誤:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run()
