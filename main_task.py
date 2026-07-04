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
    明確定義分析維度，包括法人籌碼、十大券商、黑天鵝警示與 AI 解讀。
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
            
        print(f"正在啟動深度分析: {ticker_symbol}")
        
        # 呼叫 worker 進行進階 AI 分析
        # 確保 worker.py 的 get_ai_analysis 函數會執行以下步驟：
        # 1. 抓取過去 10 日法人與主力券商籌碼並繪製表格
        # 2. 綜合新聞分析黑天鵝等級
        # 3. 輸出 GPT 綜合解讀
        result = worker.get_ai_analysis(ticker_symbol)
        
        # 寫入包含表格數據的完整分析報告，供前端顯示
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"### {ticker_symbol} 深度金融分析報告\n\n")
            f.write(result)
            
    except ImportError as ie:
        error_msg = f"匯入錯誤 (ImportError): {str(ie)}\n請確認 worker.py 是否包含完整的籌碼分析邏輯。"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)
    except Exception as e:
        error_msg = f"分析失敗: {str(e)}\n{traceback.format_exc()}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run()
