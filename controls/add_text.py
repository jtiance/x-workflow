# -*- coding: utf-8 -*-
"""
增加文本控件模块
提供为文本每一行增加前缀、后缀或前后缀的功能
"""

from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QComboBox, QSizePolicy
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class AddTextControl(BaseControl):
    """
    增加文本控件
    用于为文本的每一行增加前缀、后缀或前后缀
    """
    
    def __init__(self, parent=None):
        """
        初始化增加文本控件
        
        Args:
            parent: 父控件
        """
        super().__init__("增加文本", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加操作类型选择和文本输入相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：操作类型
        type_label = QLabel("操作类型:")
        type_label.setMinimumWidth(70)
        type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["增加前缀", "增加后缀", "增加前后缀"])
        self.type_combo.currentIndexChanged.connect(self._emit_parameters_changed)
        self.type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(type_label, 0, 0)
        grid_layout.addWidget(self.type_combo, 0, 1)
        
        # 第2行：文本
        text_label = QLabel("文本:")
        text_label.setMinimumWidth(70)
        text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("输入要添加的文本...")
        self.text_input.textChanged.connect(self._emit_parameters_changed)
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(text_label, 1, 0)
        grid_layout.addWidget(self.text_input, 1, 1)
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
        
    def get_operation_type(self):
        """
        获取当前选择的操作类型
        
        Returns:
            str: 操作类型，可能的值为 "增加前缀", "增加后缀", "增加前后缀"
        """
        return self.type_combo.currentText()
        
    def set_operation_type(self, type_text):
        """
        设置操作类型
        
        Args:
            type_text: 操作类型文本
        """
        index = self.type_combo.findText(type_text)
        if index != -1:
            self.type_combo.setCurrentIndex(index)
        
    def get_text(self):
        """
        获取当前输入的文本
        
        Returns:
            str: 文本内容
        """
        return self.text_input.text()
        
    def set_text(self, text):
        """
        设置文本内容
        
        Args:
            text: 要设置的文本
        """
        self.text_input.setText(text)
        
    def execute(self, text):
        """
        执行增加文本的操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        operation_type = self.get_operation_type()
        add_text = self.get_text()
        
        if not add_text:
            return text
        
        # 按行分割文本
        lines = text.split('\n')
        result_lines = []
        
        # 根据操作类型处理每一行
        for line in lines:
            if operation_type == "增加前缀":
                result_lines.append(add_text + line)
            elif operation_type == "增加后缀":
                result_lines.append(line + add_text)
            elif operation_type == "增加前后缀":
                result_lines.append(add_text + line + add_text)
        
        # 重新组合成文本
        return '\n'.join(result_lines)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_operation_type("增加前缀")
        self.set_text("")
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "add_text",
            "operation_type": self.get_operation_type(),
            "text": self.get_text()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "add_text":
            self.set_operation_type(config.get("operation_type", "增加前缀"))
            self.set_text(config.get("text", ""))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "add_text"
