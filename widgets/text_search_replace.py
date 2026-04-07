# -*- coding: utf-8 -*-
"""
统一搜索替换组件
整合搜索和替换功能，支持单行/双行模式切换
"""
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QGridLayout
)
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import SearchLineEdit, LineEdit, TransparentToolButton
from qfluentwidgets import FluentIcon as FIF

from components.custom_case_tool_button import CustomCaseToolButton
from components.custom_regex_tool_button import CustomRegexToolButton
from components.custom_replace_tool_button import CustomReplaceToolButton
from components.custom_replace_all_tool_button import CustomReplaceAllToolButton


class TextSearchReplace(QWidget):
    """
    统一搜索替换组件
    """

    # 定义信号
    search_requested = Signal(str, bool, bool)  # 搜索请求：(搜索内容, 是否区分大小写, 是否使用正则)
    find_next_requested = Signal()  # 查找下一个
    find_previous_requested = Signal()  # 查找上一个
    replace_current_requested = Signal(str)  # 替换当前匹配项：(替换文本)
    replace_all_requested = Signal(str)  # 替换所有匹配项：(替换文本)
    close_requested = Signal()  # 关闭请求

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_replace_mode = False  # 是否显示替换行
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """初始化界面"""
        # 使用网格布局，支持双行结构
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # ========== 第一行：搜索 ==========
        # 搜索输入框
        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        self.search_input.setClearButtonEnabled(True)
        layout.addWidget(self.search_input, 0, 0)

        # 搜索功能按钮容器
        search_button_layout = QHBoxLayout()
        search_button_layout.setSpacing(0)

        # 忽略大小写按钮
        self.case_sensitive_btn = CustomCaseToolButton(
            icon_size=QtCore.QSize(16, 16),
            checked=False
        )
        search_button_layout.addWidget(self.case_sensitive_btn)

        # 正则搜索按钮
        self.regex_btn = CustomRegexToolButton(
            icon_size=QtCore.QSize(16, 16),
            checked=False
        )
        search_button_layout.addWidget(self.regex_btn)

        # 上一个按钮
        self.prev_btn = TransparentToolButton()
        self.prev_btn.setIcon(FIF.UP.icon())
        self.prev_btn.setToolTip("上一个匹配")
        self.prev_btn.setIconSize(QtCore.QSize(12, 12))
        search_button_layout.addWidget(self.prev_btn)

        # 下一个按钮
        self.next_btn = TransparentToolButton()
        self.next_btn.setIcon(FIF.DOWN.icon())
        self.next_btn.setToolTip("下一个匹配")
        self.next_btn.setIconSize(QtCore.QSize(12, 12))
        search_button_layout.addWidget(self.next_btn)

        # 匹配计数
        self.match_count_label = QLabel("0/0")
        self.match_count_label.setAlignment(Qt.AlignCenter)
        self.match_count_label.setMinimumWidth(40)
        search_button_layout.addWidget(self.match_count_label)

        # 替换切换按钮
        self.toggle_replace_btn = TransparentToolButton()
        self.toggle_replace_btn.setIcon(FIF.CARE_DOWN_SOLID.icon())
        self.toggle_replace_btn.setToolTip("展开替换选项")
        self.toggle_replace_btn.setIconSize(QtCore.QSize(12, 12))
        search_button_layout.addWidget(self.toggle_replace_btn)

        # 关闭按钮
        self.close_btn = TransparentToolButton()
        self.close_btn.setIcon(FIF.CLOSE.icon())
        self.close_btn.setToolTip("关闭搜索")
        self.close_btn.setIconSize(QtCore.QSize(12, 12))
        search_button_layout.addWidget(self.close_btn)

        layout.addLayout(search_button_layout, 0, 1)

        # ========== 第二行：替换（默认隐藏） ==========
        # 替换输入框
        self.replace_input = LineEdit()
        self.replace_input.setPlaceholderText("替换为...")
        self.replace_input.setClearButtonEnabled(True)
        layout.addWidget(self.replace_input, 1, 0)
        self.replace_input.hide()

        # 替换按钮容器
        self.replace_button_layout = QHBoxLayout()
        self.replace_button_layout.setSpacing(0)

        # 替换按钮（默认隐藏）
        self.replace_btn = CustomReplaceToolButton(
            icon_size=QtCore.QSize(16, 16)
        )
        # 修改字体大小不覆盖原有样式
        font = self.replace_btn.font()
        font.setPointSize(12)
        self.replace_btn.setFont(font)
        self.replace_btn.hide()
        self.replace_button_layout.addWidget(self.replace_btn)

        # 全部替换按钮（默认隐藏）
        self.replace_all_btn = CustomReplaceAllToolButton(
            icon_size=QtCore.QSize(16, 16)
        )
        # 修改字体大小不覆盖原有样式
        font = self.replace_all_btn.font()
        font.setPointSize(12)
        self.replace_all_btn.setFont(font)
        self.replace_all_btn.hide()
        self.replace_button_layout.addWidget(self.replace_all_btn)

        # 添加弹性填充
        self.replace_button_layout.addStretch()

        layout.addLayout(self.replace_button_layout, 1, 1)
        # 隐藏替换行（设置最小高度为0，拉伸因子为0）
        layout.setRowMinimumHeight(1, 0)
        layout.setRowStretch(1, 0)

        # 设置列拉伸因子
        layout.setColumnStretch(0, 8)
        layout.setColumnStretch(1, 2)

    def _connect_signals(self):
        """连接信号槽"""
        # 搜索输入框文本变化时触发搜索
        self.search_input.textChanged.connect(self._on_search_input_changed)

        # 忽略大小写按钮切换时重新搜索
        self.case_sensitive_btn.toggled.connect(self._on_search_option_changed)

        # 正则按钮切换时重新搜索
        self.regex_btn.toggled.connect(self._on_search_option_changed)

        # 导航按钮
        self.prev_btn.clicked.connect(self.find_next_requested)
        self.next_btn.clicked.connect(self.find_previous_requested)

        # 替换切换按钮
        self.toggle_replace_btn.clicked.connect(self._toggle_replace_mode)

        # 替换按钮
        self.replace_btn.clicked.connect(self._on_replace_current)
        self.replace_all_btn.clicked.connect(self._on_replace_all)

        # 关闭按钮
        self.close_btn.clicked.connect(self.close_requested)

    def _on_search_input_changed(self):
        """搜索输入框内容变化时触发"""
        self._emit_search_request()

    def _on_search_option_changed(self):
        """搜索选项变化时触发"""
        self._emit_search_request()

    def _emit_search_request(self):
        """发出搜索请求信号"""
        pattern = self.search_input.text()
        # 按钮选中表示忽略大小写，所以case_sensitive取反
        case_sensitive = not self.case_sensitive_btn.isChecked()
        use_regex = self.regex_btn.isChecked()
        self.search_requested.emit(pattern, case_sensitive, use_regex)

    def _toggle_replace_mode(self):
        """切换替换模式显示/隐藏"""
        self._is_replace_mode = not self._is_replace_mode
        layout = self.layout()

        if self._is_replace_mode:
            # 显示替换行
            self.replace_input.show()
            self.replace_btn.show()
            self.replace_all_btn.show()
            layout.setRowMinimumHeight(1, self.replace_input.sizeHint().height())
            layout.setRowStretch(1, 0)
            self.toggle_replace_btn.setIcon(FIF.CARE_UP_SOLID.icon())
            self.toggle_replace_btn.setToolTip("收起替换选项")
            self.replace_input.setFocus()
        else:
            # 隐藏替换行
            self.replace_input.hide()
            self.replace_btn.hide()
            self.replace_all_btn.hide()
            layout.setRowMinimumHeight(1, 0)
            layout.setRowStretch(1, 0)
            self.toggle_replace_btn.setIcon(FIF.CARE_DOWN_SOLID.icon())
            self.toggle_replace_btn.setToolTip("展开替换选项")
            self.search_input.setFocus()

    def _on_replace_current(self):
        """替换当前匹配项"""
        replace_str = self.replace_input.text()
        self.replace_current_requested.emit(replace_str)

    def _on_replace_all(self):
        """替换所有匹配项"""
        replace_str = self.replace_input.text()
        self.replace_all_requested.emit(replace_str)

    def update_match_count(self, current, total):
        """
        更新匹配计数显示

        Args:
            current: 当前匹配索引(从1开始)
            total: 总匹配数
        """
        if total == 0:
            self.match_count_label.setText("0/0")
        else:
            self.match_count_label.setText(f"{current}/{total}")

    def set_focus(self):
        """设置焦点到搜索输入框"""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def get_search_pattern(self):
        """获取当前搜索内容"""
        return self.search_input.text()

    def get_replace_text(self):
        """获取替换文本"""
        return self.replace_input.text()

    def is_case_sensitive(self):
        """是否区分大小写"""
        return not self.case_sensitive_btn.isChecked()

    def use_regex(self):
        """是否使用正则表达式"""
        return self.regex_btn.isChecked()

    def show_search_mode(self):
        """显示为搜索模式（单行）"""
        self.show()
        self._is_replace_mode = False
        layout = self.layout()
        # 隐藏替换行
        self.replace_input.hide()
        self.replace_btn.hide()
        self.replace_all_btn.hide()
        layout.setRowMinimumHeight(1, 0)
        layout.setRowStretch(1, 0)
        self.toggle_replace_btn.setIcon(FIF.CARE_DOWN_SOLID.icon())
        self.toggle_replace_btn.setToolTip("展开替换选项")
        self.set_focus()

    def show_replace_mode(self):
        """显示为替换模式（双行）"""
        self.show()
        self._is_replace_mode = True
        layout = self.layout()
        # 显示替换行
        self.replace_input.show()
        self.replace_btn.show()
        self.replace_all_btn.show()
        layout.setRowMinimumHeight(1, self.replace_input.sizeHint().height())
        layout.setRowStretch(1, 0)
        self.toggle_replace_btn.setIcon(FIF.UP.icon())
        self.toggle_replace_btn.setToolTip("收起替换选项")
        self.set_focus()

    def clear_all(self):
        """清空所有输入和状态"""
        self.search_input.clear()
        self.replace_input.clear()
        self.case_sensitive_btn.setChecked(False)
        self.regex_btn.setChecked(False)
        self.update_match_count(0, 0)
