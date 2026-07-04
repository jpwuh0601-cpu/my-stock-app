import sys
import os
import traceback
import argparse

# 強制將當前目錄放入 sys.path，確保 worker.py 可以被找到
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run():
    parser = argparse.ArgumentParser()
    # 將 ticker 改為選填，預設為 2330.TW
    parser.add_argument('--ticker', type=str, default="2330.TW", help="股票代號")
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        import worker
        
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在啟動深度分析: {ticker_symbol}")
        
        result = worker.get_ai_analysis(ticker_symbol)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except ImportError as ie:
        # 這是網頁端最常見的錯誤，請確認 worker.py 是否存在於同一目錄
        error_msg = f"匯入錯誤: 請確認 worker.py 是否已正確部署。\n詳細錯誤: {str(ie)}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
    except Exception as e:
        error_msg = f"分析失敗: {str(e)}\n{traceback.format_exc()}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run()
