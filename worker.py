def get_ai_insight(report_data):
    """若沒有客戶端或 API 額度，則直接回傳提示無法分析"""
    if not client:
        return "（未配置 OpenAI API，無法進行深度分析）"
    
    # ... 略 ...
    try:
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    except Exception as e:
        # 當額度用完時，這裡會捕捉到錯誤並回傳給 LINE
        return f"AI 分析暫時無法使用 (原因: {str(e)[:20]}...)"
