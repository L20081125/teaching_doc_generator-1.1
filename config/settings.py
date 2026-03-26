# config/settings.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置文件
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AIConfig:
    """AI配置"""
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    DEFAULT_MODEL: str = "deepseek-chat"
    MAX_TOKENS: int = 8000
    TEMPERATURE: float = 0.7
    TIMEOUT: int = 60


@dataclass
class DocConfig:
    """文档配置"""
    TEMPLATE_DIR: Path = Path(__file__).parent.parent / "templates"
    OUTPUT_DIR: Path = Path(__file__).parent.parent / "output"
    SUPPORTED_FORMATS: list = None

    def __post_init__(self):
        if self.SUPPORTED_FORMATS is None:
            self.SUPPORTED_FORMATS = ["docx", "pdf", "txt"]
        # 确保目录存在
        self.TEMPLATE_DIR.mkdir(exist_ok=True)
        self.OUTPUT_DIR.mkdir(exist_ok=True)


@dataclass
class UIConfig:
    """UI配置"""
    WINDOW_TITLE: str = "📚 教学文档智能生成系统 v1.0"
    WINDOW_WIDTH: int = 1100
    WINDOW_HEIGHT: int = 750
    THEME: str = "light"  # "light" 或 "dark"
    COLOR_THEME: str = "blue"  # "blue", "green", "dark-blue"


# 全局配置实例
ai_config = AIConfig()
doc_config = DocConfig()
ui_config = UIConfig()