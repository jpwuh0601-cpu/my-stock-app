import json
import os
import importlib.util

def run_analysis():
    # 讀取 tickers.txt
    if not os.path.exists("tickers.txt"):
        print("找不到 tickers.txt")
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    # 動態載入 worker
    worker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "worker.py")
    spec = importlib.util.spec_from_file_location("worker", worker_path)
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)

    all_results = {}
    for ticker in tickers:
        print(f"正在分析: {ticker}")
        try:
            # 這裡假定 worker.py 中的分析函數會回傳該股票的資料字典
            # 若您的 worker.py 是存入 json 檔案，我們需要調整為回傳資料
            result = worker.get_ai_analysis_data(ticker) 
            all_results[ticker] = result
        except Exception as e:
            print(f"分析 {ticker} 失敗: {e}")

    # 統一儲存成一個大的 market_data.json
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print("所有股票分析完成並已更新 market_data.json")

if __name__ == "__main__":
    run_analysis()
