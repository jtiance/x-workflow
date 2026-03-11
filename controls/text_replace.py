# -*- coding: utf-8 -*-
"""
文本替换控件模块
提供文本替换功能的可视化控件
"""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class TextReplaceControl(BaseControl):
    """
    文本替换控件
    用于在文本中查找并替换指定内容
    """
    
    def __init__(self, parent=None):
        """
        初始化文本替换控件
        
        Args:
            parent: 父控件
        """
        super().__init__("文本替换", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加文本替换相关的控件
        """
        layout = self.get_content_layout()
        
        # 1. 查找文本行
        find_layout = QHBoxLayout()
        find_label = QLabel("查找:")
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("输入要查找的文本...")
        self.find_input.textChanged.connect(self._emit_parameters_changed)
        
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        
        # 2. 替换文本行
        replace_layout = QHBoxLayout()
        replace_label = QLabel("替换:")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("输入替换后的文本...")
        self.replace_input.textChanged.connect(self._emit_parameters_changed)
        
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)
        
        # 将所有组件添加到内容布局
        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        
    def get_find_text(self):
        """
        获取当前输入的查找文本
        
        Returns:
            str: 查找文本
        """
        return self.find_input.text()
        
    def get_replace_text(self):
        """
        获取当前输入的替换文本
        
        Returns:
            str: 替换文本
        """
        return self.replace_input.text()
        
    def set_find_text(self, text):
        """
        设置查找文本
        
        Args:
            text: 要设置的查找文本
        """
        self.find_input.setText(text)
        
    def set_replace_text(self, text):
        """
        设置替换文本
        
        Args:
            text: 要设置的替换文本
        """
        self.replace_input.setText(text)
        
    def execute(self, text):
        """
        执行文本替换操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        find_text = self.get_find_text()
        replace_text = self.get_replace_text()
        
        if find_text:
            return text.replace(find_text, replace_text)
        
        return text
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_find_text("")
        self.set_replace_text("")
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_replace",
            "find_text": self.get_find_text(),
            "replace_text": self.get_replace_text()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_replace":
            self.set_find_text(config.get("find_text", ""))
            self.set_replace_text(config.get("replace_text", ""))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_replace"