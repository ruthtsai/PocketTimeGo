import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# 載入 .env
load_dotenv()

# 設定 API key
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

def call_gemini_api(task_title, task_description):
    """
    呼叫 Gemini API，回傳預估時間、環境、優先度
    """
    prompt = f"""
我有一個任務：
標題：{task_title}
描述：{task_description}

請幫我生成：
1. 預估時間（分鐘）
2. 建議環境（電腦、紙筆、安靜空間）
3. 優先順序（1~5）
請用 JSON 格式回傳，例如：
{{
    "estimated_time": 45,
    "environment": "電腦",
    "priority": 3
}}
"""

    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content(prompt)

    # response.text 會包含文字回應
    #print(response.text)

    try:
        result = json.loads(response.text)
        return {
            "estimated_time": result.get("estimated_time", 30),
            "environment": result.get("environment", "電腦"),
            "priority": result.get("priority", 3)
        }
    except Exception:
        # 解析失敗使用預設值
        return {"estimated_time": 30, "environment": "電腦", "priority": 3}

#print(call_gemini_api("寫報告", "整理期末報告"))
