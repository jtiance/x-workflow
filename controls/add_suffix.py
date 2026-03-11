# -*- coding: utf-8 -*-
"""
增加后缀控件模块
提供为文本每一行增加后缀的功能
"""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class AddSuffixControl(BaseControl):
    """
    增加后缀控件
    用于为文本的每一行后边增加指定的文本
    """
    
    def __init__(self, parent=None):
        """
        初始化增加后缀控件
        
        Args:
            parent: 父控件
        """
        super().__init__("增加后缀", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加后缀输入相关的控件
        """
        layout = self.get_content_layout()
        
        # 后缀输入行
        suffix_layout = QHBoxLayout()
        suffix_label = QLabel("后缀:")
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("输入要添加的后缀...")
        self.suffix_input.textChanged.connect(self._emit_parameters_changed)
        
        suffix_layout.addWidget(suffix_label)
        suffix_layout.addWidget(self.suffix_input)
        
        # 将组件添加到内容布局
        layout.addLayout(suffix_layout)
        
    def get_suffix(self):
        """
        获取当前输入的后缀文本
        
        Returns:
            str: 后缀文本
        """
        return self.suffix_input.text()
        
    def set_suffix(self, text):
        """
        设置后缀文本
        
        Args:
            text: 要设置的后缀文本
        """
        self.suffix_input.setText(text)
        
    def execute(self, text):
        """
        执行为每一行增加后缀的操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        suffix = self.get_suffix()
        
        if not suffix:
            return text
        
        # 按行分割文本
        lines = text.split('\n')
        
        # 为每一行添加后缀
        result_lines = [line + suffix for line in lines]
        
        # 重新组合成文本
        return '\n'.join(result_lines)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_suffix("")
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "add_suffix",
            "suffix": self.get_suffix()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "add_suffix":
            self.set_suffix(config.get("suffix", ""))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "add_suffix"
