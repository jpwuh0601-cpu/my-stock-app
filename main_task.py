import sys
import os
import traceback
import argparse

# 強制將當前目錄放入 sys.path，確保可以找到 worker.py
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run():
    parser = argparse.ArgumentParser()
    # 提供預設值以避免 GitHub Action 因缺少參數而報錯
    parser.add_argument('--ticker', type=str, default="2330.TW", help="股票代號")
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        # 顯示目錄除錯資訊
        print(f"DEBUG: 當前目錄檔案清單: {os.listdir(current_dir)}")
        
        worker_path = os.path.join(current_dir, "worker.py")
        if not os.path.exists(worker_path):
            raise ImportError(f"找不到 worker.py，路徑: {worker_path}")
            
        import worker
        
        # 處理股票代號格式
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在執行分析: {ticker_symbol}")
        
        # 呼叫分析函數
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 將結果寫入檔案
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except Exception as e:
        # 當發生錯誤時，將錯誤寫入檔案並記錄至日誌，方便 GitHub Actions 追蹤
        error_msg = f"--- 分析失敗 ---\n錯誤類型: {type(e).__name__}\n錯誤訊息: {str(e)}\n\n詳細堆疊:\n{traceback.format_exc()}"
        print(error_msg)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
        
        # 發生錯誤時確保程式結束碼為 1，通知 GitHub Action 任務失敗
        sys.exit(1)

if __name__ == "__main__":
    run()
