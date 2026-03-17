# -*- coding: utf-8 -*-
"""
移除空行控件模块
提供移除文本中空行的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QCheckBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class RemoveEmptyLinesControl(BaseControl):
    """
    移除空行控件类
    提供移除文本中空行的功能
    """
    
    def __init__(self, parent=None):
        """
        初始化移除空行控件
        
        Args:
            parent: 父控件
        """
        super().__init__("移除空行", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加移除空行相关的控件
        """
        layout = self.get_content_layout()
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第 1 行：仅空白字符行
        blank_label = QLabel("仅空白字符行:")
        blank_label.setMinimumWidth(70)
        blank_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.blank_check = QCheckBox()
        self.blank_check.setChecked(False)
        self.blank_check.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(blank_label, 0, 0)
        grid_layout.addWidget(self.blank_check, 0, 1)
        
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
    
    def is_only_blank(self):
        """
        获取是否仅移除仅包含空白字符的行
        
        Returns:
            bool: 是否仅移除仅包含空白字符的行
        """
        return self.blank_check.isChecked()
    
    def execute(self, text):
        """
        执行移除空行操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return text
        
        lines = text.split('\n')
        result = []
        
        only_blank = self.is_only_blank()
        
        for line in lines:
            if only_blank:
                # 仅移除仅包含空白字符的行
                if line.strip():
                    result.append(line)
            else:
                # 移除所有空行（包括仅包含空白字符的行）
                if line:
                    result.append(line)
        
        return '\n'.join(result)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.blank_check.setChecked(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "remove_empty_lines",
            "only_blank": self.is_only_blank()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "remove_empty_lines":
            self.blank_check.setChecked(config.get("only_blank", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "remove_empty_lines"
