# ==================== gui/main_window.py ====================
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面 - 使用 CustomTkinter 构建现代化 GUI
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import datetime

# 确保导入路径正确，如果报错请检查 ai 和 core 文件夹是否存在
try:
    from ai.deepseek_client import DeepSeekClient
    from ai.qwen_client import QwenClient
    from core.document_generator import DocumentGenerator
except ImportError as e:
    print(f"警告：模块导入失败 {e}，请确保项目结构正确。")
    # 为了演示界面，即使导入失败也尽量让界面能跑起来（实际运行时会报错）
    DeepSeekClient = None
    QwenClient = None
    DocumentGenerator = None


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 窗口基本配置
        self.title("📚 教学文档智能生成系统 v1.0")
        self.geometry("1100x750")
        self.minsize(900, 650)

        # 2. 配置网格布局 (必须在创建子组件之前配置)
        self.grid_columnconfigure(0, weight=0)  # 侧边栏固定宽度
        self.grid_columnconfigure(1, weight=1)  # 主区域拉伸
        self.grid_rowconfigure(0, weight=1)

        # 3. 初始化 AI 客户端
        if DeepSeekClient:
            self.deepseek_client = DeepSeekClient()
            self.qwen_client = QwenClient()
            self.current_client = self.deepseek_client
        else:
            self.deepseek_client = None
            self.qwen_client = None
            self.current_client = None

        # 4. 创建界面组件 (只调用一次！)
        self._create_sidebar()
        self._create_main_area()

    def _create_sidebar(self):
        """创建左侧表单区域"""
        # 创建可滚动侧边栏
        self.sidebar = ctk.CTkScrollableFrame(self, width=420)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 定义输出格式变量
        self.output_format_var = ctk.StringVar(value="word")

        # 标题
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="📋 教学需求配置",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        # ===== 基础信息 =====
        info_frame = ctk.CTkFrame(self.sidebar)
        info_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(info_frame, text="📌 基础信息", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15,
                                                                                          pady=(10, 5))

        # 课程名称
        ctk.CTkLabel(info_frame, text="课程名称:").pack(anchor="w", padx=15, pady=(5, 0))
        self.course_name = ctk.CTkEntry(info_frame, placeholder_text="请输入课程名称", width=360)
        self.course_name.pack(padx=15, pady=5)

        # 教学专业 (自由输入)
        ctk.CTkLabel(info_frame, text="教学专业:").pack(anchor="w", padx=15, pady=(5, 0))
        self.major = ctk.CTkEntry(info_frame, placeholder_text="例如：计算机科学与技术", width=360)
        self.major.insert(0, "计算机科学与技术")
        self.major.pack(padx=15, pady=5)

        # 授课对象 (自由输入)
        ctk.CTkLabel(info_frame, text="授课对象:").pack(anchor="w", padx=15, pady=(5, 0))
        self.audience = ctk.CTkEntry(info_frame, placeholder_text="例如：本科二年级", width=360)
        self.audience.insert(0, "本科二年级")
        self.audience.pack(padx=15, pady=5)

        # 课时安排
        ctk.CTkLabel(info_frame, text="课时安排:").pack(anchor="w", padx=15, pady=(5, 0))
        self.hours_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        self.hours_frame.pack(anchor="w", padx=15, pady=5)
        self.hours_entry = ctk.CTkEntry(self.hours_frame, width=80, placeholder_text="学时")
        self.hours_entry.pack(side="left")
        ctk.CTkLabel(self.hours_frame, text=" 学时").pack(side="left")

        # ===== 教学要求 =====
        req_frame = ctk.CTkFrame(self.sidebar)
        req_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(req_frame, text="🎯 教学要求", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15,
                                                                                         pady=(10, 5))

        # 教学模式 (自由输入)
        ctk.CTkLabel(req_frame, text="教学模式:").pack(anchor="w", padx=15, pady=(5, 0))
        self.teaching_mode = ctk.CTkEntry(req_frame, placeholder_text="例如：混合式教学", width=360)
        self.teaching_mode.insert(0, "混合式教学")
        self.teaching_mode.pack(padx=15, pady=5)

        # 课程任务
        ctk.CTkLabel(req_frame, text="课程任务/目标:").pack(anchor="w", padx=15, pady=(5, 0))
        self.task_desc = ctk.CTkTextbox(req_frame, width=360, height=100)
        self.task_desc.pack(padx=15, pady=5)
        self.task_desc.insert("1.0", "请描述本课程的主要任务和教学目标...")

        # 考核方式 (自由输入)
        ctk.CTkLabel(req_frame, text="考核方式:").pack(anchor="w", padx=15, pady=(5, 0))
        self.assessment = ctk.CTkEntry(req_frame, placeholder_text="例如：综合评估", width=360)
        self.assessment.insert(0, "综合评估")
        self.assessment.pack(padx=15, pady=5)

        # ===== 文档配置 =====
        doc_frame = ctk.CTkFrame(self.sidebar)
        doc_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(doc_frame, text="📄 文档配置", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15,
                                                                                         pady=(10, 5))

        # 文档类型
        ctk.CTkLabel(doc_frame, text="文档类型:").pack(anchor="w", padx=15, pady=(5, 0))
        self.doc_type = ctk.CTkComboBox(doc_frame,
                                        values=["教学大纲", "教案设计", "课件 PPT 大纲", "实验指导书",
                                                "课程计划书", "学习指导手册", "考核方案"],
                                        width=360)
        self.doc_type.set("教学大纲")
        self.doc_type.pack(padx=15, pady=5)

        # 输出格式
        ctk.CTkLabel(doc_frame, text="输出格式:").pack(anchor="w", padx=15, pady=(5, 0))
        self.format_frame = ctk.CTkFrame(doc_frame, fg_color="transparent")
        self.format_frame.pack(anchor="w", padx=15, pady=5)

        self.format_word = ctk.CTkRadioButton(self.format_frame, text="Word (.docx)", value="word",
                                              variable=self.output_format_var)
        self.format_word.pack(side="left", padx=5)

        self.format_pdf = ctk.CTkRadioButton(self.format_frame, text="PDF", value="pdf",
                                             variable=self.output_format_var)
        self.format_pdf.pack(side="left", padx=5)
        self.format_word.select()

        # 详细程度
        ctk.CTkLabel(doc_frame, text="内容详细程度:").pack(anchor="w", padx=15, pady=(5, 0))
        self.detail_level = ctk.CTkSegmentedButton(doc_frame, values=["简洁", "标准", "详细"])
        self.detail_level.set("标准")
        self.detail_level.pack(padx=15, pady=5)

        # ===== AI 配置 (🔴 重点修复：添加了 api_key_entry) =====
        ai_frame = ctk.CTkFrame(self.sidebar)
        ai_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(ai_frame, text="🤖 AI 模型配置", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15,
                                                                                           pady=(10, 5))

        # 选择模型
        ctk.CTkLabel(ai_frame, text="选择模型:").pack(anchor="w", padx=15, pady=(5, 0))
        self.ai_model = ctk.CTkComboBox(
            ai_frame,
            values=["DeepSeek-R1 (推荐)", "DeepSeek-V3", "通义千问-Qwen3", "自动选择"],
            width=360,
            command=self._on_model_change
        )
        self.ai_model.set("DeepSeek-R1 (推荐)")
        self.ai_model.pack(padx=15, pady=5)

        # 🔴 新增：API Key 输入框
        ctk.CTkLabel(ai_frame, text="API Key:").pack(anchor="w", padx=15, pady=(5, 0))
        self.api_key_entry = ctk.CTkEntry(
            ai_frame,
            placeholder_text="sk-... (请输入您的 API Key)",
            width=360,
            show="*"  # 隐藏输入内容
        )
        self.api_key_entry.pack(padx=15, pady=5)

        # 提示文本
        hint_label = ctk.CTkLabel(
            ai_frame,
            text="💡 首次使用请前往 DeepSeek 或阿里云 DashScope 官网获取",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        hint_label.pack(anchor="w", padx=15, pady=(0, 10))

        # ===== 生成按钮 =====
        self.generate_btn = ctk.CTkButton(
            self.sidebar,
            text="🚀 生成教学文档",
            command=self._start_generation,
            fg_color="#2E86AB",
            hover_color="#1A5F7A",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.generate_btn.pack(pady=20, padx=15, fill="x")

        # 进度条和状态 (只定义一次)
        self.progress_bar = ctk.CTkProgressBar(self.sidebar)
        self.progress_bar.pack(padx=15, pady=10, fill="x")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.sidebar, text="就绪", text_color="gray")
        self.status_label.pack(pady=5)

        # 调试打印
        print("✅ DEBUG: _create_sidebar 执行完毕！")
        print(f"   - api_key_entry exists: {hasattr(self, 'api_key_entry')}")
        print(f"   - ai_model exists: {hasattr(self, 'ai_model')}")

    def _create_main_area(self):
        """创建右侧预览区域"""
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 标题栏
        header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            header_frame,
            text="📄 内容预览",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")

        # 操作按钮
        self.copy_btn = ctk.CTkButton(header_frame, text="📋 复制内容", width=100, command=self._copy_content)
        self.copy_btn.pack(side="right", padx=5)

        self.save_btn = ctk.CTkButton(header_frame, text="💾 保存文件", width=100, command=self._save_file,
                                      state="disabled")
        self.save_btn.pack(side="right", padx=5)

        self.clear_btn = ctk.CTkButton(header_frame, text="🗑️ 清空", width=80, command=self._clear_preview,
                                       fg_color="gray")
        self.clear_btn.pack(side="right", padx=5)

        # 预览文本框
        self.preview_text = ctk.CTkTextbox(self.main_area, font=ctk.CTkFont(family="Consolas", size=12))
        self.preview_text.pack(padx=15, pady=10, fill="both", expand=True)

        # 底部信息
        info_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=5)
        self.word_count_label = ctk.CTkLabel(info_frame, text="字数：0", text_color="gray")
        self.word_count_label.pack(side="left")
        self.time_label = ctk.CTkLabel(info_frame, text="生成时间：-", text_color="gray")
        self.time_label.pack(side="right")

    def _on_model_change(self, selection):
        """模型选择变更处理"""
        if not self.deepseek_client or not self.qwen_client:
            return

        if "DeepSeek" in selection:
            self.current_client = self.deepseek_client
        elif "通义千问" in selection or "Qwen" in selection:
            self.current_client = self.qwen_client
        else:
            self.current_client = self.deepseek_client

    def _start_generation(self):
        """开始生成文档（异步）"""
        # 1. 验证课程名称
        if not self.course_name.get().strip():
            messagebox.showwarning("警告", "请输入课程名称！")
            self.course_name.focus()
            return

        # 2. 验证 API Key (现在可以正常获取了)
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("警告", "请输入 API Key！\n可在 DeepSeek 或阿里云官网获取")
            self.api_key_entry.focus()
            return

        # 3. 设置 API Key 到客户端
        if self.current_client:
            self.current_client.api_key = api_key
        else:
            messagebox.showerror("错误", "AI 客户端未初始化，请检查代码导入。")
            return

        # 4. 更新 UI 状态
        self.generate_btn.configure(state="disabled", text="⏳ 生成中...")
        self.progress_bar.set(0)
        self.status_label.configure(text="正在调用 AI 生成内容...", text_color="#2E86AB")
        self.save_btn.configure(state="disabled")

        # 5. 启动后台线程
        thread = threading.Thread(target=self._generate_content, daemon=True)
        thread.start()

    def _generate_content(self):
        """生成内容（后台线程）"""
        try:
            # 步骤 1: 构建数据
            self.after(0, lambda: self.progress_bar.set(0.2))
            self.after(0, lambda: self.status_label.configure(text="正在整理需求..."))

            data = self._collect_form_data()
            prompt = self._build_prompt(data)

            # 步骤 2: 调用 AI
            self.after(0, lambda: self.progress_bar.set(0.4))
            self.after(0, lambda: self.status_label.configure(text="AI 正在思考并撰写..."))

            content = self.current_client.generate_teaching_doc(prompt)

            # 步骤 3: 显示结果
            self.after(0, lambda: self.progress_bar.set(0.8))
            self.after(0, lambda: self.status_label.configure(text="正在格式化..."))

            self.after(0, lambda: self.preview_text.delete("1.0", "end"))
            self.after(0, lambda: self.preview_text.insert("1.0", content))
            self.after(0, lambda: self._update_word_count(content))

            # 保存临时数据
            self.generated_content = content
            self.generated_data = data

            # 完成
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self.status_label.configure(text="✅ 生成完成！", text_color="green"))
            self.after(0, lambda: self.save_btn.configure(state="normal"))

        except Exception as e:
            error_msg = str(e)
            print(f"生成错误：{error_msg}")
            self.after(0, lambda: self.status_label.configure(text=f"❌ 生成失败", text_color="red"))
            self.after(0, lambda: messagebox.showerror("生成错误",
                                                       f"发生错误：{error_msg}\n\n请检查 API Key 是否正确或网络是否通畅。"))
        finally:
            self.after(0, lambda: self.generate_btn.configure(state="normal", text="🚀 生成教学文档"))

    def _collect_form_data(self) -> dict:
        """收集表单数据"""
        return {
            "course_name": self.course_name.get(),
            "major": self.major.get(),
            "audience": self.audience.get(),
            "hours": self.hours_entry.get(),
            "teaching_mode": self.teaching_mode.get(),
            "task_desc": self.task_desc.get("1.0", "end-1c"),
            "assessment": self.assessment.get(),
            "doc_type": self.doc_type.get(),
            "output_format": self.output_format_var.get(),
            "detail_level": self.detail_level.get()
        }

    def _build_prompt(self, data: dict) -> str:
        """构建 AI 提示词"""
        detail_instructions = {
            "简洁": "请简洁明了，控制在 1500 字以内",
            "标准": "请详细完整，控制在 3000-4000 字",
            "详细": "请非常详细，包含所有细节，控制在 5000 字以上"
        }

        return f"""你是一名专业的教学文档生成专家，请根据以下信息生成一份规范的教学文档。

【文档类型】{data['doc_type']}

【课程信息】
- 课程名称：{data['course_name']}
- 教学专业：{data['major']}
- 授课对象：{data['audience']}
- 课时安排：{data['hours']} 学时
- 教学模式：{data['teaching_mode']}

【课程任务与目标】
{data['task_desc']}

【考核方式】{data['assessment']}

【输出要求】
1. 按照标准{data['doc_type']}格式输出，结构清晰完整
2. {detail_instructions[data['detail_level']]}
3. 语言专业规范，适合{data['major']}专业
4. 包含必要的教学目标、内容安排、方法设计、评估方式等
5. 使用 Markdown 格式，便于后续转换为 Word/PDF

请直接输出文档内容，无需额外说明。"""

    def _update_word_count(self, content: str):
        """更新字数统计"""
        count = len(content.replace(" ", "").replace("\n", ""))
        self.word_count_label.configure(text=f"字数：{count}")
        self.time_label.configure(text=f"生成时间：{datetime.datetime.now().strftime('%H:%M:%S')}")

    def _copy_content(self):
        """复制内容到剪贴板"""
        content = self.preview_text.get("1.0", "end-1c")
        if content.strip():
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("成功", "内容已复制到剪贴板！")
        else:
            messagebox.showwarning("提示", "没有可复制的内容。")

    def _clear_preview(self):
        """清空预览"""
        self.preview_text.delete("1.0", "end")
        self.word_count_label.configure(text="字数：0")
        self.time_label.configure(text="生成时间：-")
        self.save_btn.configure(state="disabled")
        self.status_label.configure(text="已清空", text_color="gray")

    def _save_file(self):
        """保存文件"""
        if not hasattr(self, 'generated_content'):
            messagebox.showwarning("警告", "请先生成内容！")
            return

        if not DocumentGenerator:
            messagebox.showerror("错误", "文档生成模块未加载，无法保存文件。")
            return

        file_type = self.output_format_var.get()

        if file_type == "pdf":
            default_ext = ".pdf"
            file_types_list = [("PDF 文件", "*.pdf")]
        else:
            default_ext = ".docx"
            file_types_list = [("Word 文档", "*.docx"), ("文本文件", "*.txt")]

        save_path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=file_types_list,
            initialfile=f"{self.course_name.get()}_{self.doc_type.get()}"
        )

        if save_path:
            try:
                generator = DocumentGenerator()
                # 注意：这里假设你的 DocumentGenerator 支持 save_document 方法
                # 如果该方法签名不同，请相应调整
                generator.save_document(self.generated_content, self.generated_data, save_path)
                messagebox.showinfo("成功", f"文档已保存至：\n{save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()