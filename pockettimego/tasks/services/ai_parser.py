import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re
import time

# 設定 API key
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


def extract_json_from_text(text: str):
    """
    從模型輸出中提取 JSON 內容（移除 ```json ... ``` 與雜訊）
    """
    if not text:
        return None

    # 1️⃣ 去掉 Markdown 標記
    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip()

    # 2️⃣ 嘗試找出第一個 {...} 區塊
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return match.group(0).strip()
    return cleaned


def call_gemini_api(task_title, task_description, max_retries=3):
    """
    呼叫 Gemini API，回傳預估時間、環境、優先度
    若解析失敗則自動重試最多 3 次，並輸出 debug 訊息
    """
    prompt = f"""
我有一個任務：
標題：{task_title}
描述：{task_description}

請幫我生成：
1. 預估時間（分鐘）
2. 任務需求（以下選項之一：需要電腦、需要紙筆、需要平板、安靜環境、團隊合作、運動空間、飲食/邊吃邊做、洗衣相關、休閒/放鬆、其他）
3. 優先順序（1~3）
### 規則
1.請用 JSON 格式回傳，例如：
{{
    "estimated_time": 45,
    "environment": "需要電腦",
    "priority": 2
}}
2.請只回傳 JSON，不要包含任何其他文字或說明。
"""

    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    for attempt in range(1, max_retries + 1):
        print(f"\n🌀 第 {attempt} 次呼叫 Gemini API...")
        try:
            response = model.generate_content(prompt)
            raw_text = getattr(response, "text", None)
            print(f"🔍 [DEBUG] 模型回傳內容:\n{raw_text}\n")

            json_text = extract_json_from_text(raw_text)
            print(f"🧩 [DEBUG] 清理後 JSON 字串:\n{json_text}\n")

            if not json_text:
                raise ValueError("無法提取 JSON 內容")

            result = json.loads(json_text)
            print("✅ 成功解析 JSON！")

            return {
                "estimated_time": result.get("estimated_time", 30),
                "environment": result.get("environment", "其他"),
                "priority": result.get("priority", 2)
            }

        except Exception as e:
            print(f"⚠️ 第 {attempt} 次嘗試失敗：{e}")
            if attempt < max_retries:
                time.sleep(1)
            else:
                print("❌ 全部重試失敗，使用預設值。")

    return {"estimated_time": 30, "environment": "其他", "priority": 2}


# 測試執行
if __name__ == "__main__":
    result = call_gemini_api("寫報告", "整理資料結構期末報告")
    print("\n📦 最終結果：", result)
