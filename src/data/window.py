import pandas as pd
import numpy as np

def create_windows(df, window_size):
    """
    Create windowed data.
    """
    # Sort the dataframe by datetime
    df.sort_index(level='datetime', inplace=True)

    # List to hold the window data
    window_data = []

    # Group the data by plant
    for plant, data in df.groupby(level='plant'):
        # Create windows of specified size within each group
        for i in range(len(data) - window_size):
            temp = data.iloc[i: i + window_size + 1].copy()
            window_data.append(temp)
    
    return window_data

def create_windows_no_overlap(df, window_size):
    """
    Create non-overlapping windowed data.
    """
    # Sort the dataframe by date
    df.sort_values('datetime', inplace=True)

    # List to hold the window data
    window_data = []

    # Group the data by plant
    for plant, data in df.groupby('plant'):
        # Create windows of specified size within each group
        for i in range(0, len(data) - window_size, window_size):
            temp = data.iloc[i: i + window_size].copy()
            window_data.append(temp)
            
    return window_data
