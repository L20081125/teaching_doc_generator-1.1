#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeek API 客户端 - 修复版"""

import requests
import os

class DeepSeekClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"

    def generate_teaching_doc(self, prompt: str, model: str = None) -> str:
        # 如果没有 API Key，返回模拟数据以防报错
        if not self.api_key or self.api_key == "sk-...":
            return "【模拟模式】未配置有效的 API Key。\n\n这是一个测试文档，请在界面中输入正确的 DeepSeek API Key 以生成真实内容。"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model or self.model,
            "messages": [
                {"role": "system", "content": "你是一名专业的教学文档生成专家。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"API 调用出错：{str(e)}"
