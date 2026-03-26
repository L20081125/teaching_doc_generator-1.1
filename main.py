# ==================== main.py ====================
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教学文档智能生成系统 - 主程序入口
版本：1.0.0
日期：2026-03-25
"""

import customtkinter as ctk
from gui.main_window import MainWindow

if __name__ == "__main__":
    # 设置外观模式
    ctk.set_appearance_mode("light")  # "dark" 或 "light"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

    # 创建并运行应用
    app = MainWindow()
    app.mainloop()