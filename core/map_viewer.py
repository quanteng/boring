from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QMouseEvent
import geopandas as gpd
import numpy as np
import contextily as ctx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon as MplPolygon, Circle
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.lines import Line2D
from shapely.geometry import Point, Polygon, LineString


class MapViewer(FigureCanvas):
    point_selected_signal = Signal(str)
    point_moved_signal = Signal(str, float, float)

    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 8), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_axis_off()
        self.fig.tight_layout()

        # 图层管理
        self.layers = {}
        self.layer_order = []
        self.base_map = None

        # 编辑状态
        self.edit_mode = None  # 'select', 'move', 'delete'
        self.selected_point = None
        self.dragging = False

        # 连接事件
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('button_release_event', self.on_release)

    def add_layer(self, gdf, name, layer_type, **style):
        """
        添加图层到地图
        :param gdf: GeoDataFrame
        :param name: 图层名称
        :param layer_type: 'point', 'line' 或 'polygon'
        :param style: 样式参数
        """
        if gdf is None or gdf.empty:
            return

        # 移除同名旧图层
        # if name in self.layers:
        #     self.remove_layer(name)

        # 设置默认样式
        defaults = {
            'point': {'color': 'blue', 'markersize': 4, 'alpha': 1.0},
            'line': {'color': 'gray', 'linewidth': 0.5, 'alpha': 1.0},
            'polygon': {'edgecolor': 'black', 'facecolor': 'none', 'linewidth': 1.0, 'alpha': 1.0}
        }
        style = {**defaults.get(layer_type, {}), **style}

        try:
            # 根据图层类型创建不同的图形元素
            if layer_type == 'point':
                x = [p.x for p in gdf.geometry]
                y = [p.y for p in gdf.geometry]
                artist, = self.ax.plot(x, y, 'o', **style)
            elif layer_type == 'line':
                lines = []
                for geom in gdf.geometry:
                    if geom.geom_type == 'LineString':
                        lines.append(np.array(geom.coords)[:, :2])
                    elif geom.geom_type == 'MultiLineString':
                        for line in geom:
                            lines.append(np.array(line.coords)[:, :2])
                collection = LineCollection(lines, **style)
                artist = self.ax.add_collection(collection)
            elif layer_type == 'polygon':
                patches = []
                for geom in gdf.geometry:
                    if geom.geom_type == 'Polygon':
                        coords = np.array(geom.exterior.coords)[:, :2]
                        patches.append(MplPolygon(coords, closed=True))
                    elif geom.geom_type == 'MultiPolygon':
                        for poly in geom.geoms:
                            coords = np.array(poly.exterior.coords)[:, :2]
                            patches.append(MplPolygon(coords, closed=True))
                collection = PatchCollection(patches, **style)
                artist = self.ax.add_collection(collection)

            # 保存图层信息
            self.layers[name] = {
                'type': layer_type,
                'artist': artist,
                'gdf': gdf,
                'style': style
            }
            self.layer_order.append(name)

            # # 首次添加面图层时加载底图
            # if self.base_map is None and layer_type == 'polygon':
            #     self._refresh_basemap()
            #
            # self.draw()

        except Exception as e:
            print(f"添加图层 {name} 失败: {str(e)}")

    def remove_layer(self, name):
        """移除指定图层"""
        if name in self.layers:
            self.layers[name]['artist'].remove()
            del self.layers[name]
            if name in self.layer_order:
                self.layer_order.remove(name)
            self.draw()

    def update_layer(self, name, gdf):
        """更新图层数据"""
        if name in self.layers:
            layer_type = self.layers[name]['type']
            style = self.layers[name]['style']
            # self.remove_layer(name)
            self.add_layer(gdf, name, layer_type, **style)

    def update_layer_order(self, order):
        """更新图层顺序"""
        self.layer_order = order
        self._refresh_layers()

    def _refresh_layers(self):
        """根据图层顺序重新绘制所有图层"""
        # 移除所有图层
        for name in list(self.layers.keys()):
            self.layers[name]['artist'].remove()

        # 按新顺序重新添加
        for name in self.layer_order:
            if name in self.layers:
                layer = self.layers[name]
                self.add_layer(layer['gdf'], name, layer['type'], **layer['style'])

    def set_layer_visibility(self, name, visible):
        """设置图层可见性"""
        if name in self.layers:
            self.layers[name]['artist'].set_visible(visible)
            self.draw()

    def clear(self):
        """清除所有图层"""
        # for name in list(self.layers.keys()):
        #     self.remove_layer(name)
        self.layer_order = []
        self.base_map = None
        self.draw()

    def _refresh_basemap(self):
        """刷新底图"""
        if not self.layers:
            return

        # 获取第一个面图层的CRS
        for name in self.layer_order:
            if self.layers[name]['type'] == 'polygon':
                crs = self.layers[name]['gdf'].crs
                if crs is not None:
                    break
        else:
            crs = "EPSG:4326"

        try:
            # 移除旧底图
            if self.base_map is not None:
                self.base_map.remove()

            # 添加新底图
            self.base_map = ctx.add_basemap(
                self.ax,
                crs=crs.to_string() if hasattr(crs, 'to_string') else str(crs),
                source=ctx.providers.OpenStreetMap.Mapnik,
                zoom='auto'
            )
            self.draw()
        except Exception as e:
            print(f"无法加载底图: {str(e)}")

    def zoom_to_layer(self, gdf):
        """缩放到指定图层范围"""
        if gdf is not None and not gdf.empty:
            self.zoom_to_bounds(gdf.total_bounds)

    def zoom_to_layers(self, layers):
        """缩放到多个图层的合并范围"""
        if not layers:
            return

        bounds = None
        for layer in layers:
            if layer is not None and not layer.empty:
                if bounds is None:
                    bounds = layer.total_bounds
                else:
                    minx, miny, maxx, maxy = layer.total_bounds
                    bounds = [
                        min(bounds[0], minx),
                        min(bounds[1], miny),
                        max(bounds[2], maxx),
                        max(bounds[3], maxy)
                    ]

        if bounds is not None:
            self.zoom_to_bounds(bounds)

    def zoom_to_bounds(self, bounds):
        """缩放到指定范围"""
        if bounds is None or len(bounds) != 4:
            return

        # 计算带边界的范围
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        x_margin = width * 0.1
        y_margin = height * 0.1

        self.ax.set_xlim(bounds[0] - x_margin, bounds[2] + x_margin)
        self.ax.set_ylim(bounds[1] - y_margin, bounds[3] + y_margin)

        # 刷新底图
        self._refresh_basemap()
        self.draw()

    def zoom_in(self):
        """放大视图"""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        width = (xlim[1] - xlim[0]) * 0.7
        height = (ylim[1] - ylim[0]) * 0.7

        self.ax.set_xlim(x_center - width / 2, x_center + width / 2)
        self.ax.set_ylim(y_center - height / 2, y_center + height / 2)
        self.draw()

    def zoom_out(self):
        """缩小视图"""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        width = (xlim[1] - xlim[0]) / 0.7
        height = (ylim[1] - ylim[0]) / 0.7

        self.ax.set_xlim(x_center - width / 2, x_center + width / 2)
        self.ax.set_ylim(y_center - height / 2, y_center + height / 2)
        self.draw()

    def zoom_to_full(self):
        """缩放到全图"""
        if not self.layers:
            return

        # 计算所有图层的合并范围
        bounds = None
        for name in self.layer_order:
            if name in self.layers:
                gdf = self.layers[name]['gdf']
                if gdf is not None and not gdf.empty:
                    if bounds is None:
                        bounds = gdf.total_bounds
                    else:
                        minx, miny, maxx, maxy = gdf.total_bounds
                        bounds = [
                            min(bounds[0], minx),
                            min(bounds[1], miny),
                            max(bounds[2], maxx),
                            max(bounds[3], maxy)
                        ]

        if bounds is not None:
            self.zoom_to_bounds(bounds)

    def on_click(self, event):
        """鼠标点击事件处理"""
        if event.inaxes != self.ax:
            return

        if event.button == 1:  # 左键
            if self.edit_mode == 'select':
                self._handle_select(event)
            elif self.edit_mode == 'move':
                self._handle_start_drag(event)
            elif self.edit_mode == 'delete':
                self._handle_delete(event)

    def _handle_select(self, event):
        """处理选择操作"""
        for name in reversed(self.layer_order):  # 从最上层开始检查
            if name in self.layers and self.layers[name]['type'] == 'point':
                layer = self.layers[name]
                x_data = [p.x for p in layer['gdf'].geometry]
                y_data = [p.y for p in layer['gdf'].geometry]

                # 计算点到点击位置的距离
                distances = np.sqrt((np.array(x_data) - event.xdata) ** 2 +
                                    (np.array(y_data) - event.ydata) ** 2)
                min_idx = np.argmin(distances)

                # 如果距离足够近，则选择该点
                if distances[min_idx] < 0.02 * np.mean(self.ax.get_xlim()):
                    point_id = layer['gdf'].iloc[min_idx]['id']
                    self.selected_point = (name, min_idx)
                    self._highlight_point(name, min_idx)
                    self.point_selected_signal.emit(point_id)
                    self.draw()
                    break

    def _handle_start_drag(self, event):
        """开始拖动点"""
        if self.selected_point:
            layer_name, idx = self.selected_point
            point = self.layers[layer_name]['gdf'].iloc[idx].geometry
            if point.distance(Point(event.xdata, event.ydata)) < 0.02 * np.mean(self.ax.get_xlim()):
                self.dragging = True

    def _handle_delete(self, event):
        """处理删除操作"""
        for name in reversed(self.layer_order):
            if name in self.layers and self.layers[name]['type'] == 'point':
                layer = self.layers[name]
                x_data = [p.x for p in layer['gdf'].geometry]
                y_data = [p.y for p in layer['gdf'].geometry]

                distances = np.sqrt((np.array(x_data) - event.xdata) ** 2 +
                                    (np.array(y_data) - event.ydata) ** 2)
                min_idx = np.argmin(distances)

                if distances[min_idx] < 0.02 * np.mean(self.ax.get_xlim()):
                    # 从数据中删除点
                    layer['gdf'] = layer['gdf'].drop(layer['gdf'].index[min_idx])

                    # 重新绘制图层
                    self.update_layer(name, layer['gdf'])
                    self.draw()
                    break

    def on_motion(self, event):
        """鼠标移动事件处理"""
        if not event.inaxes or not self.dragging or not self.selected_point:
            return

        layer_name, idx = self.selected_point
        point_id = self.layers[layer_name]['gdf'].iloc[idx]['id']

        # 更新点位置
        self.layers[layer_name]['gdf'].at[
            self.layers[layer_name]['gdf'].index[idx], 'geometry'] = Point(event.xdata, event.ydata)

        # 发射信号
        self.point_moved_signal.emit(point_id, event.xdata, event.ydata)

        # 重新绘制图层
        self.update_layer(layer_name, self.layers[layer_name]['gdf'])

    def on_release(self, event):
        """鼠标释放事件处理"""
        self.dragging = False

    def _highlight_point(self, layer_name, idx):
        """高亮显示选中的点"""
        # 移除旧的高亮
        if 'highlight' in self.layers[layer_name]:
            self.layers[layer_name]['highlight'].remove()

        # 添加新高亮
        point = self.layers[layer_name]['gdf'].iloc[idx].geometry
        circle = Circle((point.x, point.y), 0.0002,
                        color='yellow', alpha=0.7, zorder=10)
        self.layers[layer_name]['highlight'] = self.ax.add_patch(circle)