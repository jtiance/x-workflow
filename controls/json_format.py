# -*- coding: utf-8 -*-
"""
JSON格式化控件模块
提供JSON格式化功能的可视化控件
"""

import json
from PySide6.QtWidgets import QHBoxLayout, QLabel, QCheckBox, QSpinBox, QSizePolicy
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class JsonFormatControl(BaseControl):
    """
    JSON格式化控件
    用于格式化JSON文本
    """
    
    def __init__(self, parent=None):
        """
        初始化JSON格式化控件
        
        Args:
            parent: 父控件
        """
        super().__init__("JSON格式化", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加JSON格式化相关的控件
        """
        layout = self.get_content_layout()
        
        # 1. 缩进设置
        indent_layout = QHBoxLayout()
        indent_label = QLabel("缩进:")
        self.indent_spin = QSpinBox()
        self.indent_spin.setMinimum(0)
        self.indent_spin.setMaximum(8)
        self.indent_spin.setValue(4)
        self.indent_spin.setSuffix(" 空格")
        self.indent_spin.setMinimumWidth(150)  # 最小宽度，更宽一点
        self.indent_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 水平方向扩展
        self.indent_spin.valueChanged.connect(self._emit_parameters_changed)
        
        indent_layout.addWidget(indent_label)
        indent_layout.addWidget(self.indent_spin)
        indent_layout.addStretch()
        
        # 2. 排序键
        sort_layout = QHBoxLayout()
        self.sort_checkbox = QCheckBox("按键名排序")
        self.sort_checkbox.setChecked(False)
        self.sort_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        sort_layout.addWidget(self.sort_checkbox)
        sort_layout.addStretch()
        
        # 3. 确保ASCII
        ascii_layout = QHBoxLayout()
        self.ascii_checkbox = QCheckBox("确保ASCII（转义非ASCII字符）")
        self.ascii_checkbox.setChecked(False)
        self.ascii_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        ascii_layout.addWidget(self.ascii_checkbox)
        ascii_layout.addStretch()
        
        # 将所有组件添加到内容布局
        layout.addLayout(indent_layout)
        layout.addLayout(sort_layout)
        layout.addLayout(ascii_layout)
        
    def get_indent(self):
        """
        获取缩进设置
        
        Returns:
            int: 缩进空格数，0表示不缩进
        """
        return self.indent_spin.value()
        
    def get_sort_keys(self):
        """
        获取是否排序键
        
        Returns:
            bool: 是否按键名排序
        """
        return self.sort_checkbox.isChecked()
        
    def get_ensure_ascii(self):
        """
        获取是否确保ASCII
        
        Returns:
            bool: 是否转义非ASCII字符
        """
        return self.ascii_checkbox.isChecked()
        
    def set_indent(self, indent):
        """
        设置缩进
        
        Args:
            indent: 缩进空格数
        """
        self.indent_spin.setValue(indent)
        
    def set_sort_keys(self, sort):
        """
        设置是否排序键
        
        Args:
            sort: 是否按键名排序
        """
        self.sort_checkbox.setChecked(sort)
        
    def set_ensure_ascii(self, ensure_ascii):
        """
        设置是否确保ASCII
        
        Args:
            ensure_ascii: 是否转义非ASCII字符
        """
        self.ascii_checkbox.setChecked(ensure_ascii)
        
    def execute(self, text):
        """
        执行JSON格式化操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        # 解析JSON（如果出错会抛出异常，由调用者处理）
        data = json.loads(text)
        
        # 获取设置
        indent = self.get_indent()
        sort_keys = self.get_sort_keys()
        ensure_ascii = self.get_ensure_ascii()
        
        # 格式化
        formatted = json.dumps(
            data,
            indent=indent if indent > 0 else None,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii
        )
        
        return formatted
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_indent(4)
        self.set_sort_keys(False)
        self.set_ensure_ascii(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "json_format",
            "indent": self.get_indent(),
            "sort_keys": self.get_sort_keys(),
            "ensure_ascii": self.get_ensure_ascii()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "json_format":
            self.set_indent(config.get("indent", 4))
            self.set_sort_keys(config.get("sort_keys", False))
            self.set_ensure_ascii(config.get("ensure_ascii", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "json_format"