#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问 (DashScope) API 客户端
用于生成教学文档
"""
import os
import requests


def generate_teaching_doc(prompt: str, api_key: str = None) -> str:
    """
    【极简版】通义千问生成函数
    无需类，无需官方SDK，一行调用
    """
    # 1. 获取 Key (优先参数，其次环境变量)
    key = api_key or os.getenv("DASHSCOPE_API_KEY", "")

    # 2. 没 Key 直接返回模拟数据 (防崩溃)
    if not key or len(key) < 10:
        return f"【模拟模式】未配置 API Key。\n\n提示词：{prompt}\n\n(请配置 DASHSCOPE_API_KEY 以生成真实内容)"

    # 3. 直接发请求 (使用 qwen-turbo 模型，便宜且快)
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [
            {"role": "system", "content": "你是一名教学文档专家。"},
            {"role": "user", "content": prompt}
        ]},
        "parameters": {"result_format": "message"}
    }

    try:
        resp = requests.post(url, json=data, headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        # 提取内容
        return result["output"]["choices"][0]["message"]["content"]
    except Exception as e:
        return f"请求出错：{str(e)}"


# 兼容之前的类调用方式 (如果 GUI 里写了 QwenClient().generate...)
class QwenClient:
    def __init__(self, api_key=None): self.key = api_key

    def generate_teaching_doc(self, prompt, **kwargs):
        return generate_teaching_doc(prompt, self.key)