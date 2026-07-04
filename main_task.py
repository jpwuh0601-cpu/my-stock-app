import sys
import os
import traceback
import argparse

# 強制將當前目錄放入 sys.path，確保 worker.py 可以被找到
current_dir = os.path.abspath(os.path.dirname(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run():
    """
    更新後的執行邏輯：
    整合三大法人、十大券商明細、黑天鵝警示與新聞解讀。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True)
    args = parser.parse_args()

    output_file = os.path.join(current_dir, "analysis_result.txt")
    
    try:
        import worker
        
        ticker_symbol = args.ticker.strip()
        if ticker_symbol.isdigit() and not ticker_symbol.endswith(('.TW', '.TWO')):
            ticker_symbol += ".TW"
            
        print(f"正在執行深度分析: {ticker_symbol}")
        
        # 呼叫 worker 進行進階 AI 分析
        # 預期 worker.get_ai_analysis 現在會回傳包含表格與警示的完整分析報告
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 寫入包含表格數據的完整結果
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("### AI 深度金融分析報告\n\n")
            f.write(result)
            
    except ImportError as ie:
        error_msg = f"匯入錯誤 (ImportError): {str(ie)}\n請確保 worker.py 已更新支援表格輸出。"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
    except Exception as e:
        error_msg = f"分析失敗: {str(e)}\n{traceback.format_exc()}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run()
