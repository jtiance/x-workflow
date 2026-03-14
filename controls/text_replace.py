# -*- coding: utf-8 -*-
"""
文本替换控件模块
提供文本替换功能的可视化控件
"""

import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QSizePolicy

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
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：查找
        find_label = QLabel("查找:")
        find_label.setMinimumWidth(70)
        find_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("输入要查找的文本...")
        self.find_input.textChanged.connect(self._emit_parameters_changed)
        self.find_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(find_label, 0, 0)
        grid_layout.addWidget(self.find_input, 0, 1)
        
        # 第2行：替换
        replace_label = QLabel("替换:")
        replace_label.setMinimumWidth(70)
        replace_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("输入替换后的文本...")
        self.replace_input.textChanged.connect(self._emit_parameters_changed)
        self.replace_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(replace_label, 1, 0)
        grid_layout.addWidget(self.replace_input, 1, 1)
        
        # 第3行：查找选项（复选框）
        self.case_checkbox = QCheckBox("忽略大小写")
        self.case_checkbox.setChecked(False)
        self.case_checkbox.stateChanged.connect(self._emit_parameters_changed)

        self.regex_checkbox = QCheckBox("使用正则表达式")
        self.regex_checkbox.setChecked(False)
        self.regex_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.case_checkbox, 2, 0)
        grid_layout.addWidget(self.regex_checkbox, 2, 1)
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
        
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
    
    def is_use_regex(self):
        """
        是否使用正则表达式
        
        Returns:
            bool: 是否使用正则表达式
        """
        return self.regex_checkbox.isChecked()
    
    def is_ignore_case(self):
        """
        是否忽略大小写
        
        Returns:
            bool: 是否忽略大小写
        """
        return self.case_checkbox.isChecked()
        
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
    
    def set_use_regex(self, use_regex):
        """
        设置是否使用正则表达式
        
        Args:
            use_regex: 是否使用正则表达式
        """
        self.regex_checkbox.setChecked(use_regex)
    
    def set_ignore_case(self, ignore_case):
        """
        设置是否忽略大小写
        
        Args:
            ignore_case: 是否忽略大小写
        """
        self.case_checkbox.setChecked(ignore_case)
        
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
        
        if not find_text:
            return text
        
        if self.is_use_regex():
            # 使用正则表达式替换
            flags = 0
            if self.is_ignore_case():
                flags |= re.IGNORECASE
            
            try:
                # 定义一个替换函数，跳过空匹配
                def replace_func(match):
                    if match.group(0):  # 只替换非空匹配
                        return replace_text
                    return match.group(0)  # 空匹配保持不变
                
                return re.sub(find_text, replace_func, text, flags=flags)
            except re.error:
                # 正则表达式错误，回退到普通替换
                if self.is_ignore_case():
                    # 忽略大小写的普通替换
                    result = []
                    pos = 0
                    lower_text = text.lower()
                    lower_find = find_text.lower()
                    while pos < len(text):
                        found_pos = lower_text.find(lower_find, pos)
                        if found_pos == -1:
                            result.append(text[pos:])
                            break
                        result.append(text[pos:found_pos])
                        result.append(replace_text)
                        pos = found_pos + len(find_text)
                    return "".join(result)
                else:
                    return text.replace(find_text, replace_text)
        else:
            # 普通文本替换
            if self.is_ignore_case():
                # 忽略大小写的普通替换
                result = []
                pos = 0
                lower_text = text.lower()
                lower_find = find_text.lower()
                while pos < len(text):
                    found_pos = lower_text.find(lower_find, pos)
                    if found_pos == -1:
                        result.append(text[pos:])
                        break
                    result.append(text[pos:found_pos])
                    result.append(replace_text)
                    pos = found_pos + len(find_text)
                return "".join(result)
            else:
                return text.replace(find_text, replace_text)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_find_text("")
        self.set_replace_text("")
        self.set_use_regex(False)
        self.set_ignore_case(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_replace",
            "find_text": self.get_find_text(),
            "replace_text": self.get_replace_text(),
            "use_regex": self.is_use_regex(),
            "ignore_case": self.is_ignore_case()
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
            self.set_use_regex(config.get("use_regex", False))
            self.set_ignore_case(config.get("ignore_case", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_replace"
