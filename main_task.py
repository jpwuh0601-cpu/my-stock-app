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
        # 使用絕對路徑確保能正確載入 worker
        worker_path = os.path.join(current_dir, "worker.py")
        if not os.path.exists(worker_path):
            raise ImportError("找不到 worker.py，請確認檔案是否已部署至正確路徑。")
            
        import worker
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 確保以 UTF-8 無 BOM 格式寫入，並加入寫入防錯
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except Exception as e:
        # 記錄錯誤並在 Canvas 中顯示詳細錯誤資訊，方便前端除錯
        error_info = f"分析失敗: {str(e)}\n{traceback.format_exc()}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_info)
        # 讓程式以非零狀態碼結束，以便於偵測部署失敗
        sys.exit(1)

if __name__ == "__main__":
    run()
