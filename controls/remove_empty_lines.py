# -*- coding: utf-8 -*-
"""
移除空行控件模块
提供移除文本中空行的功能
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QComboBox, QSizePolicy)
from components.custom_buttons import CheckablePushButton
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
        
        # 第 1 行：移除模式
        mode_label = QLabel("移除模式:")
        mode_label.setMinimumWidth(70)
        mode_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.mode_combo = QComboBox()
        self.mode_combo.setEditable(True)
        self.mode_combo.lineEdit().setReadOnly(True)
        self.mode_combo.addItems(["移除所有空行", "仅移除空白字符行", "仅移除完全空行"])
        self.mode_combo.setCurrentText("移除所有空行")
        self.mode_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)
        
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
    
    def get_remove_mode(self):
        """
        获取移除模式
        
        Returns:
            str: 移除模式 ('all', 'only_blank', 'only_empty')
        """
        mode_text = self.mode_combo.currentText()
        if mode_text == "仅移除空白字符行":
            return "only_blank"
        elif mode_text == "仅移除完全空行":
            return "only_empty"
        else:
            return "all"
    
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
        
        mode = self.get_remove_mode()
        
        for line in lines:
            if mode == "only_blank":
                # 仅移除仅包含空白字符的行，保留完全空的行
                if not line or line.strip():
                    result.append(line)
            elif mode == "only_empty":
                # 仅移除完全空行（不包含任何字符的行）
                if line:
                    result.append(line)
            else:
                # 移除所有空行（包括仅包含空白字符的行）
                if line.strip():
                    result.append(line)
        
        return '\n'.join(result)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.mode_combo.setCurrentText("移除所有空行")
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "remove_empty_lines",
            "remove_mode": self.get_remove_mode()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "remove_empty_lines":
            remove_mode = config.get("remove_mode", "all")
            if remove_mode == "only_blank":
                self.mode_combo.setCurrentText("仅移除空白字符行")
            elif remove_mode == "only_empty":
                self.mode_combo.setCurrentText("仅移除完全空行")
            else:
                self.mode_combo.setCurrentText("移除所有空行")
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "remove_empty_lines"
