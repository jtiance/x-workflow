# -*- coding: utf-8 -*-
"""
控件选择对话框模块
用于选择要添加的控件类型
"""

from PySide6.QtWidgets import (
    QGridLayout, QLabel, QFrame, QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import ListWidget

from .custom_dialog import CustomDialog


class ControlDialog(CustomDialog):
    """
    控件选择对话框
    左侧显示可用控件列表，右侧显示选中控件的预览
    """

    # 定义信号：当用户确认选择控件时发出
    control_selected = Signal(str)  # 控件类型名称

    def __init__(self, parent=None):
        """
        初始化控件选择对话框

        Args:
            parent: 父控件
        """
        super().__init__(title="控件选择器", parent=parent)

        # 设置对话框属性
        self.setMinimumSize(600, 400)  # 设置最小尺寸
        self.setObjectName("ControlDialog")

        # 保存选中的控件类型
        self.selected_control = None

        # 调整内容区域边距
        self.set_content_margins(10, 10, 10, 10)
        self.set_content_spacing(10)

        # 初始化 UI
        self._init_ui()

        # 填充控件列表
        self._populate_control_list()

        # 默认选中第一个选项
        if self.control_list.count() > 0:
            self.control_list.setCurrentRow(0)

    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建网格布局 (2行2列)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # ============= 左侧：控件列表 =============
        # 列表标题
        left_title = QLabel("可用控件")
        left_title.setObjectName("ListTitle")

        # 控件列表
        self.control_list = ListWidget()
        self.control_list.setObjectName("ControlList")
        self.control_list.setMinimumWidth(200)  # 设置最小宽度
        self.control_list.setMinimumHeight(300)  # 设置最小高度
        # 通过边框体现列表范围（保留原有样式）
        self.control_list.setStyleSheet("""
            ListWidget {
                border: 1px solid #4a4a4a;
                border-radius: 4px;
            }
            ListWidget::item {
                min-height: 30px;
            }
            ListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)
        self.control_list.currentItemChanged.connect(self._on_selection_changed)
        self.control_list.itemDoubleClicked.connect(self._on_item_double_clicked)

        # ============= 右侧：预览区域 =============
        # 预览标题
        right_title = QLabel("控件预览")
        right_title.setObjectName("PreviewTitle")

        # 预览区域（使用 QFrame 作为容器）
        self.preview_area = QFrame()
        self.preview_area.setFrameShape(QFrame.StyledPanel)
        self.preview_area.setObjectName("PreviewArea")
        self.preview_area.setMinimumHeight(300)  # 设置最小高度
        # 设置边框样式，只针对这个 QFrame
        self.preview_area.setStyleSheet("""
            QFrame#PreviewArea {
                border: 1px solid #4a4a4a;
                border-radius: 4px;
            }
        """)

        # 预览区域的布局
        self.preview_layout = QVBoxLayout(self.preview_area)
        self.preview_layout.setContentsMargins(10, 10, 10, 10)

        # 初始提示标签
        self.preview_hint = QLabel("请从左侧选择一个控件")
        self.preview_hint.setAlignment(Qt.AlignCenter)
        self.preview_layout.addWidget(self.preview_hint)

        # ============= 添加到网格布局 =============
        # 第一行：标题
        grid_layout.addWidget(left_title, 0, 0)
        grid_layout.addWidget(right_title, 0, 1)

        # 第二行：内容
        grid_layout.addWidget(self.control_list, 1, 0)
        grid_layout.addWidget(self.preview_area, 1, 1)

        # 设置列宽比例 (左侧1，右侧4)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 4)

        # 将网格布局容器添加到内容区域
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        self.add_content_widget(grid_widget)

        # ============= 底部按钮区域 =============
        # 取消按钮
        self.add_button("取消", is_reject=True)
        # 确定按钮（主按钮蓝色）
        self.ok_button = self.add_button("确定", callback=self._on_ok_clicked, is_primary=True, is_accept=True)
        self.ok_button.setEnabled(False)  # 初始禁用，直到选择控件

    def _populate_control_list(self):
        """
        填充控件列表
        添加可用的控件类型
        """
        # 这里定义可用的控件类型
        # 格式：(显示名称, 控件类型标识)
        controls = [
            ("文本替换", "text_replace"),
            ("JSON格式化", "json_format"),
            ("JSON压缩", "json_compress"),
            ("XML格式化", "xml_format"),
            ("HTML格式化", "html_format"),
            ("增加文本", "add_text"),
            ("大小写转换", "case_convert"),
            ("文本分割", "text_split"),
            ("文本合并", "text_merge"),
            ("文本搜索删除", "text_search_delete"),
            ("移除重复行", "remove_duplicate"),
            ("移除空行", "remove_empty_lines"),
            ("文本裁剪", "text_trim"),
        ]

        # 添加到列表
        for display_name, control_type in controls:
            # 直接使用字符串添加项
            self.control_list.addItem(display_name)
            # 获取最后一项并设置数据
            last_item = self.control_list.item(self.control_list.count() - 1)
            last_item.setData(Qt.UserRole, control_type)

    def _on_selection_changed(self, current, previous):
        """
        当列表选择改变时调用

        Args:
            current: 当前选中的 item
            previous: 之前选中的 item
        """
        # 清空预览区域
        self._clear_preview()

        if current is not None:
            # 获取选中的控件类型
            control_type = current.data(Qt.UserRole)
            self.selected_control = control_type

            # 启用确定按钮
            self.ok_button.setEnabled(True)

            # 更新预览
            self._update_preview(control_type)
        else:
            # 没有选中任何项
            self.selected_control = None
            self.ok_button.setEnabled(False)

            # 显示提示
            self.preview_hint = QLabel("请从左侧选择一个控件")
            self.preview_hint.setAlignment(Qt.AlignCenter)
            self.preview_layout.addWidget(self.preview_hint)

    def _clear_preview(self):
        """
        清空预览区域
        """
        # 移除预览布局中的所有组件
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _update_preview(self, control_type):
        """
        更新预览区域，显示选中控件的预览

        Args:
            control_type: 控件类型标识
        """
        # 先添加一个 stretch，让控件能够在垂直方向居中
        self.preview_layout.addStretch()

        if control_type == "text_replace":
            # 文本替换控件预览
            from controls.text_replace import TextReplaceControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextReplaceControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_find_text("hello")
            preview_control.set_replace_text("world")

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "json_format":
            # JSON格式化控件预览
            from controls.json_format import JsonFormatControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = JsonFormatControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_indent(4)
            preview_control.set_sort_keys(True)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "json_compress":
            # JSON压缩控件预览
            from controls.json_compress import JsonCompressControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = JsonCompressControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_sort_keys(True)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "xml_format":
            # XML格式化控件预览
            from controls.xml_format import XmlFormatControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = XmlFormatControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_indent(2)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "html_format":
            # HTML格式化控件预览
            from controls.html_format import HtmlFormatControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = HtmlFormatControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_indent(2)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "add_text":
            # 增加文本控件预览
            from controls.add_text import AddTextControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = AddTextControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_operation_type("增加前缀")
            preview_control.set_text("> ")

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "case_convert":
            # 大小写转换控件预览
            from controls.case_convert import CaseConvertControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = CaseConvertControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "text_split":
            # 文本分割控件预览
            from controls.text_split import TextSplitControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextSplitControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_delimiter(",")

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "text_merge":
            # 文本合并控件预览
            from controls.text_merge import TextMergeControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextMergeControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_separator(", ")
            # 默认关闭换行功能
            preview_control.set_enable_line_break(False)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "text_search_delete":
            # 文本搜索删除控件预览
            from controls.text_search_delete import TextSearchDeleteControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextSearchDeleteControl()
            preview_control.setEnabled(False)  # 禁用交互
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.set_search_text("test")

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "remove_duplicate":
            # 移除重复行控件预览
            from controls.remove_duplicate import RemoveDuplicateControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = RemoveDuplicateControl()
            preview_control.setEnabled(False)
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "remove_empty_lines":
            # 移除空行控件预览
            from controls.remove_empty_lines import RemoveEmptyLinesControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = RemoveEmptyLinesControl()
            preview_control.setEnabled(False)
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

        elif control_type == "text_trim":
            # 文本裁剪控件预览
            from controls.text_trim import TextTrimControl

            # 创建预览控件（禁用交互，只用于显示）
            preview_control = TextTrimControl()
            preview_control.setEnabled(False)
            # 隐藏操作按钮
            if hasattr(preview_control, 'set_buttons_visible'):
                preview_control.set_buttons_visible(False)

            # 设置一些示例数据
            preview_control.match_edit.setText("test")

            # 添加到预览区域
            self.preview_layout.addWidget(preview_control)
            self.preview_layout.addStretch()

    def _on_ok_clicked(self):
        """
        当点击确定按钮时调用
        """
        if self.selected_control:
            # 发出信号
            self.control_selected.emit(self.selected_control)

    def _on_item_double_clicked(self, item):
        """
        当双击列表项时调用
        """
        if item:
            # 获取选中的控件类型
            self.selected_control = item.data(Qt.UserRole)
            # 发出信号
            self.control_selected.emit(self.selected_control)
            # 关闭对话框，返回 Accepted
            self.accept()

    def get_selected_control(self):
        """
        获取选中的控件类型

        Returns:
            str: 控件类型标识，如果没有选中则返回 None
        """
        return self.selected_control
