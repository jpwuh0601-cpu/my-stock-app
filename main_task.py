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
        import worker
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 確保以 UTF-8 無 BOM 格式寫入
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except Exception as e:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"分析失敗: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    run()
