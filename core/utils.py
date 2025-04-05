from PySide6.QtWidgets import QMessageBox
import geopandas as gpd

def show_message(title: str, text: str, icon=QMessageBox.Information):
    """显示消息对话框"""
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

def validate_data(file_path: str, require_crs: bool = False) -> bool:
    """验证数据文件是否有效"""
    try:
        gdf = gpd.read_file(file_path)
        if require_crs and gdf.crs is None:
            return False
        return True
    except:
        return False

def reproject_to_target_crs(gdf: gpd.GeoDataFrame, target_crs: str = "EPSG:4490") -> gpd.GeoDataFrame:
    """将数据重投影到目标坐标系"""
    if gdf.crs is None:
        raise ValueError("输入数据没有坐标系定义")
    return gdf.to_crs(target_crs)