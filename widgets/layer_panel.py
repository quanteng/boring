from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                               QHeaderView, QPushButton, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDrag


class LayerPanel(QWidget):
    layer_visibility_changed_signal = Signal(str, bool)
    layer_order_changed_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 图层树控件
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(2)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tree.model().rowsMoved.connect(self._update_layer_order)
        self.tree.itemChanged.connect(self.on_item_changed)
        self.layout.addWidget(self.tree)

        # 操作按钮
        btn_layout = QVBoxLayout()
        self.btn_remove = QPushButton("移除选中图层")
        self.btn_remove.clicked.connect(self.remove_selected_layers)
        btn_layout.addWidget(self.btn_remove)
        self.layout.addLayout(btn_layout)

    def add_layer(self, name, layer_type, visible=True):
        """添加图层到树形列表"""
        item = QTreeWidgetItem(self.tree)
        item.setText(0, name)
        item.setData(0, Qt.UserRole, layer_type)
        item.setCheckState(0, Qt.Checked if visible else Qt.Unchecked)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
        self.tree.addTopLevelItem(item)
        self._update_layer_order()

    def remove_layer(self, name):
        """移除指定图层"""
        items = self.tree.findItems(name, Qt.MatchExactly, 0)
        if items:
            index = self.tree.indexOfTopLevelItem(items[0])
            self.tree.takeTopLevelItem(index)
            self._update_layer_order()

    def remove_selected_layers(self):
        """移除选中图层"""
        for item in self.tree.selectedItems():
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)
        self._update_layer_order()

    def clear(self):
        """清除所有图层"""
        self.tree.clear()
        self._update_layer_order()

    def _update_layer_order(self):
        """更新图层顺序并发射信号"""
        order = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            order.append(item.text(0))
        self.layer_order_changed_signal.emit(order)

    def on_item_changed(self, item, column):
        """图层可见性改变事件"""
        if column == 0:
            layer_name = item.text(0)
            visible = item.checkState(0) == Qt.Checked
            self.layer_visibility_changed_signal.emit(layer_name, visible)