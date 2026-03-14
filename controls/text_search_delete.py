# -*- coding: utf-8 -*-
"""
文本查询删除控件模块
基于特定文本查询每行，找到匹配行后进行删除操作
"""

from PySide6.QtWidgets import (QGridLayout, QLabel, QLineEdit, QComboBox, 
                              QCheckBox, QSizePolicy)
from PySide6.QtCore import Qt

from controls.base_control import BaseControl


class TextSearchDeleteControl(BaseControl):
    """
    文本查询删除控件类
    查找包含特定文本的行并删除
    """
    
    def __init__(self, parent=None):
        """
        初始化文本查询删除控件
        
        Args:
            parent: 父控件
        """
        super().__init__("文本搜索删除", parent)
        
    def _init_content(self):
        """
        初始化内容区域
        添加文本搜索删除相关的控件
        """
        layout = self.get_content_layout()
        
        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 第1行：查询文本
        search_label = QLabel("查询文本:")
        search_label.setMinimumWidth(70)
        search_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入要查询的文本...")
        self.search_input.textChanged.connect(self._emit_parameters_changed)
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(search_label, 0, 0)
        grid_layout.addWidget(self.search_input, 0, 1)
        
        # 第2行：匹配模式
        match_label = QLabel("匹配模式:")
        match_label.setMinimumWidth(70)
        match_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.match_combo = QComboBox()
        self.match_combo.addItems(["包含文本", "不包含文本"])
        self.match_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.match_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(match_label, 1, 0)
        grid_layout.addWidget(self.match_combo, 1, 1)
        
        # 第3行：删除模式
        delete_label = QLabel("删除模式:")
        delete_label.setMinimumWidth(70)
        delete_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.delete_combo = QComboBox()
        self.delete_combo.addItems(["删除匹配行", "删除非匹配行"])
        self.delete_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.delete_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        grid_layout.addWidget(delete_label, 2, 0)
        grid_layout.addWidget(self.delete_combo, 2, 1)
        
        # 第4行：区分大小写
        self.case_checkbox = QCheckBox("区分大小写")
        self.case_checkbox.setChecked(False)
        self.case_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.case_checkbox, 3, 0, 1, 2)  # 跨两列
        
        # 第5行：使用正则表达式
        self.regex_checkbox = QCheckBox("使用正则表达式")
        self.regex_checkbox.setChecked(False)
        self.regex_checkbox.stateChanged.connect(self._emit_parameters_changed)
        
        grid_layout.addWidget(self.regex_checkbox, 4, 0, 1, 2)  # 跨两列
        
        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)
        
        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)
    
    def get_search_text(self):
        """
        获取搜索文本
        
        Returns:
            str: 搜索文本
        """
        return self.search_input.text()
    
    def set_search_text(self, text):
        """
        设置搜索文本
        
        Args:
            text: 搜索文本
        """
        self.search_input.setText(text)
    
    def _line_matches(self, line):
        """
        检查单行是否匹配条件
        
        Args:
            line: 要检查的行文本
            
        Returns:
            bool: 是否匹配
        """
        search_text = self.get_search_text()
        if not search_text:
            return False
        
        # 准备比较文本
        compare_line = line if self.case_checkbox.isChecked() else line.lower()
        compare_search = search_text if self.case_checkbox.isChecked() else search_text.lower()
        
        if self.regex_checkbox.isChecked():
            import re
            try:
                flags = 0 if self.case_checkbox.isChecked() else re.IGNORECASE
                pattern = re.compile(search_text, flags)
                matches = bool(pattern.search(line))
            except re.error:
                # 正则表达式错误，回退到普通文本匹配
                matches = compare_search in compare_line
        else:
            matches = compare_search in compare_line
        
        # 根据匹配模式返回结果
        match_mode = self.match_combo.currentText()
        if match_mode == "包含文本":
            return matches
        else:
            return not matches
    
    def execute(self, text):
        """
        执行文本搜索删除操作
        
        Args:
            text: 要处理的文本
            
        Returns:
            str: 处理后的文本
        """
        if not text:
            return text
        
        # 按行分割文本
        lines = text.splitlines()
        if not lines:
            return text
        
        # 处理每一行
        result_lines = []
        delete_mode = self.delete_combo.currentText()
        
        for line in lines:
            line_matches = self._line_matches(line)
            
            # 根据删除模式决定是否保留该行
            should_keep = False
            if delete_mode == "删除匹配行":
                should_keep = not line_matches
            else:
                should_keep = line_matches
            
            if should_keep:
                result_lines.append(line)
        
        # 重新合并文本
        return "\n".join(result_lines)
        
    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.search_input.setText("")
        self.match_combo.setCurrentText("包含文本")
        self.delete_combo.setCurrentText("删除匹配行")
        self.case_checkbox.setChecked(False)
        self.regex_checkbox.setChecked(False)
        
    def get_config(self):
        """
        获取控件配置
        
        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "text_search_delete",
            "search_text": self.get_search_text(),
            "match_mode": "contains" if self.match_combo.currentText() == "包含文本" else "not_contains",
            "delete_mode": "delete_matched" if self.delete_combo.currentText() == "删除匹配行" else "delete_unmatched",
            "case_sensitive": self.case_checkbox.isChecked(),
            "use_regex": self.regex_checkbox.isChecked()
        }
        
    def load_config(self, config):
        """
        加载控件配置
        
        Args:
            config: 控件配置字典
        """
        if config.get("type") == "text_search_delete":
            self.set_search_text(config.get("search_text", ""))
            match_mode = config.get("match_mode", "contains")
            self.match_combo.setCurrentText("包含文本" if match_mode == "contains" else "不包含文本")
            delete_mode = config.get("delete_mode", "delete_matched")
            self.delete_combo.setCurrentText("删除匹配行" if delete_mode == "delete_matched" else "删除非匹配行")
            self.case_checkbox.setChecked(config.get("case_sensitive", False))
            self.regex_checkbox.setChecked(config.get("use_regex", False))
            
    def get_control_type(self):
        """
        获取控件类型
        
        Returns:
            str: 控件类型标识
        """
        return "text_search_delete"
