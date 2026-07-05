def generate_ai_analysis(ticker_symbol, info):
    """
    結合基本面與籌碼面的 AI 決策邏輯
    """
    pe = info.get('forwardPE', 20)
    eps = info.get('trailingEps', 0)
    
    # 根據機構持股比例或其他指標模擬籌碼集中度
    # 此處假設若 floatShares 數據存在則進行簡單評分
    shares = info.get('floatShares', 1)
    institutional_buy = (shares * 0.05)  # 模擬數據
    
    # AI 決策分析邏輯
    analysis = f"綜合分析：本益比 {pe:.2f}，EPS {eps:.2f}。"
    
    # 籌碼面權重
    if institutional_buy > 1000000:
        analysis += " 【籌碼集中】機構持續買入，動能強勁。"
    else:
        analysis += " 【籌碼偏弱】機構動作保守，建議謹慎。"
    
    # 最終決策
    if pe < 15 and eps > 5 and institutional_buy > 1000000:
        analysis += " 🚀 總結：強力買入訊號。"
    elif pe > 30:
        analysis += " ⚠️ 總結：風險警示，高本益比。"
    else:
        analysis += " 📊 總結：建議觀望，維持現狀。"
        
    return analysis
