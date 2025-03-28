import pandas as pd

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
