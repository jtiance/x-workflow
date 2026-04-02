# -*- coding: utf-8 -*-
"""
移除重复行控件模块
提供移除文本中重复行的功能
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QSizePolicy)
from qfluentwidgets import ComboBox, BodyLabel

from components.custom_buttons import CheckablePushButton
from controls.base_control import BaseControl


class RemoveDuplicateControl(BaseControl):
    """
    移除重复行控件类
    提供按不同方式移除重复行的功能
    """
    
    def __init__(self, parent=None):
        """
        初始化移除重复行控件
        
        Args:
            parent: 父控件
        """
        super().__init__("移除重复行", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加移除重复行相关的控件
        """
        layout = self.get_content_layout()
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        mode_label = BodyLabel("模式:")
        mode_label.setMinimumWidth(70)
        mode_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.mode_combo = ComboBox()
        self.mode_combo.addItems(["保留首次出现", "保留最后一次出现"])
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        # 第2行：按钮组
        from PySide6.QtWidgets import QHBoxLayout
        
        # 创建水平布局容纳2个按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        # 忽略大小写按钮
        self.ignore_case_check = CheckablePushButton("Aa")
        self.ignore_case_check.setChecked(False)
        self.ignore_case_check.setToolTip("忽略大小写")
        self.ignore_case_check.clicked.connect(self._emit_parameters_changed)
        self.ignore_case_check.setFixedWidth(40)
        
        # 忽略空行按钮
        self.ignore_blank_check = CheckablePushButton("忽略空行")
        self.ignore_blank_check.setChecked(False)
        self.ignore_blank_check.setToolTip("空行不会被移除重复行")
        self.ignore_blank_check.clicked.connect(self._emit_parameters_changed)
        self.ignore_blank_check.setFixedWidth(60)
        
        # 添加按钮到水平布局
        button_layout.addWidget(self.ignore_case_check)
        button_layout.addWidget(self.ignore_blank_check)
        button_layout.addStretch()  # 右侧添加弹性空间
        
        # 将水平布局添加到网格布局
        grid_layout.addLayout(button_layout, 1, 1)  # 放在第二列
        
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
    
    def get_mode(self):
        """
        获取当前模式
        
        Returns:
            str: 'first' 或 'last'
        """
        if self.mode_combo.currentText() == "保留首次出现":
            return "first"
        else:
            return "last"
    
    def is_ignore_case(self):
        """
        获取是否忽略大小写
        
        Returns:
            bool: 是否忽略大小写
        """
        return self.ignore_case_check.isChecked()
    
    def is_ignore_blank(self):
        """
        获取是否忽略空行
        
        Returns:
            bool: 是否忽略空行
        """
        return self.ignore_blank_check.isChecked()
    
    def execute(self, text):
        """
        执行移除重复行操作

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        if not text:
            return text

        lines = text.split('\n')

        ignore_case = self.is_ignore_case()
        ignore_blank = self.is_ignore_blank()
        mode = self.get_mode()

        if mode == "first":
            # 使用集合而不是列表，提高查找性能 O(1) vs O(n)
            seen = set()
            result = []
            for line in lines:
                if ignore_blank and not line.strip():
                    result.append(line)
                    continue

                check_line = line if not ignore_case else line.lower()

                if check_line not in seen:
                    seen.add(check_line)
                    result.append(line)

            return '\n'.join(result)

        else:
            # 保留最后一次出现 - 使用字典
            seen_last = {}
            for line in lines:
                if ignore_blank and not line.strip():
                    continue

                check_line = line if not ignore_case else line.lower()
                seen_last[check_line] = line

            return '\n'.join(seen_last.values())
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentText("保留首次出现")
        self.ignore_case_check.setChecked(False)
        self.ignore_blank_check.setChecked(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "remove_duplicate",
            "mode": self.get_mode(),
            "ignore_case": self.is_ignore_case(),
            "ignore_blank": self.is_ignore_blank()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "remove_duplicate":
            mode = config.get("mode", "first")
            if mode == "first":
                self.mode_combo.setCurrentText("保留首次出现")
            else:
                self.mode_combo.setCurrentText("保留最后一次出现")
            self.ignore_case_check.setChecked(config.get("ignore_case", False))
            self.ignore_blank_check.setChecked(config.get("ignore_blank", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "remove_duplicate"
