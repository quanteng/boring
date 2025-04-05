import sys
import os
import geopandas as gpd
from PySide6.QtWidgets import (QApplication, QMainWindow, QDockWidget,
                               QStatusBar, QToolBar, QMenuBar,QLabel, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt, Signal
from core.map_viewer import MapViewer
from core.boring_planner import BoringPlanner
from widgets.layer_panel import LayerPanel
from widgets.attribute_table import AttributeTable
from widgets.tool_panel import ToolPanel
from shapely.geometry import Point


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("钻孔布点规划系统 v3.0")
        self.resize(1400, 900)

        # 初始化核心组件
        self.planner = BoringPlanner()
        self.map_viewer = MapViewer()
        self.setCentralWidget(self.map_viewer)

        # 初始化UI
        self._init_menubar()
        self._init_toolbar()
        self._init_dock_widgets()
        self._init_statusbar()

        # 连接信号槽
        self._connect_signals()

        # 状态变量
        self.current_project_path = None
        self.has_unsaved_changes = False

    def _init_menubar(self):
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")
        file_menu.addAction("新建项目", self.new_project)
        file_menu.addAction("打开项目...", self.open_project)
        file_menu.addAction("保存项目", self.save_project)
        file_menu.addAction("另存为...", self.save_project_as)
        file_menu.addSeparator()
        file_menu.addAction("导出结果...", self.export_results)
        file_menu.addSeparator()
        file_menu.addAction("退出", self.close)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        self.undo_action = edit_menu.addAction("撤销")
        self.redo_action = edit_menu.addAction("重做")
        edit_menu.addSeparator()
        edit_menu.addAction("设置...")

        # 视图菜单
        view_menu = menubar.addMenu("视图")
        view_menu.addAction("全图", self.map_viewer.zoom_to_full)
        view_menu.addAction("放大", self.map_viewer.zoom_in)
        view_menu.addAction("缩小", self.map_viewer.zoom_out)
        view_menu.addSeparator()
        view_menu.addAction("重置视图", self.reset_view)

        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        tools_menu.addAction("生成网格", self.generate_grid)
        tools_menu.addAction("规划钻孔", self.plan_boring)
        tools_menu.addAction("避让建筑物", self.avoid_buildings)
        tools_menu.addAction("优化布点", self.optimize_points)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        help_menu.addAction("使用说明", self.show_help)
        help_menu.addAction("关于", self.show_about)

    def _init_toolbar(self):
        """初始化工具栏"""
        toolbar = QToolBar("主工具栏")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 文件操作
        toolbar.addAction("打开", self.open_project)
        toolbar.addAction("保存", self.save_project)
        toolbar.addSeparator()

        # 视图操作
        toolbar.addAction("放大", self.map_viewer.zoom_in)
        toolbar.addAction("缩小", self.map_viewer.zoom_out)
        toolbar.addAction("全图", self.map_viewer.zoom_to_full)
        toolbar.addSeparator()

        # 编辑工具
        toolbar.addAction("选择", lambda: self.map_viewer.set_edit_mode('select'))
        toolbar.addAction("移动", lambda: self.map_viewer.set_edit_mode('move'))
        toolbar.addAction("删除", lambda: self.map_viewer.set_edit_mode('delete'))
        toolbar.addSeparator()

        # 规划工具
        toolbar.addAction("生成网格", self.generate_grid)
        toolbar.addAction("规划钻孔", self.plan_boring)
        toolbar.addSeparator()

        # 优化工具
        toolbar.addAction("避让建筑", self.avoid_buildings)
        toolbar.addAction("优化布点", self.optimize_points)

    def _init_dock_widgets(self):
        """初始化停靠窗口"""
        # 左侧工具面板
        self.tool_panel = ToolPanel()
        left_dock = QDockWidget("工具面板", self)
        left_dock.setWidget(self.tool_panel)
        left_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)

        # 右侧图层面板
        self.layer_panel = LayerPanel()
        right_dock = QDockWidget("图层控制", self)
        right_dock.setWidget(self.layer_panel)
        right_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)

        # 底部属性面板
        self.attribute_table = AttributeTable()
        bottom_dock = QDockWidget("属性表格", self)
        bottom_dock.setWidget(self.attribute_table)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottom_dock)

    def _init_statusbar(self):
        """初始化状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # 坐标显示
        self.coord_label = QLabel("坐标: ")
        self.statusbar.addPermanentWidget(self.coord_label)

        # 比例尺
        self.scale_label = QLabel("比例: ")
        self.statusbar.addPermanentWidget(self.scale_label)

        # 默认消息
        self.statusbar.showMessage("就绪")

    def _connect_signals(self):
        """连接信号与槽"""
        # 工具面板信号
        self.tool_panel.load_dcfq_signal.connect(self.load_dcfq_file)
        self.tool_panel.load_zdqy_signal.connect(self.load_zdqy_file)
        self.tool_panel.load_building_signal.connect(self.load_building_file)
        self.tool_panel.generate_grid_signal.connect(self.generate_grid)
        self.tool_panel.plan_boring_signal.connect(self.plan_boring)
        self.tool_panel.avoid_buildings_signal.connect(self.avoid_buildings)
        self.tool_panel.export_results_signal.connect(self.export_results)

        # 地图视图信号
        self.map_viewer.point_selected_signal.connect(self.on_point_selected)
        self.map_viewer.point_moved_signal.connect(self.on_point_moved)
        self.map_viewer.coord_changed_signal.connect(self.update_coord_display)

        # 图层面板信号
        self.layer_panel.layer_visibility_changed_signal.connect(
            self.map_viewer.set_layer_visibility)
        self.layer_panel.layer_order_changed_signal.connect(
            self.map_viewer.update_layer_order)
        self.layer_panel.layer_style_changed_signal.connect(
            self.map_viewer.update_layer_style)

        # 属性表格信号
        self.attribute_table.attribute_changed_signal.connect(
            self.on_attribute_changed)

    # ======================== 文件操作 ========================
    def new_project(self):
        """新建项目"""
        if self.check_unsaved_changes():
            self.reset_project()

    def open_project(self):
        """打开项目"""
        if self.check_unsaved_changes():
            path, _ = QFileDialog.getOpenFileName(
                self, "打开项目", "", "钻孔规划项目 (*.bpp);;所有文件 (*)")
            if path:
                self.load_project(path)

    def save_project(self):
        """保存项目"""
        if self.current_project_path:
            self._save_project(self.current_project_path)
        else:
            self.save_project_as()

    def save_project_as(self):
        """项目另存为"""
        path, _ = QFileDialog.getSaveFileName(
            self, "另存为", "", "钻孔规划项目 (*.bpp);;所有文件 (*)")
        if path:
            self._save_project(path)
            self.current_project_path = path
            self.setWindowTitle(f"钻孔布点规划系统 v3.0 - {os.path.basename(path)}")

    def export_results(self):
        """导出结果"""
        if not hasattr(self, 'boring_gdf') or self.boring_gdf.empty:
            QMessageBox.warning(self, "警告", "没有可导出的钻孔数据")
            return

        path, filter = QFileDialog.getSaveFileName(
            self, "导出结果", "",
            "Shapefile (*.shp);;GeoJSON (*.geojson);;CSV (*.csv);;KML (*.kml)")

        if path:
            try:
                if path.endswith('.shp'):
                    self.boring_gdf.to_file(path)
                elif path.endswith('.geojson'):
                    self.boring_gdf.to_file(path, driver='GeoJSON')
                elif path.endswith('.csv'):
                    self.boring_gdf.to_csv(path)
                elif path.endswith('.kml'):
                    self.boring_gdf.to_file(path, driver='KML')

                self.statusbar.showMessage(f"结果已导出到: {path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    # ======================== 数据加载 ========================
    def load_dcfq_file(self):
        """加载调查分区文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择调查分区文件", "",
            "Shapefile (*.shp);;GeoJSON (*.geojson);;所有文件 (*)")

        if path:
            try:
                self.dcfq_gdf = gpd.read_file(path)

                # 检查坐标系
                if self.dcfq_gdf.crs is None:
                    reply = QMessageBox.question(
                        self, "坐标系缺失",
                        "调查分区文件缺少坐标系，是否设置为WGS84(EPSG:4326)?",
                        QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.dcfq_gdf = self.dcfq_gdf.set_crs("EPSG:4326")
                    else:
                        return

                # 修复几何错误
                self.dcfq_gdf.geometry = self.dcfq_gdf.geometry.make_valid()

                # 添加到地图
                self.map_viewer.add_layer(
                    self.dcfq_gdf, 'Survey Areas', 'polygon',
                    edgecolor='red', facecolor='none', linewidth=1)

                # 添加到图层控制
                self.layer_panel.add_layer('Survey Areas', 'polygon')

                # 缩放到图层范围
                self.map_viewer.zoom_to_layer(self.dcfq_gdf)

                self.statusbar.showMessage(f"已加载调查分区: {os.path.basename(path)}")
                self.has_unsaved_changes = True

            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载调查分区失败: {str(e)}")

    def load_zdqy_file(self):
        """加载重点区域文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择重点区域文件", "",
            "Shapefile (*.shp);;GeoJSON (*.geojson);;所有文件 (*)")

        if path:
            try:
                self.zdqy_gdf = gpd.read_file(path)

                # 检查坐标系
                if self.zdqy_gdf.crs is None:
                    if hasattr(self, 'dcfq_gdf'):
                        self.zdqy_gdf = self.zdqy_gdf.set_crs(self.dcfq_gdf.crs)
                    else:
                        reply = QMessageBox.question(
                            self, "坐标系缺失",
                            "重点区域文件缺少坐标系，是否设置为WGS84(EPSG:4326)?",
                            QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.zdqy_gdf = self.zdqy_gdf.set_crs("EPSG:4326")
                        else:
                            return

                # 修复几何错误
                self.zdqy_gdf.geometry = self.zdqy_gdf.geometry.make_valid()

                # 添加到地图
                self.map_viewer.add_layer(
                    self.zdqy_gdf, 'Key Areas', 'polygon',
                    edgecolor='orange', facecolor='none', linewidth=1)

                # 添加到图层控制
                self.layer_panel.add_layer('Key Areas', 'polygon')

                self.statusbar.showMessage(f"已加载重点区域: {os.path.basename(path)}")
                self.has_unsaved_changes = True

            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载重点区域失败: {str(e)}")

    def load_building_file(self):
        """加载建筑物文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择建筑物文件", "",
            "Shapefile (*.shp);;GeoJSON (*.geojson);;所有文件 (*)")

        if path:
            try:
                self.building_gdf = gpd.read_file(path)

                # 检查坐标系
                if self.building_gdf.crs is None:
                    if hasattr(self, 'dcfq_gdf'):
                        self.building_gdf = self.building_gdf.set_crs(self.dcfq_gdf.crs)
                    else:
                        reply = QMessageBox.question(
                            self, "坐标系缺失",
                            "建筑物文件缺少坐标系，是否设置为WGS84(EPSG:4326)?",
                            QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.building_gdf = self.building_gdf.set_crs("EPSG:4326")
                        else:
                            return

                # 修复几何错误
                self.building_gdf.geometry = self.building_gdf.geometry.make_valid()

                # 添加到地图
                self.map_viewer.add_layer(
                    self.building_gdf, 'Buildings', 'polygon',
                    edgecolor='black', facecolor='none', linewidth=1)

                # 添加到图层控制
                self.layer_panel.add_layer('Buildings', 'polygon')

                self.statusbar.showMessage(f"已加载建筑物: {os.path.basename(path)}")
                self.has_unsaved_changes = True

            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载建筑物失败: {str(e)}")

    # ======================== 核心功能 ========================
    def generate_grid(self, params=None):
        """生成网格"""
        if not hasattr(self, 'dcfq_gdf'):
            QMessageBox.warning(self, "警告", "请先加载调查分区数据")
            return

        try:
            if params is None:
                params = {
                    'grid_size': 20,
                    'random_offset': True,
                    'offset_x': 0,
                    'offset_y': 0
                }

            # 生成网格
            self.grid_gdf = self.planner.create_grid(
                self.dcfq_gdf,
                params['grid_size'],
                random_offset=params['random_offset'],
                offset_x=params['offset_x'],
                offset_y=params['offset_y']
            )

            # 添加到地图
            self.map_viewer.add_layer(
                self.grid_gdf, 'Grid', 'point',
                color='gray', markersize=3, alpha=0.7)

            # 添加到图层控制
            self.layer_panel.add_layer('Grid', 'point')

            # 绘制网格线
            self.map_viewer.draw_grid_lines(
                self.dcfq_gdf,
                grid_sizes=[params['grid_size']],
                color='lightgray', alpha=0.5)

            self.statusbar.showMessage(
                f"已生成网格: {len(self.grid_gdf)} 个点 (网格大小: {params['grid_size']}米)")
            self.has_unsaved_changes = True

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成网格失败: {str(e)}")

    def plan_boring(self, params=None):
        """规划钻孔点位"""
        if not hasattr(self, 'grid_gdf'):
            QMessageBox.warning(self, "警告", "请先生成网格")
            return

        try:
            if params is None:
                params = {
                    'boring_step': 2,
                    'boring_step_zdqy': 1,
                    'wboring_step': 8,
                    'wboring_step_zdqy': 4,
                    'offset_x': 0,
                    'offset_y': 0
                }

            # 获取重点区域数据
            zdqy_gdf = self.zdqy_gdf if hasattr(self, 'zdqy_gdf') else None

            # 规划钻孔
            self.boring_gdf = self.planner.plan_boring(
                self.grid_gdf,
                self.dcfq_gdf,
                zdqy_gdf,
                params
            )

            # 添加到地图
            self.map_viewer.add_layer(
                self.boring_gdf, 'Boring Points', 'point',
                color='green', markersize=6, alpha=1.0)

            # 添加到图层控制
            self.layer_panel.add_layer('Boring Points', 'point')

            # 统计钻孔数量
            boring_count = len(self.boring_gdf[self.boring_gdf['type'] == 'BORING'])
            wboring_count = len(self.boring_gdf[self.boring_gdf['type'] == 'WBORING'])

            self.statusbar.showMessage(
                f"规划完成: 普通钻孔 {boring_count} 个, 监测井 {wboring_count} 个")
            self.has_unsaved_changes = True

        except Exception as e:
            QMessageBox.critical(self, "错误", f"规划钻孔失败: {str(e)}")

    def avoid_buildings(self):
        """避让建筑物处理"""
        if not hasattr(self, 'building_gdf'):
            QMessageBox.warning(self, "警告", "请先加载建筑物数据")
            return

        if not hasattr(self, 'boring_gdf'):
            QMessageBox.warning(self, "警告", "请先规划钻孔点")
            return

        try:
            # 获取避让半径
            radius = self.tool_panel.spin_avoid_radius.value()

            # 执行避让
            self.boring_gdf = self.planner.avoid_buildings(
                self.boring_gdf,
                self.building_gdf,
                search_radius=radius
            )

            # 更新地图显示
            self.map_viewer.update_layer('Boring Points', self.boring_gdf)

            # 统计移动点数
            moved_count = len(self.boring_gdf[self.boring_gdf['moved'] == True])

            self.statusbar.showMessage(
                f"已完成建筑物避让，移动了 {moved_count} 个点 (避让半径: {radius}米)")
            self.has_unsaved_changes = True

        except Exception as e:
            QMessageBox.critical(self, "错误", f"避让建筑物失败: {str(e)}")

    # ======================== 其他方法 ========================
    def on_point_selected(self, point_id):
        """点选事件处理"""
        if hasattr(self, 'boring_gdf'):
            selected = self.boring_gdf[self.boring_gdf['id'] == point_id]
            if not selected.empty:
                self.attribute_table.current_layer_name = 'Boring Points'
                self.attribute_table.show_features(selected)

    def on_point_moved(self, point_id, new_x, new_y):
        """点移动事件处理"""
        if hasattr(self, 'boring_gdf'):
            idx = self.boring_gdf.index[self.boring_gdf['id'] == point_id]
            if len(idx) > 0:
                self.boring_gdf.at[idx[0], 'geometry'] = Point(new_x, new_y)
                self.boring_gdf.at[idx[0], 'moved'] = True
                self.has_unsaved_changes = True
                self.statusbar.showMessage(f"已移动点 {point_id} 到 ({new_x:.2f}, {new_y:.2f})")

    def on_attribute_changed(self, layer_name, field_name, new_value):
        """属性改变事件处理"""
        if hasattr(self, 'boring_gdf') and layer_name == 'Boring Points':
            idx = self.boring_gdf.index[self.boring_gdf['id'] == self.attribute_table.current_feature_id]
            if len(idx) > 0:
                self.boring_gdf.at[idx[0], field_name] = new_value
                self.has_unsaved_changes = True
                self.statusbar.showMessage(f"已更新点属性: {field_name} = {new_value}")

    def update_coord_display(self, x, y):
        """更新坐标显示"""
        self.coord_label.setText(f"坐标: {x:.2f}, {y:.2f}")

    def reset_view(self):
        """重置视图"""
        if hasattr(self, 'dcfq_gdf'):
            self.map_viewer.zoom_to_layer(self.dcfq_gdf)
        else:
            self.map_viewer.zoom_to_full()

    def check_unsaved_changes(self):
        """检查未保存的更改"""
        if self.has_unsaved_changes:
            reply = QMessageBox.question(
                self, "未保存的更改",
                "当前项目有未保存的更改，是否保存?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if reply == QMessageBox.Save:
                self.save_project()
                return True
            elif reply == QMessageBox.Discard:
                return True
            else:
                return False
        return True

    def reset_project(self):
        """重置项目"""
        self.map_viewer.clear()
        self.layer_panel.clear()
        self.attribute_table.clear()

        if hasattr(self, 'dcfq_gdf'):
            del self.dcfq_gdf
        if hasattr(self, 'zdqy_gdf'):
            del self.zdqy_gdf
        if hasattr(self, 'building_gdf'):
            del self.building_gdf
        if hasattr(self, 'grid_gdf'):
            del self.grid_gdf
        if hasattr(self, 'boring_gdf'):
            del self.boring_gdf

        self.current_project_path = None
        self.has_unsaved_changes = False
        self.setWindowTitle("钻孔布点规划系统 v3.0")
        self.statusbar.showMessage("已重置项目")

    def _save_project(self, path):
        """保存项目到文件"""
        # TODO: 实现项目保存逻辑
        self.has_unsaved_changes = False
        self.statusbar.showMessage(f"项目已保存: {path}")

    def load_project(self, path):
        """从文件加载项目"""
        # TODO: 实现项目加载逻辑
        self.current_project_path = path
        self.has_unsaved_changes = False
        self.setWindowTitle(f"钻孔布点规划系统 v3.0 - {os.path.basename(path)}")
        self.statusbar.showMessage(f"项目已加载: {path}")

    def optimize_points(self):
        """优化布点"""
        QMessageBox.information(self, "优化布点", "优化布点功能将在后续版本实现")

    def show_help(self):
        """显示帮助"""
        QMessageBox.information(self, "帮助", "钻孔布点规划系统使用说明")

    def show_about(self):
        """显示关于"""
        QMessageBox.about(self, "关于",
                          "钻孔布点规划系统 v3.0\n\n"
                          "基于PySide6和GeoPandas开发\n"
                          "© 2023 环境调查团队")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())