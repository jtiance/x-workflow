# -*- coding: utf-8 -*-
"""
增加前缀控件模块
提供为文本每一行增加前缀的功能
"""

from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class AddPrefixControl(BaseControl):
    """
    增加前缀控件
    用于为文本的每一行前边增加指定的文本
    """
    
    def __init__(self, parent=None):
        """
        初始化增加前缀控件
        
        Args:
            parent: 父控件
        """
        super().__init__("增加前缀", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加前缀输入相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：前缀
        prefix_label = QLabel("前缀:")
        prefix_label.setMinimumWidth(70)
        
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("输入要添加的前缀...")
        self.prefix_input.textChanged.connect(self._emit_parameters_changed)
        self.prefix_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(prefix_label, 0, 0)
        grid_layout.addWidget(self.prefix_input, 0, 1)
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
        
    def get_prefix(self):
        """
        获取当前输入的前缀文本
        
        Returns:
            str: 前缀文本
        """
        return self.prefix_input.text()
        
    def set_prefix(self, text):
        """
        设置前缀文本
        
        Args:
            text: 要设置的前缀文本
        """
        self.prefix_input.setText(text)
        
    def execute(self, text):
        """
        执行为每一行增加前缀的操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        prefix = self.get_prefix()
        
        if not prefix:
            return text
        
        # 按行分割文本
        lines = text.split('\n')
        
        # 为每一行添加前缀
        result_lines = [prefix + line for line in lines]
        
        # 重新组合成文本
        return '\n'.join(result_lines)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_prefix("")
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "add_prefix",
            "prefix": self.get_prefix()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "add_prefix":
            self.set_prefix(config.get("prefix", ""))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "add_prefix"
