
def create_datetime_column(df, year_col='year', month_col='month', day_col='day', hour_col='hour', year_prefix='20'):
    """
    Creates a datetime column from year, month, day, and hour columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        year_col (str): Name of the year column.
        month_col (str): Name of the month column.
        day_col (str): Name of the day column.
        hour_col (str): Name of the hour column.
        year_prefix (str): Prefix to add to the year (e.g., '20' for 20xx).

    Returns:
        pd.DataFrame: DataFrame with the new 'datetime' column added.
    """
    import pandas as pd
    import geopandas
    from shapely.geometry import Point
    try:
        df[year_col] = df[year_col].astype(str)
        df['year_full'] = year_prefix + df[year_col]
        df['year_full'] = df['year_full'].astype(int)
        df['year'] = df['year_full']

        df['datetime'] = pd.to_datetime(df[['year', month_col, day_col, hour_col]])
        df = df.drop(columns=['year_full'])
        return df
    except KeyError as e:
        print(f"Error: Column {e} not found in the DataFrame.")
        return df

def create_geodataframe(df, x_col='e', y_col='n', crs="EPSG:4326"):
    """
    Converts a DataFrame with coordinate columns to a GeoDataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing coordinate columns.
        x_col (str): Name of the column containing x-coordinates (e.g., longitude or Easting).
        y_col (str): Name of the column containing y-coordinates (e.g., latitude or Northing).
        crs (str): Coordinate Reference System to use (e.g., "EPSG:4326" for WGS 84).

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame with a 'geometry' column containing Point objects.
    """
    from shapely.geometry import Point, LineString
    import geopandas
    try:
        # 1. Create Point geometry from x and y columns
        geometry = [Point(xy) for xy in zip(df[x_col], df[y_col])]

        # 2. Create GeoDataFrame
        gdf = geopandas.GeoDataFrame(df, geometry=geometry, crs=crs)

        return gdf
    except KeyError as e:
        print(f"Error: Column {e} not found in the DataFrame: {e}")
        return None

def gdf_lines_and_stats_by_height(gdf, time_col='datetime', n_col='n', e_col='e'):
    """
    Creates LineStrings from Point geometries, grouped by height_code,
    calculates mean for selected columns, sum for rainfall,
    and extracts first time, n, e.

    Returns a GeoDataFrame with one row per height_code.
    """
    from shapely.geometry import Point, LineString
    import pandas as pd
    import geopandas
    try:
        mean_cols = ['pressure', 'air_temp', 'relhumid']

        def process_group(group):
            group = group.sort_values(by=time_col, ascending=False)

            line = LineString(group['geometry'].tolist())
            means = group[mean_cols].mean()
            rainfall_sum = group['rainfall'].sum()

            first_time = group[time_col].iloc[0]
            first_n = group[n_col].iloc[0]
            first_e = group[e_col].iloc[0]

            result = pd.Series(
                [line, first_time, first_n, first_e] + means.tolist() + [rainfall_sum],
                index=['geometry', 'datetime', 'n', 'e'] + mean_cols + ['rainfall'],
            )
            return result

        result_df = gdf.groupby('height_code').apply(process_group)

        line_gdf = geopandas.GeoDataFrame(result_df, geometry='geometry', crs=gdf.crs)
        line_gdf = line_gdf.reset_index()

        return line_gdf
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
    
def split_geodataframe_by_height_code(gdf):
    """
    Splits a GeoDataFrame into three GeoDataFrames based on 'height_code' values (1, 2, 3).

    Args:
        gdf (geopandas.GeoDataFrame): Input GeoDataFrame.

    Returns:
        tuple: A tuple of three GeoDataFrames (gdf_1, gdf_2, gdf_3). If a height_code is missing, its corresponding gdf will be None.
    """

    gdf_1 = gdf[gdf['height_code'] == 1].copy() if 1 in gdf['height_code'].values else None
    gdf_2 = gdf[gdf['height_code'] == 2].copy() if 2 in gdf['height_code'].values else None
    gdf_3 = gdf[gdf['height_code'] == 3].copy() if 3 in gdf['height_code'].values else None

    gdf_1 = gdf_1.reset_index(drop=True)
    gdf_2 = gdf_2.reset_index(drop=True)
    gdf_3 = gdf_3.reset_index(drop=True)
    return gdf_1, gdf_2, gdf_3
    