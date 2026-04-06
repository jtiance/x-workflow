# -*- coding: utf-8 -*-
"""
导出对话框模块
用于导出最终文档结果
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QWidget
)
from qfluentwidgets import ComboBox, LineEdit

from components.custom_folder import CustomFolder
from .custom_dialog import CustomDialog


class ExportDialog(CustomDialog):
    """
    导出对话框
    """

    # 定义信号：当用户确认导出时发出
    export_confirmed = Signal(str, str, str)  # folder_path, filename, format

    def __init__(self, text_content="", parent=None):
        """
        初始化导出对话框

        Args:
            text_content: 文本内容，用于生成默认文件名
            parent: 父控件
        """
        super().__init__(title="导出文档", parent=parent)

        # 设置对话框属性
        self.setMinimumSize(450, 220)

        # ============= GridLayout 表单区域 =============
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(10)

        # 第一行：导出路径
        path_label = QLabel("导出路径:")
        self.path_input = CustomFolder()
        self.path_input.setPlaceholderText("请选择导出目录...")

        grid_layout.addWidget(path_label, 0, 0)
        grid_layout.addWidget(self.path_input, 0, 1)

        # 第二行：文件名
        filename_label = QLabel("文件名:")
        self.filename_input = LineEdit()
        self.filename_input.setPlaceholderText("请输入文件名...")
        # 设置默认文件名（取文本第一行的前10个字）
        default_filename = self._extract_default_filename(text_content)
        self.filename_input.setText(default_filename)

        grid_layout.addWidget(filename_label, 1, 0)
        grid_layout.addWidget(self.filename_input, 1, 1)

        # 第三行：格式
        format_label = QLabel("格式:")
        self.format_combo = ComboBox()
        self.format_combo.addItem("*.txt")

        grid_layout.addWidget(format_label, 2, 0)
        grid_layout.addWidget(self.format_combo, 2, 1)

        # 设置列伸展因子，让输入框占更多空间
        grid_layout.setColumnStretch(1, 1)

        # 将表单添加到内容区域
        self.add_content_widget(form_widget)

        # ============= 底部按钮区域 =============
        # 取消按钮
        self.add_button("取消", is_reject=True)
        # 导出按钮（主按钮）
        self.export_button = self.add_button("导出", callback=self._on_export_clicked, is_primary=True, is_accept=True)
        self.export_button.setEnabled(False)  # 初始禁用，直到选择路径

        # 连接信号
        self.path_input.textChanged.connect(self._on_input_changed)
        self.filename_input.textChanged.connect(self._on_input_changed)

    def _extract_default_filename(self, text_content):
        """
        从文本内容中提取默认文件名（取第一行的前10个字）

        Args:
            text_content: 文本内容

        Returns:
            str: 默认文件名
        """
        if not text_content:
            return ""

        # 取第一行
        first_line = text_content.strip().split("\n")[0] if "\n" in text_content else text_content.strip()
        if not first_line:
            return ""

        # 取前10个字
        filename = first_line[:10].strip()

        # 移除文件名中非法的字符
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            filename = filename.replace(char, '')

        return filename

    def _on_input_changed(self, _):
        """
        当输入改变时调用
        """
        # 启用/禁用导出按钮
        has_path = bool(self.path_input.text().strip())
        has_filename = bool(self.filename_input.text().strip())
        self.export_button.setEnabled(has_path and has_filename)

    def _on_export_clicked(self):
        """
        当点击导出按钮时调用
        """
        folder_path = self.path_input.text().strip()
        filename = self.filename_input.text().strip()
        if not folder_path or not filename:
            return

        # 获取格式（去掉 *.）
        fmt = self.format_combo.currentText().replace("*.", "")

        # 发出信号
        self.export_confirmed.emit(folder_path, filename, fmt)
