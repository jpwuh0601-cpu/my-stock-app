import sys
import os
import traceback
import argparse

# 強制將當前目錄放入 sys.path
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, default="2330.TW", help="股票代號")
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        # 顯示當前目錄檔案清單，協助除錯 (這行在執行後會印在 GitHub Action 日誌)
        print(f"DEBUG: 當前工作目錄檔案: {os.listdir(current_dir)}")
        
        worker_path = os.path.join(current_dir, "worker.py")
        if not os.path.exists(worker_path):
            raise ImportError(f"找不到 worker.py，路徑: {worker_path}")
            
        import worker
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在分析: {ticker_symbol}")
        result = worker.get_ai_analysis(ticker_symbol)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except Exception as e:
        # 這裡將錯誤資訊詳細印出，GitHub Actions 的 Logs 會直接顯示
        error_msg = f"--- 分析失敗 ---\n錯誤類型: {type(e).__name__}\n錯誤訊息: {str(e)}\n\n詳細堆疊:\n{traceback.format_exc()}"
        print(error_msg)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
        
        # 強制結束並顯示錯誤碼 1，讓 GitHub Actions 記錄失敗
        sys.exit(1)

if __name__ == "__main__":
    run()
