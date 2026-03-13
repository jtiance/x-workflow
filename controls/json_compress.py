# -*- coding: utf-8 -*-
"""
JSON压缩控件模块
提供JSON压缩功能的可视化控件
"""

import json
from PySide6.QtWidgets import QGridLayout, QLabel, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class JsonCompressControl(BaseControl):
    """
    JSON压缩控件
    用于将JSON文本压缩成一行
    """
    
    def __init__(self, parent=None):
        """
        初始化JSON压缩控件
        
        Args:
            parent: 父控件
        """
        super().__init__("JSON压缩", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加JSON压缩相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：按键名排序
        self.sort_checkbox = QCheckBox("按键名排序")
        self.sort_checkbox.setChecked(False)
        self.sort_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.sort_checkbox, 0, 0, 1, 2)  # 跨两列
        
        # 第2行：确保ASCII
        self.ascii_checkbox = QCheckBox("确保ASCII（转义非ASCII字符）")
        self.ascii_checkbox.setChecked(False)
        self.ascii_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.ascii_checkbox, 1, 0, 1, 2)  # 跨两列
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
        
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
        执行JSON压缩操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        # 解析JSON（如果出错会抛出异常，由调用者处理）
        data = json.loads(text)
        
        # 获取设置
        sort_keys = self.get_sort_keys()
        ensure_ascii = self.get_ensure_ascii()
        
        # 压缩成一行（indent=None）
        compressed = json.dumps(
            data,
            indent=None,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii
        )
        
        return compressed
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_sort_keys(False)
        self.set_ensure_ascii(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "json_compress",
            "sort_keys": self.get_sort_keys(),
            "ensure_ascii": self.get_ensure_ascii()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "json_compress":
            self.set_sort_keys(config.get("sort_keys", False))
            self.set_ensure_ascii(config.get("ensure_ascii", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "json_compress"
