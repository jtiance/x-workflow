# -*- coding: utf-8 -*-
"""
随机时间生成控件模块
提供在指定时间范围内生成随机时间的功能
"""
import random
import time
from datetime import datetime
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QGridLayout, QSizePolicy, QHBoxLayout
from qfluentwidgets import ComboBox, BodyLabel, SpinBox, FastCalendarPicker

from controls.base_control import BaseControl

# 日期时间格式映射（和datetime_convert保持一致）
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


class RandomDatetimeControl(BaseControl):
    """
    随机时间生成控件类
    提供在指定时间范围内生成随机时间的功能
    """

    def __init__(self, parent=None):
        """
        初始化随机时间生成控件

        Args:
            parent: 父控件
        """
        super().__init__("随机时间生成", parent)

    def _init_content(self):
        """
        初始化内容区域
        添加随机时间生成相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：时间范围
        range_label = BodyLabel("时间范围:")
        range_label.setMinimumWidth(70)
        range_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 创建水平布局容纳两个日期选择器
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)

        # 开始日期选择器
        self.start_date_picker = FastCalendarPicker()
        self.start_date_picker.setDateFormat("yyyy-MM-dd")
        # 默认设置为今天往前推1年
        default_start = QDate.currentDate().addYears(-1)
        self.start_date_picker.setDate(default_start)
        self.start_date_picker.dateChanged.connect(self._emit_parameters_changed)
        self.start_date_picker.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 结束日期选择器
        self.end_date_picker = FastCalendarPicker()
        self.end_date_picker.setDateFormat("yyyy-MM-dd")
        # 默认设置为今天
        default_end = QDate.currentDate()
        self.end_date_picker.setDate(default_end)
        self.end_date_picker.dateChanged.connect(self._emit_parameters_changed)
        self.end_date_picker.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        date_layout.addWidget(self.start_date_picker)
        date_layout.addWidget(self.end_date_picker)
        date_layout.addStretch()  # 右侧添加弹性空间

        grid_layout.addWidget(range_label, 0, 0)
        grid_layout.addLayout(date_layout, 0, 1)

        # 第2行：时间格式
        format_label = BodyLabel("时间格式:")
        format_label.setMinimumWidth(70)
        format_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.format_combo = ComboBox()
        self.format_combo.addItems([name for name, _ in DATETIME_FORMATS])
        self.format_combo.setCurrentText("年-月-日 时:分:秒")
        self.format_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.format_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(format_label, 1, 0)
        grid_layout.addWidget(self.format_combo, 1, 1)

        # 第3行：生成数量
        count_label = BodyLabel("生成数量:")
        count_label.setMinimumWidth(70)
        count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.count_spin = SpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(10000)
        self.count_spin.setSingleStep(10)
        self.count_spin.setValue(100)
        self.count_spin.setSuffix("个")
        self.count_spin.valueChanged.connect(self._emit_parameters_changed)
        self.count_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(count_label, 2, 0)
        grid_layout.addWidget(self.count_spin, 2, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

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
            return str(int(time.mktime(dt.timetuple()) * 1000 + random.randint(0, 999)))
        else:
            # 其他格式化字符串
            return dt.strftime(target_format)

    def execute(self, text):
        """
        执行随机时间生成操作

        Args:
            text: 输入文本（忽略，直接生成新内容）

        Returns:
            str: 生成的随机时间文本，每行一个
        """
        start_date = self.start_date_picker.getDate()
        end_date = self.end_date_picker.getDate()

        if not start_date.isValid() or not end_date.isValid():
            return ""

        # 确保开始日期 <= 结束日期
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        # 转换为时间戳
        start_dt = datetime(start_date.year(), start_date.month(), start_date.day(), 0, 0, 0)
        end_dt = datetime(end_date.year(), end_date.month(), end_date.day(), 23, 59, 59)

        start_ts = time.mktime(start_dt.timetuple())
        end_ts = time.mktime(end_dt.timetuple())

        count = self.count_spin.value()
        format_name = self.format_combo.currentText()
        target_format = FORMAT_MAP.get(format_name, "%Y-%m-%d %H:%M:%S")

        result = []
        for _ in range(count):
            # 生成随机时间戳
            random_ts = random.uniform(start_ts, end_ts)
            random_dt = datetime.fromtimestamp(random_ts)
            formatted = self._format_datetime(random_dt, target_format)
            result.append(formatted)

        return '\n'.join(result)

    def reset_parameters(self):
        """
        重置参数到默认值
        """
        # 默认开始日期为1年前
        default_start = QDate.currentDate().addYears(-1)
        self.start_date_picker.setDate(default_start)
        # 默认结束日期为今天
        default_end = QDate.currentDate()
        self.end_date_picker.setDate(default_end)
        self.format_combo.setCurrentText("年-月-日 时:分:秒")
        self.count_spin.setValue(100)

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 控件配置字典
        """
        start_date = self.start_date_picker.getDate()
        end_date = self.end_date_picker.getDate()

        return {
            "type": "random_datetime",
            "start_date": start_date.toString(Qt.DateFormat.ISODate) if start_date.isValid() else None,
            "end_date": end_date.toString(Qt.DateFormat.ISODate) if end_date.isValid() else None,
            "format": self.format_combo.currentText(),
            "count": self.count_spin.value()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 控件配置字典
        """
        if config.get("type") == "random_datetime":
            # 加载开始日期
            start_date_str = config.get("start_date")
            if start_date_str:
                start_date = QDate.fromString(start_date_str, Qt.DateFormat.ISODate)
                if start_date.isValid():
                    self.start_date_picker.setDate(start_date)

            # 加载结束日期
            end_date_str = config.get("end_date")
            if end_date_str:
                end_date = QDate.fromString(end_date_str, Qt.DateFormat.ISODate)
                if end_date.isValid():
                    self.end_date_picker.setDate(end_date)

            # 加载格式
            format_name = config.get("format", "年-月-日 时:分:秒")
            format_index = self.format_combo.findText(format_name)
            if format_index != -1:
                self.format_combo.setCurrentIndex(format_index)

            # 加载数量
            count = config.get("count", 100)
            self.count_spin.setValue(count)

    def get_control_type(self):
        """
        获取控件类型

        Returns:
            str: 控件类型标识
        """
        return "random_datetime"
