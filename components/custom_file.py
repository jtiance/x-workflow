# -*- coding: utf-8 -*-
"""
自定义文件选择组件
类似 CustomFolder，但用于选择文件，支持后缀过滤
"""

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import LineEdit
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.components.widgets.line_edit import LineEditButton


class CustomFile(LineEdit):
    """文件选择输入框"""

    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fileButton = LineEditButton(FIF.DOCUMENT, self)
        self._file_filters = []  # 文件过滤后缀列表

        self.hBoxLayout.addWidget(self.fileButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.fileButton.clicked.connect(self._open_file_dialog)
        self.clearButton.clicked.connect(self.clear)

    def set_file_filters(self, filters: list[str]):
        """设置允许的文件后缀过滤
        :param filters: 后缀列表，如 ["xlsx", "xls", "csv"]
        """
        self._file_filters = filters

    def _open_file_dialog(self):
        """打开文件选择对话框"""
        # 构建过滤字符串
        filter_str = ""
        if self._file_filters:
            extensions = " ".join([f"*.{ext}" for ext in self._file_filters])
            filter_str = f"支持的文件 ({extensions});;所有文件 (*.*)"

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            self.text() or "",
            filter_str
        )
        if file_path:
            self.setText(file_path)
            self.file_selected.emit(file_path)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28 * enable + 30, 0)
