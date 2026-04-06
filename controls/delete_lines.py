# -*- coding: utf-8 -*-
"""
删除指定行控件模块
删除指定起始行到终止行之间的内容
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QSizePolicy)
from qfluentwidgets import BodyLabel, SpinBox

from controls.base_control import BaseControl


class DeleteLinesControl(BaseControl):
    """
    删除指定行控件类
    删除用户指定的起始行到终止行之间的内容（包含起始行和终止行）
    """

    def __init__(self, parent=None):
        """
        初始化删除指定行控件

        Args:
            parent: 父控件
        """
        super().__init__("删除指定行", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加起始行和终止行的 SpinBox 控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：起始行
        start_label = BodyLabel("起始行:")
        start_label.setMinimumWidth(70)
        start_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.start_spin = SpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(999999)
        self.start_spin.setValue(1)
        self.start_spin.valueChanged.connect(self._emit_parameters_changed)
        self.start_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(start_label, 0, 0)
        grid_layout.addWidget(self.start_spin, 0, 1)

        # 第2行：终止行
        end_label = BodyLabel("终止行:")
        end_label.setMinimumWidth(70)
        end_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.end_spin = SpinBox()
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(999999)
        self.end_spin.setValue(1)
        self.end_spin.valueChanged.connect(self._emit_parameters_changed)
        self.end_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(end_label, 1, 0)
        grid_layout.addWidget(self.end_spin, 1, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def get_start_line(self):
        """
        获取起始行

        Returns:
            int: 起始行号（从1开始）
        """
        return self.start_spin.value()

    def get_end_line(self):
        """
        获取终止行

        Returns:
            int: 终止行号（从1开始）
        """
        return self.end_spin.value()

    def set_start_line(self, line):
        """
        设置起始行

        Args:
            line: 起始行号（从1开始）
        """
        self.start_spin.setValue(max(1, line))

    def set_end_line(self, line):
        """
        设置终止行

        Args:
            line: 终止行号（从1开始）
        """
        self.end_spin.setValue(max(1, line))

    def execute(self, text):
        """
        执行删除指定行操作

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        if not text:
            return text

        # 按行分割文本（保留换行符信息）
        lines = text.splitlines(keepends=True)
        if not lines:
            return text

        # 获取起始行和终止行（转换为从0开始的索引）
        start_line = self.get_start_line()
        end_line = self.get_end_line()

        # 确保起始行不大于终止行
        if start_line > end_line:
            start_line, end_line = end_line, start_line

        # 转换为0-based索引
        start_idx = start_line - 1
        end_idx = end_line - 1

        # 确保索引在有效范围内
        start_idx = max(0, start_idx)
        end_idx = min(len(lines) - 1, end_idx)

        # 保留不在删除范围内的行
        result_lines = []
        for i, line in enumerate(lines):
            if i < start_idx or i > end_idx:
                result_lines.append(line)

        # 重新合并文本
        return "".join(result_lines)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.start_spin.setValue(1)
        self.end_spin.setValue(1)

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "delete_lines",
            "start_line": self.get_start_line(),
            "end_line": self.get_end_line()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "delete_lines":
            self.set_start_line(config.get("start_line", 1))
            self.set_end_line(config.get("end_line", 1))

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "delete_lines"
