# -*- coding: utf-8 -*-
"""
文本替换控件模块
提供文本替换功能的可视化控件
"""

import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy, QHBoxLayout
from qfluentwidgets import LineEdit, TogglePushButton, BodyLabel

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
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：查找
        find_label = BodyLabel("查找:")
        find_label.setMinimumWidth(70)
        find_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.find_input = LineEdit()
        self.find_input.setPlaceholderText("输入要查找的文本...")
        self.find_input.textChanged.connect(self._emit_parameters_changed)
        self.find_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(find_label, 0, 0)
        grid_layout.addWidget(self.find_input, 0, 1)
        
        # 第2行：查找选项（按钮组）
        
        # 创建水平布局容纳3个查找选项按钮
        find_options_layout = QHBoxLayout()
        find_options_layout.setSpacing(5)
        
        # 忽略大小写按钮
        self.case_checkbox = TogglePushButton("Aa")
        self.case_checkbox.setChecked(False)
        self.case_checkbox.setToolTip("忽略大小写")
        self.case_checkbox.clicked.connect(self._emit_parameters_changed)
        self.case_checkbox.setFixedWidth(45)
        
        # 使用正则表达式按钮
        self.regex_checkbox = TogglePushButton("RE")
        self.regex_checkbox.setChecked(False)
        self.regex_checkbox.setToolTip("使用正则表达式")
        self.regex_checkbox.clicked.connect(self._emit_parameters_changed)
        self.regex_checkbox.setFixedWidth(45)
        
        # 查找转义字符按钮
        self.find_escape_checkbox = TogglePushButton("/r/n")
        self.find_escape_checkbox.setChecked(False)
        self.find_escape_checkbox.setToolTip("查找转义字符")
        self.find_escape_checkbox.clicked.connect(self._emit_parameters_changed)
        self.regex_checkbox.setFixedWidth(60)
        
        # 设置按钮固定宽度
        button_width = 50
        self.case_checkbox.setFixedWidth(button_width)
        self.regex_checkbox.setFixedWidth(button_width)
        self.find_escape_checkbox.setFixedWidth(button_width)
        
        # 添加按钮到水平布局
        find_options_layout.addWidget(self.case_checkbox)
        find_options_layout.addWidget(self.regex_checkbox)
        find_options_layout.addWidget(self.find_escape_checkbox)
        find_options_layout.addStretch()  # 右侧添加弹性空间
        
        # 将水平布局添加到网格布局
        grid_layout.addLayout(find_options_layout, 1, 1)
        
        # 第3行：替换
        replace_label = BodyLabel("替换:")
        replace_label.setMinimumWidth(70)
        replace_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.replace_input = LineEdit()
        self.replace_input.setPlaceholderText("输入替换后的文本...")
        self.replace_input.textChanged.connect(self._emit_parameters_changed)
        self.replace_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(replace_label, 2, 0)
        grid_layout.addWidget(self.replace_input, 2, 1)
        
        # 第4行：替换选项
        self.escape_checkbox = TogglePushButton("/r/n")
        self.escape_checkbox.setChecked(False)
        self.escape_checkbox.setToolTip("替换转义字符")
        self.escape_checkbox.setFixedWidth(50)
        self.escape_checkbox.clicked.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.escape_checkbox, 3, 1)
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 设置控件的最小高度，确保所有内容可见
        self.setMinimumHeight(200)
        
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
    
    def is_escape_chars(self):
        """
        是否转义字符
        
        Returns:
            bool: 是否转义字符
        """
        return self.escape_checkbox.isChecked()
    
    def is_find_escape_chars(self):
        """
        是否在查找时转义字符
        
        Returns:
            bool: 是否在查找时转义字符
        """
        return self.find_escape_checkbox.isChecked()
    
    def set_escape_chars(self, escape):
        """
        设置是否转义字符
        
        Args:
            escape: 是否转义字符
        """
        self.escape_checkbox.setChecked(escape)
    
    def set_find_escape_chars(self, escape):
        """
        设置是否在查找时转义字符
        
        Args:
            escape: 是否在查找时转义字符
        """
        self.find_escape_checkbox.setChecked(escape)
        
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
    
    def _convert_escape_chars(self, text):
        """
        将转义字符转换为实际字符
        
        Args:
            text: 包含转义字符的文本
            
        Returns:
            str: 转换后的文本
        """
        if not text:
            return text
        
        escape_map = {
            '\\n': '\n',
            '\\t': '\t',
            '\\r': '\r',
            '\\\\': '\\',
            '\\0': '\0',
        }
        
        result = text
        for escape, char in escape_map.items():
            result = result.replace(escape, char)
        
        return result
        
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
        
        # 如果启用查找转义字符，则转换查找文本
        if self.is_find_escape_chars():
            find_text = self._convert_escape_chars(find_text)
        
        # 如果启用转义字符，则转换替换文本
        if self.is_escape_chars():
            replace_text = self._convert_escape_chars(replace_text)
        
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
        self.set_escape_chars(False)
        self.set_find_escape_chars(False)
        
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
            "ignore_case": self.is_ignore_case(),
            "escape_chars": self.is_escape_chars(),
            "find_escape_chars": self.is_find_escape_chars()
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
            self.set_escape_chars(config.get("escape_chars", False))
            self.set_find_escape_chars(config.get("find_escape_chars", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_replace"
