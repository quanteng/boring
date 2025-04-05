from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QGroupBox,
                               QPushButton, QLineEdit, QLabel, QSpinBox, QCheckBox,
                               QFileDialog, QFormLayout)
from PySide6.QtCore import Signal, Qt


class ToolPanel(QWidget):
    # 定义信号
    load_dcfq_signal = Signal()
    load_zdqy_signal = Signal()
    load_building_signal = Signal()
    generate_grid_signal = Signal(dict)
    plan_boring_signal = Signal(dict)
    avoid_buildings_signal = Signal()
    export_results_signal = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建标签页
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # 初始化各标签页
        self._init_data_tab()
        self._init_grid_tab()
        self._init_boring_tab()

        # 导出按钮
        self.btn_export = QPushButton("导出结果")
        self.btn_export.clicked.connect(self.export_results_signal.emit)
        self.layout.addWidget(self.btn_export)

    def _init_data_tab(self):
        """数据管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 调查分区组
        group_dcfq = QGroupBox("调查分区")
        layout_dcfq = QVBoxLayout()
        self.btn_load_dcfq = QPushButton("加载调查分区")
        self.btn_load_dcfq.clicked.connect(self.load_dcfq_signal.emit)
        layout_dcfq.addWidget(self.btn_load_dcfq)
        group_dcfq.setLayout(layout_dcfq)
        layout.addWidget(group_dcfq)

        # 重点区域组
        group_zdqy = QGroupBox("重点区域")
        layout_zdqy = QVBoxLayout()
        self.btn_load_zdqy = QPushButton("加载重点区域")
        self.btn_load_zdqy.clicked.connect(self.load_zdqy_signal.emit)
        layout_zdqy.addWidget(self.btn_load_zdqy)
        group_zdqy.setLayout(layout_zdqy)
        layout.addWidget(group_zdqy)

        # 建筑物组
        group_building = QGroupBox("建筑物")
        layout_building = QVBoxLayout()
        self.btn_load_building = QPushButton("加载建筑物")
        self.btn_load_building.clicked.connect(self.load_building_signal.emit)
        layout_building.addWidget(self.btn_load_building)
        group_building.setLayout(layout_building)
        layout.addWidget(group_building)

        self.tabs.addTab(tab, "数据管理")

    def _init_grid_tab(self):
        """网格设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 网格参数组
        group_params = QGroupBox("网格参数")
        layout_params = QFormLayout()

        # 网格大小
        self.spin_grid_size = QSpinBox()
        self.spin_grid_size.setRange(5, 200)
        self.spin_grid_size.setValue(20)
        layout_params.addRow("网格大小(m):", self.spin_grid_size)

        # 随机偏移
        self.cb_random_offset = QCheckBox("启用随机偏移")
        self.cb_random_offset.setChecked(True)
        layout_params.addRow(self.cb_random_offset)

        group_params.setLayout(layout_params)
        layout.addWidget(group_params)

        # 生成按钮
        self.btn_generate = QPushButton("生成网格")
        self.btn_generate.clicked.connect(self._generate_grid)
        layout.addWidget(self.btn_generate)

        self.tabs.addTab(tab, "网格设置")

    def _init_boring_tab(self):
        """钻孔规划标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 钻孔参数组
        group_params = QGroupBox("钻孔参数")
        layout_params = QFormLayout()

        # 普通钻孔步长
        self.spin_boring_step = QSpinBox()
        self.spin_boring_step.setRange(1, 20)
        self.spin_boring_step.setValue(2)
        layout_params.addRow("普通钻孔步长:", self.spin_boring_step)

        # 重点区域步长
        self.spin_boring_step_zdqy = QSpinBox()
        self.spin_boring_step_zdqy.setRange(1, 20)
        self.spin_boring_step_zdqy.setValue(1)
        layout_params.addRow("重点区域步长:", self.spin_boring_step_zdqy)

        # 监测井步长
        self.spin_wboring_step = QSpinBox()
        self.spin_wboring_step.setRange(1, 20)
        self.spin_wboring_step.setValue(8)
        layout_params.addRow("监测井步长:", self.spin_wboring_step)

        # 重点区域步长
        self.spin_wboring_step_zdqy = QSpinBox()
        self.spin_wboring_step_zdqy.setRange(1, 20)
        self.spin_wboring_step_zdqy.setValue(4)
        layout_params.addRow("重点区域步长:", self.spin_wboring_step_zdqy)

        # X偏移量
        self.spin_offset_x = QSpinBox()
        self.spin_offset_x.setRange(0, 20)
        layout_params.addRow("X偏移量:", self.spin_offset_x)

        # Y偏移量
        self.spin_offset_y = QSpinBox()
        self.spin_offset_y.setRange(0, 20)
        layout_params.addRow("Y偏移量:", self.spin_offset_y)

        group_params.setLayout(layout_params)
        layout.addWidget(group_params)

        # 建筑物避让组
        group_avoid = QGroupBox("建筑物避让")
        layout_avoid = QFormLayout()

        # 避让半径
        self.spin_avoid_radius = QSpinBox()
        self.spin_avoid_radius.setRange(5, 100)
        self.spin_avoid_radius.setValue(20)
        layout_avoid.addRow("避让半径(m):", self.spin_avoid_radius)

        # 避让按钮
        self.btn_avoid = QPushButton("执行避让")
        self.btn_avoid.clicked.connect(self.avoid_buildings_signal.emit)
        layout_avoid.addRow(self.btn_avoid)

        group_avoid.setLayout(layout_avoid)
        layout.addWidget(group_avoid)

        # 规划按钮
        self.btn_plan = QPushButton("规划钻孔")
        self.btn_plan.clicked.connect(self._plan_boring)
        layout.addWidget(self.btn_plan)

        self.tabs.addTab(tab, "钻孔规划")

    def _generate_grid(self):
        """生成网格参数并发射信号"""
        params = {
            'grid_size': self.spin_grid_size.value(),
            'random_offset': self.cb_random_offset.isChecked()
        }
        self.generate_grid_signal.emit(params)

    def _plan_boring(self):
        """规划钻孔参数并发射信号"""
        params = {
            'boring_step': self.spin_boring_step.value(),
            'boring_step_zdqy': self.spin_boring_step_zdqy.value(),
            'wboring_step': self.spin_wboring_step.value(),
            'wboring_step_zdqy': self.spin_wboring_step_zdqy.value(),
            'offset_x': self.spin_offset_x.value(),
            'offset_y': self.spin_offset_y.value()
        }
        self.plan_boring_signal.emit(params)