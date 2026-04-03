# -*- coding: utf-8 -*-
"""
导出对话框模块
用于导出最终文档结果
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel
)
from qfluentwidgets import PushButton, PrimaryPushButton, ComboBox

from components.custom_folder import CustomFolder


class ExportDialog(QDialog):
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
        super().__init__(parent)

        # 设置对话框属性
        self.setWindowTitle("导出文档")
        self.setMinimumSize(450, 180)

        # 初始化 UI
        self._init_ui()

    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ============= GridLayout 表单区域 =============
        grid_layout = QGridLayout()
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

        # ============= 底部按钮区域 =============
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # 导出按钮（在左侧）
        self.export_button = PrimaryPushButton("导出")
        self.export_button.clicked.connect(self._on_export_clicked)
        self.export_button.setEnabled(False)  # 初始禁用，直到选择路径
        button_layout.addWidget(self.export_button)

        # 取消按钮（在右侧）
        self.cancel_button = PushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # 将所有组件添加到主布局
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

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

        # 发出信号并关闭
        self.export_confirmed.emit(folder_path, fmt)
        self.accept()
