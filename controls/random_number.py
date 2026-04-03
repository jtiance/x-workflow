# -*- coding: utf-8 -*-
"""
随机数字生成控件模块
提供生成随机整数和浮点数的功能
"""

import random
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from qfluentwidgets import ComboBox, BodyLabel, SpinBox

from controls.base_control import BaseControl


class RandomNumberControl(BaseControl):
    """
    随机数字生成控件类
    生成指定长度的随机整数或浮点数
    """

    def __init__(self, parent=None):
        """
        初始化随机数字生成控件

        Args:
            parent: 父控件
        """
        super().__init__("随机数字生成", parent)
        # 标记是否由类型选择导致的小数位数禁用
        self._decimal_disabled_by_type = True

    def _init_content(self):
        """
        初始化内容区域
        添加随机数字生成相关的控件
        """
        layout = self.get_content_layout()

        # 使用GridLayout确保对齐
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # 第1行：类型选择
        type_label = BodyLabel("类型:")
        type_label.setMinimumWidth(90)
        type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.type_combo = ComboBox()
        self.type_combo.addItems(["整数", "浮点数"])
        self.type_combo.setCurrentText("整数")
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        self.type_combo.currentTextChanged.connect(self._emit_parameters_changed)
        self.type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(type_label, 0, 0)
        grid_layout.addWidget(self.type_combo, 0, 1)

        # 第2行：整数位数
        int_digits_label = BodyLabel("整数位数:")
        int_digits_label.setMinimumWidth(90)
        int_digits_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.int_digits_spin = SpinBox()
        self.int_digits_spin.setMinimum(1)
        self.int_digits_spin.setMaximum(100)
        self.int_digits_spin.setValue(10)
        self.int_digits_spin.setSingleStep(1)
        self.int_digits_spin.valueChanged.connect(self._emit_parameters_changed)
        self.int_digits_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(int_digits_label, 1, 0)
        grid_layout.addWidget(self.int_digits_spin, 1, 1)

        # 第3行：小数位数
        decimal_digits_label = BodyLabel("小数位数:")
        decimal_digits_label.setMinimumWidth(90)
        decimal_digits_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.decimal_digits_spin = SpinBox()
        self.decimal_digits_spin.setMinimum(0)
        self.decimal_digits_spin.setMaximum(100)
        self.decimal_digits_spin.setValue(10)
        self.decimal_digits_spin.setSingleStep(1)
        self.decimal_digits_spin.valueChanged.connect(self._emit_parameters_changed)
        self.decimal_digits_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 默认整数类型下禁用小数位数
        self.decimal_digits_spin.setEnabled(False)
        self._decimal_disabled_by_type = True

        grid_layout.addWidget(decimal_digits_label, 2, 0)
        grid_layout.addWidget(self.decimal_digits_spin, 2, 1)

        # 第4行：生成数量（参照随机时间控件）
        count_label = BodyLabel("生成数量:")
        count_label.setMinimumWidth(90)
        count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.count_spin = SpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(10000)
        self.count_spin.setSingleStep(10)
        self.count_spin.setValue(100)
        self.count_spin.setSuffix("个")
        self.count_spin.valueChanged.connect(self._emit_parameters_changed)
        self.count_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid_layout.addWidget(count_label, 3, 0)
        grid_layout.addWidget(self.count_spin, 3, 1)

        # 设置列拉伸，让第二列占据所有剩余空间
        grid_layout.setColumnStretch(1, 1)

        # 将GridLayout添加到内容布局
        layout.addLayout(grid_layout)

    def _on_type_changed(self):
        """类型选择变化处理"""
        current_type = self.type_combo.currentText()
        if current_type == "整数":
            # 整数类型下始终禁用小数位数
            self._decimal_disabled_by_type = True
            self.decimal_digits_spin.setEnabled(False)
        else:
            # 浮点数类型下，小数位数的启用状态跟随整体控件状态
            self._decimal_disabled_by_type = False
            # 只有当控件整体启用时，小数位数才启用
            self.decimal_digits_spin.setEnabled(self.isEnabled())
        # 发出参数改变信号
        self._emit_parameters_changed()

    def set_disabled_state(self, disabled):
        """
        重写父类的禁用状态设置方法

        Args:
            disabled: 是否禁用
        """
        # 调用父类方法处理通用的禁用逻辑
        super().set_disabled_state(disabled)

        # 对于小数位数，需要同时考虑控件禁用状态和类型状态
        # 如果控件被禁用，则禁用小数位数
        # 如果控件被启用，则根据类型决定是否启用小数位数
        if disabled:
            self.decimal_digits_spin.setEnabled(False)
        else:
            # 如果是整数类型，小数位数始终禁用
            # 如果是浮点数类型，小数位数启用
            self.decimal_digits_spin.setEnabled(not self._decimal_disabled_by_type)

    def execute(self, text):
        """
        执行控件核心逻辑
        生成随机数字

        Args:
            text: 输入文本（本控件不使用输入文本）

        Returns:
            str: 生成的随机数字字符串，多个结果每行一个
        """
        try:
            current_type = self.type_combo.currentText()
            int_digits = self.int_digits_spin.value()
            count = self.count_spin.value()

            results = []
            for _ in range(count):
                if current_type == "整数":
                    # 生成整数
                    min_num = 10 ** (int_digits - 1) if int_digits > 1 else 0
                    max_num = (10 ** int_digits) - 1
                    result = random.randint(min_num, max_num)
                    results.append(str(result))
                else:
                    # 生成浮点数
                    decimal_digits = self.decimal_digits_spin.value()
                    # 生成整数部分
                    int_part = random.randint(0, (10 ** int_digits) - 1)
                    # 生成小数部分
                    if decimal_digits > 0:
                        decimal_part = random.randint(0, (10 ** decimal_digits) - 1)
                        result = f"{int_part}.{str(decimal_part).zfill(decimal_digits)}"
                    else:
                        result = str(int_part)
                    results.append(result)

            return "\n".join(results)

        except Exception as e:
            return f"生成随机数字失败: {str(e)}"

    def get_config(self):
        """
        获取控件配置

        Returns:
            dict: 配置字典
        """
        return {
            "type": self.type_combo.currentText(),
            "int_digits": self.int_digits_spin.value(),
            "decimal_digits": self.decimal_digits_spin.value(),
            "count": self.count_spin.value()
        }

    def load_config(self, config):
        """
        加载控件配置

        Args:
            config: 配置字典
        """
        # 加载类型配置
        number_type = config.get("type", "整数")
        if number_type in ["整数", "浮点数"]:
            self.type_combo.setCurrentText(number_type)
        else:
            self.type_combo.setCurrentText("整数")

        # 加载整数位数配置
        int_digits = config.get("int_digits", 10)
        self.int_digits_spin.setValue(int_digits)

        # 加载小数位数配置
        decimal_digits = config.get("decimal_digits", 10)
        self.decimal_digits_spin.setValue(decimal_digits)

        # 加载生成数量配置
        count = config.get("count", 100)
        self.count_spin.setValue(count)

        # 触发类型变化事件，更新UI状态
        self._on_type_changed()

    def get_control_type(self):
        """
        获取控件类型标识

        Returns:
            str: 控件类型字符串
        """
        return "random_number"

    def reset_parameters(self):
        """重置参数为默认值"""
        # 重置类型为整数
        self.type_combo.setCurrentText("整数")
        # 重置整数位数为10
        self.int_digits_spin.setValue(10)
        # 重置小数位数为10
        self.decimal_digits_spin.setValue(10)
        # 重置生成数量为100
        self.count_spin.setValue(100)
