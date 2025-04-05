import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
from scipy.spatial import KDTree
import random
import math
import uuid


class BoringPlanner:
    def __init__(self):
        self.avoid_algorithm = 'uncertainty'  # 'random' or 'uncertainty'

    def create_grid(self, boundary_gdf, grid_size):
        """
        在边界内创建规则网格点
        :param boundary_gdf: 调查分区GeoDataFrame
        :param grid_size: 网格大小(米)
        :return: 网格点GeoDataFrame
        """
        # 获取边界范围
        minx, miny, maxx, maxy = boundary_gdf.total_bounds

        # 创建网格点
        x_coords = np.arange(minx, maxx, grid_size)
        y_coords = np.arange(miny, maxy, grid_size)

        points = []
        for x in x_coords:
            for y in y_coords:
                points.append(Point(x, y))

        # 创建GeoDataFrame
        grid_gdf = gpd.GeoDataFrame(geometry=points, crs=boundary_gdf.crs)

        # 只保留边界内的点
        grid_gdf = gpd.sjoin(grid_gdf, boundary_gdf, how='inner', op='within')

        # 添加行列号
        grid_gdf['row'] = ((grid_gdf.geometry.y - miny) / grid_size).astype(int)
        grid_gdf['col'] = ((grid_gdf.geometry.x - minx) / grid_size).astype(int)

        # 添加唯一ID
        grid_gdf['id'] = [str(uuid.uuid4()) for _ in range(len(grid_gdf))]

        return grid_gdf

    def random_offset(self, point, max_offset):
        """对点进行随机偏移"""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, max_offset)
        return Point(
            point.x + distance * math.cos(angle),
            point.y + distance * math.sin(angle)
        )

    def plan_boring(self, grid_gdf, dcfq_gdf, zdqy_gdf=None, params=None):
        """
        规划钻孔点位
        :param grid_gdf: 基础网格GeoDataFrame
        :param dcfq_gdf: 调查分区GeoDataFrame
        :param zdqy_gdf: 重点区域GeoDataFrame (可选)
        :param params: 规划参数字典
        :return: 钻孔点GeoDataFrame
        """
        if params is None:
            params = {}

        # 复制网格点
        boring_gdf = grid_gdf.copy()

        # 标记重点区域
        if zdqy_gdf is not None:
            boring_gdf['is_key_area'] = gpd.sjoin(
                boring_gdf, zdqy_gdf, how='left', op='within').index_right.notna()
        else:
            boring_gdf['is_key_area'] = False

        # 添加调查分区信息
        boring_gdf = gpd.sjoin(boring_gdf, dcfq_gdf[['DCFQ', 'geometry']], how='left', op='within')

        # 规划普通钻孔
        boring_gdf['is_boring'] = self._check_grid_condition(
            boring_gdf,
            params.get('offset_x', 0),
            params.get('offset_y', 0),
            params.get('boring_step', 2),
            params.get('boring_step_zdqy', 1)
        )

        # 规划监测井
        boring_gdf['is_wboring'] = self._check_grid_condition(
            boring_gdf,
            params.get('offset_x', 0),
            params.get('offset_y', 0),
            params.get('wboring_step', 8),
            params.get('wboring_step_zdqy', 4)
        )

        # 生成钻孔编号
        boring_points = []
        for zone in boring_gdf['DCFQ'].unique():
            zone_points = boring_gdf[boring_gdf['DCFQ'] == zone]

            # 普通钻孔
            zone_boring = zone_points[zone_points['is_boring']].copy()
            zone_boring['type'] = 'BORING'
            zone_boring['code'] = [f'S{i:04d}' for i in range(1, len(zone_boring) + 1)]

            # 监测井
            zone_wboring = zone_points[zone_points['is_wboring']].copy()
            zone_wboring['type'] = 'WBORING'
            zone_wboring['code'] = [f'W{i:04d}' for i in range(1, len(zone_wboring) + 1)]

            boring_points.extend([zone_boring, zone_wboring])

            # 合并结果
            result_gdf = gpd.GeoDataFrame(pd.concat(boring_points, ignore_index=True),
                                          crs=boring_gdf.crs)

            # 添加移动标记
            result_gdf['moved'] = False
            result_gdf['original_geom'] = result_gdf.geometry

        return result_gdf

    def avoid_buildings(self, points_gdf, buildings_gdf, search_radius=20.0):
        """
        避让建筑物处理
        :param points_gdf: 钻孔点GeoDataFrame
        :param buildings_gdf: 建筑物GeoDataFrame
        :param search_radius: 搜索半径(米)
        :return: 处理后的点GeoDataFrame
        """
        # 找出所有在建筑物内的点
        sjoin_result = gpd.sjoin(points_gdf, buildings_gdf, how='inner', op='within')
        points_to_move = points_gdf.loc[sjoin_result.index.unique()]

        if len(points_to_move) == 0:
            return points_gdf

        # 构建KDTree用于最近邻搜索
        valid_points = points_gdf[~points_gdf.index.isin(points_to_move.index)]
        if len(valid_points) > 0:
            coords = np.array([(p.x, p.y) for p in valid_points.geometry])
            kdtree = KDTree(coords)
        else:
            kdtree = None

        # 对每个需要移动的点进行处理
        for idx, row in points_to_move.iterrows():
            original_point = row.geometry
            building = buildings_gdf.loc[sjoin_result.loc[idx, 'index_right']].geometry

            # 找到建筑物边界上的最近点
            nearest_on_boundary = building.boundary.interpolate(
                building.boundary.project(original_point))

            # 计算移动方向
            if self.avoid_algorithm == 'uncertainty' and kdtree is not None:
                # 基于不确定性的移动方向
                new_point = self._move_by_uncertainty(
                    original_point, nearest_on_boundary, valid_points, kdtree, search_radius)
            else:
                # 随机移动
                new_point = self._move_randomly(original_point, nearest_on_boundary, search_radius)

            # 更新点位置
            points_gdf.at[idx, 'geometry'] = new_point
            points_gdf.at[idx, 'moved'] = True

        return points_gdf

    def _move_by_uncertainty(self, original_point, boundary_point, valid_points, kdtree, radius):
        """
        基于不确定性计算移动位置
        不确定性定义：距离已知点越远，不确定性越大
        """
        # 在搜索半径内找到所有已知点
        query_coords = np.array([[boundary_point.x, boundary_point.y]])
        indices = kdtree.query_ball_point(query_coords, r=radius)[0]

        if not indices:
            # 如果没有已知点，随机移动
            return self._move_randomly(original_point, boundary_point, radius)

        # 计算边界点周围的不确定性场
        sample_points = []
        for angle in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            dist = radius * 0.5  # 移动距离为半径的一半
            x = boundary_point.x + dist * np.cos(angle)
            y = boundary_point.y + dist * np.sin(angle)
            sample_points.append((x, y))

        # 评估每个候选点的不确定性
        uncertainties = []
        for x, y in sample_points:
            # 计算到所有已知点的距离
            distances = [Point(x, y).distance(Point(valid_points.iloc[i].geometry))
                         for i in indices]
            min_dist = min(distances) if distances else radius
            uncertainty = 1.0 - (min_dist / radius)  # 标准化到0-1
            uncertainties.append(uncertainty)

        # 选择不确定性最大的位置
        best_idx = np.argmax(uncertainties)
        return Point(sample_points[best_idx])

    def _move_randomly(self, original_point, boundary_point, radius):
        """随机移动点到建筑物外"""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius)
        new_x = boundary_point.x + distance * math.cos(angle)
        new_y = boundary_point.y + distance * math.sin(angle)
        return Point(new_x, new_y)

    def _check_grid_condition(self, gdf, offset_x, offset_y, step, step_zdqy):
        """
        检查网格点是否符合布点条件
        """
        conditions = []
        for _, row in gdf.iterrows():
            if row['is_key_area']:
                # 重点区域使用更密的步长
                cond = ((row['col'] - offset_x) % step_zdqy == 0 and
                        (row['row'] - offset_y) % step_zdqy == 0)
            else:
                # 普通区域使用正常步长
                cond = ((row['col'] - offset_x) % step == 0 and
                        (row['row'] - offset_y) % step == 0)
            conditions.append(cond)

        return pd.Series(conditions, index=gdf.index)