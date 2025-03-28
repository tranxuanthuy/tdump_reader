import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_trajectories_by_month(gdf, month_column='month', year=2014):
    # Thiết lập màu cho từng tháng
    month_colors = {
        6: 'dodgerblue',   # June
        7: 'limegreen',    # July
        8: 'orangered',    # August
        9: 'gold'          # September
    }

    # Khởi tạo bản đồ
    fig = plt.figure(figsize=(9, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([40, 180, -10, 60], crs=ccrs.PlateCarree())

    # Thêm bản đồ cơ bản
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Vẽ các đường theo tháng
    for month in sorted(gdf[month_column].unique()):
        sub_gdf = gdf[gdf[month_column] == month]
        sub_gdf.plot(ax=ax, color=month_colors.get(month, 'gray'), linewidth=0.8, alpha=0.7)

    # Chú thích tháng và năm
    ax.text(43, 63, 'JUN', color='dodgerblue', fontsize=12, fontweight='bold')
    ax.text(65, 63, 'JUL', color='limegreen', fontsize=12, fontweight='bold')
    ax.text(90, 63, 'AUG', color='orangered', fontsize=12, fontweight='bold')
    ax.text(120, 63, 'SEP', color='gold', fontsize=12, fontweight='bold')
    ax.text(150, 63, str(year), fontsize=12, fontweight='bold')

    plt.title("Trajectories by Month", fontsize=14)
    plt.tight_layout()
    plt.show()
