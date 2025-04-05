import pyproj
from functools import lru_cache


class CoordinateSystem:
    def __init__(self):
        self.central_meridians = list(range(75, 136, 3))  # 中国三度分带中央经线

    @lru_cache(maxsize=24)
    def get_crs(self, central_meridian):
        """获取国家2000三度分带投影(带号自动计算)"""
        zone = (central_meridian + 1.5) // 3
        return pyproj.CRS.from_string(
            f"+proj=tmerc +lat_0=0 +lon_0={central_meridian} "
            f"+k=1 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs +type=crs"
        )

    def auto_detect_central_meridian(self, gdf):
        """自动检测最合适的中央经线"""
        bounds = gdf.total_bounds
        center_lon = (bounds[0] + bounds[2]) / 2
        # 找到最近的中央经线
        return min(self.central_meridians, key=lambda x: abs(x - center_lon))

    def transform_gdf(self, gdf, target_crs):
        """转换GeoDataFrame到目标坐标系"""
        if gdf.crs is None:
            raise ValueError("源数据缺少CRS定义")

        if not isinstance(target_crs, pyproj.CRS):
            target_crs = pyproj.CRS.from_user_input(target_crs)

        if gdf.crs == target_crs:
            return gdf.copy()

        transformer = pyproj.Transformer.from_crs(
            gdf.crs, target_crs, always_xy=True)

        # 转换几何图形
        gdf = gdf.copy()
        gdf.geometry = gdf.geometry.to_crs(target_crs)
        return gdf