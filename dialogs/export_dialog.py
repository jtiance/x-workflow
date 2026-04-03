# -*- coding: utf-8 -*-
"""
导出对话框模块
用于导出最终文档结果
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QWidget
)
from qfluentwidgets import ComboBox

from components.custom_folder import CustomFolder
from .custom_dialog import CustomDialog


class ExportDialog(CustomDialog):
    """
    导出对话框
    """

    # 定义信号：当用户确认导出时发出
    export_confirmed = Signal(str, str)  # folder_path, format

    def __init__(self, parent=None):
        """
        初始化导出对话框

        Args:
            parent: 父控件
        """
        super().__init__(title="导出文档", parent=parent)

        # 设置对话框属性
        self.setMinimumSize(450, 180)

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

        # 第二行：格式
        format_label = QLabel("格式:")
        self.format_combo = ComboBox()
        self.format_combo.addItem("*.txt")

        grid_layout.addWidget(format_label, 1, 0)
        grid_layout.addWidget(self.format_combo, 1, 1)

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
        self.path_input.textChanged.connect(self._on_path_changed)

    def _on_path_changed(self, text):
        """
        当路径输入改变时调用
        """
        # 启用/禁用导出按钮
        self.export_button.setEnabled(bool(text.strip()))

    def _on_export_clicked(self):
        """
        当点击导出按钮时调用
        """
        folder_path = self.path_input.text().strip()
        if not folder_path:
            return

        # 获取格式（去掉 *.）
        fmt = self.format_combo.currentText().replace("*.", "")

        # 发出信号
        self.export_confirmed.emit(folder_path, fmt)
