# -*- coding: utf-8 -*-
"""
HTML提取器控件模块
提供从HTML文档中提取可见文本功能的可视化控件
"""

import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout
from qfluentwidgets import BodyLabel, ComboBox

from controls.base_control import BaseControl


class HtmlExtractControl(BaseControl):
    """
    HTML提取器控件
    用于从HTML文档中提取可见文本内容
    """

    def __init__(self, parent=None):
        """
        初始化HTML提取器控件

        Args:
            parent: 父控件
        """
        super().__init__("HTML文本提取", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加HTML提取相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：模式选择
        mode_label = BodyLabel("模式:")
        mode_label.setMinimumWidth(70)
        mode_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.mode_combo = ComboBox()
        self.mode_combo.addItem("提取可见文本", userData="visible_text")
        self.mode_combo.addItem("提取链接", userData="links")
        self.mode_combo.currentIndexChanged.connect(self._emit_parameters_changed)

        grid_layout.addWidget(mode_label, 0, 0)
        grid_layout.addWidget(self.mode_combo, 0, 1)

        # 第2行：空白处理选项
        whitespace_label = BodyLabel("空白处理:")
        whitespace_label.setMinimumWidth(70)
        whitespace_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.whitespace_combo = ComboBox()
        self.whitespace_combo.addItem("移除空行", userData="remove_empty")
        self.whitespace_combo.addItem("压缩空白", userData="compress")
        self.whitespace_combo.currentIndexChanged.connect(self._emit_parameters_changed)

        grid_layout.addWidget(whitespace_label, 1, 0)
        grid_layout.addWidget(self.whitespace_combo, 1, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def get_mode(self):
        """
        获取提取模式

        Returns:
            str: 模式 ('visible_text' 或 'links')
        """
        return self.mode_combo.currentData()

    def set_mode(self, mode):
        """
        设置提取模式

        Args:
            mode: 模式 ('visible_text' 或 'links')
        """
        index = self.mode_combo.findData(mode)
        if index != -1:
            self.mode_combo.setCurrentIndex(index)

    def get_whitespace_mode(self):
        """
        获取空白处理模式

        Returns:
            str: 模式 ('compress' 或 'remove_empty')
        """
        return self.whitespace_combo.currentData()

    def set_whitespace_mode(self, mode):
        """
        设置空白处理模式

        Args:
            mode: 模式 ('compress' 或 'remove_empty')
        """
        index = self.whitespace_combo.findData(mode)
        if index != -1:
            self.whitespace_combo.setCurrentIndex(index)


    def execute(self, text):
        """
        执行HTML提取操作

        Args:
            text: 要处理的HTML文本

        Returns:
            str: 处理后的文本
        """
        if not text:
            return text

        mode = self.get_mode()

        if mode == "links":
            # 提取链接模式
            result = self._extract_links(text)
        else:
            # 提取可见文本模式
            result = self._extract_visible_text(text)

        return result

    def _extract_visible_text(self, html_text):
        """
        从HTML中提取可见文本

        Args:
            html_text: HTML文本

        Returns:
            str: 提取的可见文本
        """
        # 规范化换行符
        text = html_text.replace('\r\n', '\n').replace('\r', '\n')

        # 第一步：移除 <style>...</style> 块（CSS代码）
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)

        # 第二步：移除 <script>...</script> 块（JavaScript代码）
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

        # 第三步：移除 <!DOCTYPE> 声明
        text = re.sub(r'<!DOCTYPE[^>]*>', '', text, flags=re.IGNORECASE)

        # 第四步：移除 HTML 注释
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

        # 第五步：移除内联样式属性（style="..."）
        text = re.sub(r'\s+style\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)

        # 第六步：移除事件处理属性（onclick, onmouseover, 等）
        text = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)

        # 处理换行标签
        # 替换 <br> 和 <br/> 为换行符
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        # 替换 </p> 为换行符
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
        # 替换 </div> 为换行符
        text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)

        # 移除所有HTML标签
        text = re.sub(r'<[^>]+>', ' ', text)

        whitespace_mode = self.get_whitespace_mode()
        if whitespace_mode == "compress":
            # 压缩多个空白字符为单个空格
            text = re.sub(r'\s+', ' ', text)
            # 移除行首尾空白
            lines = [line.strip() for line in text.split('\n')]
            lines = [line for line in lines if line]  # 移除空行
            text = '\n'.join(lines)
        else:
            # 移除空行模式：只移除空行，保留原有空白
            lines = [line.rstrip() for line in text.split('\n')]
            lines = [line for line in lines if line.strip()]  # 移除空行
            text = '\n'.join(lines)

        return text

    def _extract_links(self, html_text):
        """
        从HTML中提取链接

        Args:
            html_text: HTML文本

        Returns:
            str: 提取的链接列表
        """
        # 提取所有href属性
        links = re.findall(r'href=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
        return '\n'.join(links)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.set_mode("visible_text")
        self.set_whitespace_mode("remove_empty")

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "html_extract",
            "mode": self.get_mode(),
            "whitespace_mode": self.get_whitespace_mode()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "html_extract":
            self.set_mode(config.get("mode", "visible_text"))
            self.set_whitespace_mode(config.get("whitespace_mode", "remove_empty"))

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "html_extract"
