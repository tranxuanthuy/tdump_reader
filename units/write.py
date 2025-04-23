import pandas as pd
import geopandas as gpd
import os

def write_output(df1, df2, df3, folder_path='O:/Tran Xuan Thuy/iWAT/hysplit/processed_excel'):
    def format_datetime_for_filename(dt):
        return dt.strftime('%Y-%m-%d_%H')

    # Lấy thời gian từ cột datetime và chuẩn hóa định dạng
    dt1 = format_datetime_for_filename(pd.to_datetime(df1['datetime'].iloc[0]))
    dt2 = format_datetime_for_filename(pd.to_datetime(df2['datetime'].iloc[0]))
    dt3 = format_datetime_for_filename(pd.to_datetime(df3['datetime'].iloc[0]))

    # Tạo đường dẫn file
    file1 = f"{folder_path}/{dt1}_1.xlsx"
    file2 = f"{folder_path}/{dt2}_2.xlsx"
    file3 = f"{folder_path}/{dt3}_3.xlsx"

    # Ghi ra file Excel
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)
    df3.to_excel(file3, index=False)



def write_output_gdf(year, month, day, hour, gdf1, gdf2, gdf3, folder_path='O:/Tran Xuan Thuy/iWAT/hysplit/processed_geojson'):
    """
    Writes three GeoDataFrames to GeoJSON files.

    Args:
        gdf1 (gpd.GeoDataFrame): The first GeoDataFrame.
        gdf2 (gpd.GeoDataFrame): The second GeoDataFrame.
        gdf3 (gpd.GeoDataFrame): The third GeoDataFrame.
        folder_path (str): The folder path to save the GeoJSON files.
    """
    os.makedirs(folder_path, exist_ok=True)

    def format_datetime_for_filename(year, month, day, hour):
        return f"{year:04d}-{month:02d}-{day:02d}-{hour:02d}"


    def write_gdf_to_geojson_single(gdf, filepath):
        try:
            gdf.to_file(filepath, driver='GeoJSON')
            return 1
        except Exception as e:
            print(f"Error writing GeoDataFrame to GeoJSON: {e}")

    # thêm biến thời gian để ghi tên file
    dt = format_datetime_for_filename(year, month, day, hour)
    if 'datetime' in gdf1.columns:
        file1_timed = f"{folder_path}/{dt}_1.geojson"
        result_gdf1 = write_gdf_to_geojson_single(gdf1, file1_timed)

    if 'datetime' in gdf2.columns:
        file2_timed = f"{folder_path}/{dt}_2.geojson"
        result_gdf2 = write_gdf_to_geojson_single(gdf2, file2_timed)

    if 'datetime' in gdf3.columns:
        file3_timed = f"{folder_path}/{dt}_3.geojson"
        result_gdf3 = write_gdf_to_geojson_single(gdf3, file3_timed)
    # nếu không ghi đủ 3 file -> in thời gian
    if result_gdf1 + result_gdf2 + result_gdf3 != 3:
        print(year, month, day, hour)
