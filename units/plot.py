import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import calendar

def plot_trajectories_all_months(gdf, month_column='month', year=2014):
    cmap = plt.get_cmap("tab20")
    month_colors = {month: cmap((month - 1) % 20) for month in range(1, 13)}

    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Mở rộng phạm vi hiển thị bản đồ
    ax.set_extent([30, 180, -20, 65], crs=ccrs.PlateCarree())

    # Vẽ các đường
    available_months = sorted(gdf[month_column].dropna().unique())
    for month in available_months:
        sub_gdf = gdf[gdf[month_column] == month]
        for geom in sub_gdf.geometry:
            ax.plot(*geom.xy, color=month_colors.get(month, 'gray'),
                    linewidth=0.5, alpha=0.3, transform=ccrs.PlateCarree())

    # Vẽ bản đồ
    ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=0)
    ax.add_feature(cfeature.OCEAN, facecolor='white', zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Ghi chú tên tháng – tăng fontsize và đẩy lên chút
    for i, month in enumerate(available_months):
        ax.text(42 + i * 10, 67, calendar.month_abbr[month].upper(),  # đổi từ 63 lên 67
                color=month_colors[month], fontsize=12, fontweight='bold')

    # Ghi chú năm – to hơn và canh sát góc hơn
    ax.text(167, 67, str(year), fontsize=14, fontweight='bold')

    # Điều chỉnh khoảng trắng khung
    plt.subplots_adjust(left=0.03, right=0.98, top=0.95, bottom=0.08)
    plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation_matrix(df, columns=None, exponent=3.5, save_path=None):
    """
    Vẽ ma trận tương quan dạng scatter tam giác dưới, với cỡ điểm phi tuyến theo giá trị tương quan.
    
    Parameters:
        df (pd.DataFrame): Dữ liệu đầu vào
        columns (list or None): Danh sách cột để tính tương quan (mặc định: từ cột thứ 2 trở đi)
        exponent (float): Số mũ để điều chỉnh kích thước điểm
        save_path (str or None): Đường dẫn để lưu ảnh, nếu None thì không lưu
    """
    if columns is None:
        data = df.iloc[:, 1:-3]
    else:
        data = df[columns]
    
    corr_matrix = data.corr()
    corr_matrix = np.floor(corr_matrix * 100) / 100  # làm tròn về 2 chữ số

    # Tạo mask tam giác trên
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    melt = corr_matrix.mask(mask).melt(ignore_index=False).reset_index()

    # Hàm ánh xạ kích thước
    def nonlinear_size_mapping(value):
        if pd.isna(value):
            return 0
        abs_val = abs(value)
        return (abs_val ** exponent) * 1000

    melt["size"] = melt["value"].apply(nonlinear_size_mapping)

    # Setup plot
    fig, ax = plt.subplots(figsize=(14, 8))
    cmap = plt.cm.RdBu_r
    norm = plt.Normalize(-1, 1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.ax.tick_params(labelsize="small")

    # Scatterplot
    sns.scatterplot(ax=ax, data=melt, x="index", y="variable", size="size",
                    hue="value", hue_norm=norm, palette=cmap,
                    style=0, markers=["o"], legend=False, sizes=(40, 400))

    # Grid lines
    xmin, xmax = (-0.5, corr_matrix.shape[0] - 0.5)
    ymin, ymax = (-0.5, corr_matrix.shape[1] - 0.5)
    ax.vlines(np.arange(xmin, xmax + 1), ymin, ymax, lw=0.5, color="lightgray")
    ax.hlines(np.arange(ymin, ymax + 1), xmin, xmax, lw=0.5, color="lightgray")
    ax.set(aspect='auto', xlim=(xmin, xmax), ylim=(ymax, ymin), xlabel="", ylabel="")
    # Lấy tên biến để đặt tick
    labels = corr_matrix.columns.tolist()
    positions = np.arange(len(labels))

    # Set xticks ở giữa mỗi ô
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=10, ha='center', rotation=30)
    ax.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)

    # Annotate
    columns = corr_matrix.columns.tolist()
    for y in range(corr_matrix.shape[0]):
        for x in range(corr_matrix.shape[1]):
            if x == y:
                plt.text(x, y, columns[x], size="medium", ha="center", va="center", fontweight="bold")
            else:
                value = corr_matrix.mask(mask).to_numpy()[y, x]
                if pd.notna(value):
                    text_color = "black"
                    fontweight = "normal"
                    if abs(value) > 0.85:
                        fontweight = "bold"
                    plt.text(x, y, f"{value:.2f}", size="small",
                             ha="center", va="center", color=text_color, fontweight=fontweight)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=600)
    plt.show()
