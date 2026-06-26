import os
import yfinance as yf
import requests
from openai import OpenAI

# 1. 安全讀取環境變數 (GitHub Actions 會提供)
api_key = os.environ.get("OPENAI_API_KEY")
line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not api_key or not line_token:
    print("錯誤：缺少環境變數 (Secrets)，請確認 GitHub Actions 設定。")
    exit(1)

client = OpenAI(api_key=api_key)

def run_auto_analysis(ticker="2330.TW"):
    # 2. 抓取數據
    # 使用 auto_adjust=True 確保股價經過還原權值處理
    df = yf.download(ticker, period="1mo", progress=False)
    
    if df.empty:
        print(f"無法取得 {ticker} 的數據")
        return

    # 3. 關鍵修正：將 Series 轉為純 float 數值
    # .item() 是將單一值的 Series 轉換為 Python float 的正確方式
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1].item()
    last_price = df['Close'].iloc[-1].item()
    
    # 4. AI 分析邏輯
    prompt = f"股票 {ticker}, 最新價 {last_price:.2f}, 20日均線 {sma_20:.2f}。請從技術面分析其趨勢，並給出簡短的買賣觀點。"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        analysis_text = response.choices[0].message.content
        
        # 5. 發送至 LINE
        msg = f"\n【智能投資管家報告】\n標的: {ticker}\n最新價: {last_price:.2f}\n20日均線: {sma_20:.2f}\n\n分析建議:\n{analysis_text}"
        
        headers = {"Authorization": f"Bearer {line_token}"}
        requests.post("https://notify-api.line.me/api/notify", 
                      headers=headers, 
                      data={"message": msg})
        print(f"{ticker} 分析報告已成功傳送至 LINE！")
        
    except Exception as e:
        print(f"執行過程發生錯誤: {e}")

if __name__ == "__main__":
    run_auto_analysis("2330.TW")
