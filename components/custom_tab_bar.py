# -*- coding: utf-8 -*-
"""
自定义了 Tab 标签栏组件模块
"""
from qfluentwidgets import TabBar
from components.custom_tab_item import CustomTabItem


class CustomTabBar(TabBar):
    """自定义 TabBar，使用自定义 TabItem"""

    def insertTab(self, index: int, routeKey: str, text: str, icon=None, onClick=None):
        """重写 insertTab 方法，使用 CustomTabItem"""
        if routeKey in self.itemMap:
            raise ValueError(f"The route key `{routeKey}` is duplicated.")

        if index == -1:
            index = len(self.items)

        # 调整当前索引
        if index <= self.currentIndex() and self.currentIndex() >= 0:
            self._currentIndex += 1

        # 使用自定义的 CustomTabItem
        item = CustomTabItem(text, self.view, icon)
        item.setRouteKey(routeKey)

        # 设置标签大小
        w = self.tabMaximumWidth() if self.isScrollable() else self.tabMinimumWidth()
        item.setMinimumWidth(w)
        item.setMaximumWidth(self.tabMaximumWidth())

        item.setShadowEnabled(self.isTabShadowEnabled())
        item.setCloseButtonDisplayMode(self.closeButtonDisplayMode)
        item.setSelectedBackgroundColor(
            self.lightSelectedBackgroundColor, self.darkSelectedBackgroundColor)

        item.pressed.connect(self._onItemPressed)
        item.doubleClicked.connect(lambda: self.tabBarDoubleClicked.emit(self.items.index(item)))
        item.closed.connect(lambda: self.tabCloseRequested.emit(self.items.index(item)))
        if onClick:
            item.pressed.connect(onClick)

        self.itemLayout.insertWidget(index, item, 1)
        self.items.insert(index, item)
        self.itemMap[routeKey] = item

        if len(self.items) == 1:
            self.setCurrentIndex(0)

        return item
