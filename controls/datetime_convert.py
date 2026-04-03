# -*- coding: utf-8 -*-
"""
日期时间转换控件模块
提供不同格式日期时间之间的转换功能
"""
import time
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from qfluentwidgets import ComboBox, BodyLabel

from controls.base_control import BaseControl

# 日期时间格式映射
DATETIME_FORMATS = [
    ("时间戳(秒)", "timestamp_s"),
    ("时间戳(毫秒)", "timestamp_ms"),
    ("年-月-日 时:分:秒", "%Y-%m-%d %H:%M:%S"),
    ("年月日时分秒", "%Y%m%d%H%M%S"),
    ("年-月-日", "%Y-%m-%d"),
    ("年月日", "%Y%m%d"),
    ("时(24):分:秒", "%H:%M:%S"),
    ("时(12):分:秒", "%I:%M:%S"),
]

# 显示名称到格式的映射
FORMAT_MAP = {name: fmt for name, fmt in DATETIME_FORMATS}


class DatetimeConvertControl(BaseControl):
    """
    日期时间转换控件类
    提供不同格式日期时间之间的转换功能
    """

    def __init__(self, parent=None):
        """
        初始化日期时间转换控件

        Args:
            parent: 父控件
        """
        super().__init__("日期时间转换", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加日期时间转换相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：源格式
        source_label = BodyLabel("从:")
        source_label.setMinimumWidth(70)
        source_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.source_combo = ComboBox()
        self.source_combo.addItems([name for name, _ in DATETIME_FORMATS])
        self.source_combo.setCurrentText("时间戳(秒)")
        self.source_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.source_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(source_label, 0, 0)
        grid_layout.addWidget(self.source_combo, 0, 1)

        # 第2行：目标格式
        target_label = BodyLabel("到:")
        target_label.setMinimumWidth(70)
        target_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.target_combo = ComboBox()
        self.target_combo.addItems([name for name, _ in DATETIME_FORMATS])
        self.target_combo.setCurrentText("年-月-日 时:分:秒")
        self.target_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.target_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(target_label, 1, 0)
        grid_layout.addWidget(self.target_combo, 1, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def _parse_datetime(self, text, source_format):
        """
        解析输入文本为datetime对象

        Args:
            text: 输入文本
            source_format: 源格式

        Returns:
            datetime: 解析后的datetime对象
        """
        text = text.strip()
        if not text:
            return None

        if source_format == "timestamp_s":
            # 时间戳（秒）
            try:
                timestamp = float(text)
                return datetime.fromtimestamp(timestamp)
            except (ValueError, TypeError):
                return None
        elif source_format == "timestamp_ms":
            # 时间戳（毫秒）
            try:
                timestamp = float(text) / 1000
                return datetime.fromtimestamp(timestamp)
            except (ValueError, TypeError):
                return None
        else:
            # 其他格式化字符串
            try:
                return datetime.strptime(text, source_format)
            except (ValueError, TypeError):
                return None

    def _format_datetime(self, dt, target_format):
        """
        格式化datetime对象为目标格式

        Args:
            dt: datetime对象
            target_format: 目标格式

        Returns:
            str: 格式化后的字符串
        """
        if not dt:
            return ""

        if target_format == "timestamp_s":
            # 时间戳（秒）
            return str(int(time.mktime(dt.timetuple())))
        elif target_format == "timestamp_ms":
            # 时间戳（毫秒）
            return str(int(time.mktime(dt.timetuple()) * 1000))
        else:
            # 其他格式化字符串
            return dt.strftime(target_format)

    def execute(self, text):
        """
        执行日期时间转换操作，对每一行都执行相同的操作

        Args:
            text: 要处理的文本

        Returns:
            str: 处理后的文本
        """
        if not text:
            return text

        source_name = self.source_combo.currentText()
        target_name = self.target_combo.currentText()

        source_format = FORMAT_MAP.get(source_name)
        target_format = FORMAT_MAP.get(target_name)

        if not source_format or not target_format:
            return text

        lines = text.split('\n')
        result = []

        for line in lines:
            if not line.strip():
                result.append(line)
                continue

            dt = self._parse_datetime(line, source_format)
            if dt:
                formatted = self._format_datetime(dt, target_format)
                result.append(formatted)
            else:
                # 解析失败保留原内容
                result.append(line)

        return '\n'.join(result)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        self.source_combo.setCurrentText("时间戳(秒)")
        self.target_combo.setCurrentText("年-月-日 时:分:秒")

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        return {
            "type": "datetime_convert",
            "source_format": self.source_combo.currentText(),
            "target_format": self.target_combo.currentText()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "datetime_convert":
            source_format = config.get("source_format", "时间戳(秒)")
            target_format = config.get("target_format", "年-月-日 时:分:秒")

            source_index = self.source_combo.findText(source_format)
            if source_index != -1:
                self.source_combo.setCurrentIndex(source_index)

            target_index = self.target_combo.findText(target_format)
            if target_index != -1:
                self.target_combo.setCurrentIndex(target_index)

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "datetime_convert"
