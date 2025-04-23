from shapely.geometry import LineString
import pandas as pd
import geopandas as gpd
import os
from tqdm import tqdm

def collapse_gdf_to_linestring(gdf, mean_cols, sum_cols, geometry_col='geometry'):
    gdf = gdf.sort_values('time_step', ascending=False)  # đảm bảo đúng thứ tự thời gian

    # 1. Tạo LineString từ danh sách Point
    line = LineString(gdf[geometry_col].values)

    # 2. Tính trung bình và tổng cho từng nhóm cột
    result_data = {}

    for col in mean_cols:
        result_data[col] = gdf[col].mean(skipna=True)

    for col in sum_cols:
        result_data[col] = gdf[col].sum(skipna=True)

    # 3. Gộp thành một dòng GeoDataFrame
    result = pd.DataFrame([result_data])
    result['geometry'] = line

    return gpd.GeoDataFrame(result, geometry='geometry')


def merge_gdf(folder,\
        mean_cols = ['height', 'pressure',
       'theta', 'air_temp', 'rainfall', 'mixdepth', 'relhumid', 'spchumid',
       'h2omixra'],
        sum_cols = ['rainfall', 'terr_msl', 'sun_flux']):
    files = os.listdir(folder)
    all_linestring_gdfs = []
    for file in tqdm(files):
        # read file
        gdf = gpd.read_file(os.path.join(folder, file))\
        # cal mean
        gdf_linestring = collapse_gdf_to_linestring(gdf, mean_cols, sum_cols)
        # cal length
        gdf_linestring['length'] = gdf_linestring.geometry.length
        # set crs
        gdf_linestring.crs = gdf.crs
        # add datetime column
        gdf_linestring['datetime'] = pd.to_datetime(file.split('_')[0], format='%Y-%m-%d-%H')
        # add height_code
        gdf_linestring['heigh_code'] = int(file.split('_')[1].split('.')[0])
        # append to linestring_gdfs list
        all_linestring_gdfs.append(gdf_linestring)
    if all_linestring_gdfs:  # Check if we have any GeoDataFrames to combine
        if len(all_linestring_gdfs) > 1:
            try:
                # Concatenate all GeoDataFrames using pd.concat
                combined_gdf = gpd.GeoDataFrame(
                    pd.concat(all_linestring_gdfs, ignore_index=True), crs=all_linestring_gdfs[0].crs
                )
                return combined_gdf
            except ValueError as e:
                print(f"Error concatenating GeoDataFrames: {e}")
                return None
        else:
            return all_linestring_gdfs[0] # Return the first gdf if only one file proceeded correctly.
    else:
        print("No GeoDataFrames were successfully processed.")
        return None

