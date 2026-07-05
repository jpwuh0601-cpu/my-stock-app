import pandas as pd

def generate_ai_analysis(ticker_symbol, info, institutional_data=None, broker_data=None, news_headlines=None):
    """
    整合深度分析邏輯：
    1. 三大法人與券商數據格式化
    2. 黑天鵝風險解讀
    3. AI 主力動能分析
    """
    
    # 1. 處理籌碼數據表格 (DataFrame 格式)
    inst_df = pd.DataFrame(institutional_data) if institutional_data else pd.DataFrame()
    broker_df = pd.DataFrame(broker_data) if broker_data else pd.DataFrame()
    
    # 2. 黑天鵝風險解讀 (GPT 風險分析)
    news_summary = analyze_black_swan(news_headlines)
    
    # 3. AI 主力分析邏輯
    主力觀點 = "籌碼集中度分析："
    if not inst_df.empty:
        total_buy = inst_df['外資'].sum() + inst_df['投信'].sum()
        主力觀點 += f" 近10日法人合計買賣超 {total_buy} 張。"
    else:
        主力觀點 += " 暫無完整法人數據。"
        
    # 整合最終報告
    report = {
        "summary": f"【{ticker_symbol} 深度報告】",
        "institutional_table": inst_df,
        "broker_table": broker_df,
        "black_swan_alert": news_summary,
        "ai_主力分析": 主力觀點
    }
    
    return report

def analyze_black_swan(news_list):
    """
    GPT 新聞解讀模擬器
    """
    if not news_list:
        return "新聞平靜，未見顯著黑天鵝風險。"
    
    # 這裡未來可串接您的 LLM API 來解析新聞關鍵字
    risky_keywords = ['違約', '訴訟', '罷工', '停產', '裁員']
    found = [k for k in risky_keywords if any(k in n for n in news_list)]
    
    if found:
        return f"⚠️ 風險警示：檢測到相關關鍵字 {found}，建議降低持倉。"
    return "✅ 新聞面解讀：目前未發現重大黑天鵝風險。"

# 測試用：模擬資料結構
if __name__ == "__main__":
    sample_inst = [{"日期": f"2026-07-{i}", "外資": i*100, "投信": i*50} for i in range(1, 11)]
    report = generate_ai_analysis("2330.TW", {}, institutional_data=sample_inst)
    print(report['ai_主力分析'])
