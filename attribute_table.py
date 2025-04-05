from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                               QTableWidgetItem, QHeaderView, QComboBox)
from PySide6.QtCore import Qt, Signal


class AttributeTable(QWidget):
    attribute_changed_signal = Signal(str, str, object)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 属性表格
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["属性", "值"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.layout.addWidget(self.table)

        # 当前状态
        self.current_layer_name = None
        self.current_feature_id = None

        # 连接信号
        self.table.cellChanged.connect(self.on_cell_changed)

    def show_features(self, gdf):
        """显示要素属性"""
        self.table.clearContents()

        if len(gdf) == 0:
            self.table.setRowCount(0)
            return

        # 获取第一个要素
        feature = gdf.iloc[0]

        # 排除几何字段
        fields = [col for col in gdf.columns if col not in ['geometry', 'moved', 'original_geom']]
        self.table.setRowCount(len(fields))

        # 保存当前要素ID
        self.current_feature_id = feature.get('id', None)

        # 填充表格
        for row, (field_name, value) in enumerate(feature[fields].items()):
            # 属性名列
            name_item = QTableWidgetItem(field_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            # 处理复杂类型
            if isinstance(value, (list, dict)):
                value = str(value)

            # 属性值列
            value_item = QTableWidgetItem(str(value))

            # 特殊字段处理
            if field_name == 'type':
                self._setup_type_combobox(row, value)
            else:
                self.table.setItem(row, 1, value_item)

    def _setup_type_combobox(self, row, current_value):
        """设置钻孔类型下拉框"""
        combo = QComboBox()
        combo.addItems(['BORING', 'WBORING', 'GeoBORING', 'Soilgas_BORING'])
        combo.setCurrentText(current_value)
        combo.currentTextChanged.connect(
            lambda text: self.on_combobox_changed(row, 'type', text))
        self.table.setCellWidget(row, 1, combo)

    def clear(self):
        """清空表格"""
        self.table.clearContents()
        self.table.setRowCount(0)
        self.current_layer_name = None
        self.current_feature_id = None

    def on_cell_changed(self, row, column):
        """单元格内容改变事件"""
        if column != 1 or self.current_feature_id is None:
            return

        field_name = self.table.item(row, 0).text()
        new_value = self.table.item(row, 1).text()

        if self.current_layer_name:
            self.attribute_changed_signal.emit(
                self.current_layer_name, field_name, new_value)

    def on_combobox_changed(self, row, field_name, new_value):
        """下拉框选择改变事件"""
        if self.current_layer_name and self.current_feature_id:
            self.attribute_changed_signal.emit(
                self.current_layer_name, field_name, new_value)