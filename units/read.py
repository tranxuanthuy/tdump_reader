import pandas as pd
import io

def read_data_from_file_like(file_like, columns_name=None):
    """
    Reads data from a file-like object (e.g., a file or a string)
    starting from the line containing "PRESSURE AIR_TEMP RAINFALL RELHUMID".

    Args:
        file_like: A file-like object (e.g., an opened file or a StringIO object).
        columns_name: An optional list of column names to use for the DataFrame.
                      If None, pandas will infer column names from the data.

    Returns:
        pandas.DataFrame: A DataFrame containing the parsed data, or None if the
                          starting line is not found.
    """

    data_lines = file_like.readlines()
    start_index = -1

    for i, line in enumerate(data_lines):
        if "PRESSURE" in line:
            start_index = i + 1  # Start reading from the line after this header
            break

    if start_index == -1:
        print("Error: 'PRESSURE AIR_TEMP RAINFALL RELHUMID' line not found.")
        return None
    
    # delete line contain error value
    correct_lines = []
    for line in data_lines[start_index:]:
        if '\x00' in line:
            continue
        else:
            correct_lines.append(line)

    data_to_parse = "".join(correct_lines)

    # Use io.StringIO to treat the string as a file
    data_io = io.StringIO(data_to_parse)

    try:
        df = pd.read_csv(data_io, delim_whitespace=True, names=columns_name) # Add names parameter
        return df
    except pd.errors.EmptyDataError:
        print("Error: No data to parse after the header line.")
        return None
    
def select_desired_columns(
        df,
        desired_cols = ['height_code', 'datetime', 'time_step', 'n', 'e', 'height', 'pressure', 'air_temp', 'rainfall', 'relhumid']
        ):
    """Selects and reorders the desired columns."""
    
    try:
        return df[desired_cols]
    except KeyError as e:
        print(f"Error: Column {e} not found.")
        return None