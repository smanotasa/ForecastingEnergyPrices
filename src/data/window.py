import pandas as pd
import numpy as np
from tqdm import tqdm


def create_windows(df, window_size, overlap=True):
    """
    Create weekly windowed data.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    window_size (int): Size of each window in hours.
    overlap (bool): Whether the windows should overlap. Default is True.
    
    Returns:
    list: List of DataFrames, each representing a window.
    """
    # Check if 'datetime' is already the index
    original_index = df.index
    if df.index.name != 'datetime':
        # Convert datetime to pandas datetime if not already
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Set datetime as the index
        df.set_index('datetime', inplace=True)

    # Sort the dataframe by datetime
    df.sort_index(inplace=True)

    # List to hold the window data
    window_data = []

    # Get unique plant identifiers
    plants = df['plant'].unique()

    # Loop through each plant with a progress bar
    for plant in tqdm(plants, desc="Processing plants"):
        # Filter data for the current plant
        data = df[df['plant'] == plant]
        
        # Resample the data weekly
        weekly_groups = data.resample('W')

        # Iterate through each weekly group
        for _, weekly_data in weekly_groups:
            # Only process if the weekly data has enough observations
            if len(weekly_data) >= window_size:
                if overlap:
                    # Create overlapping windows
                    for i in range(0, len(weekly_data) - window_size + 1):
                        temp = weekly_data.iloc[i: i + window_size].copy()
                        temp.reset_index(inplace=True)  # Reset index to make 'datetime' a column again
                        window_data.append(temp)
                else:
                    # Create non-overlapping windows
                    for i in range(0, len(weekly_data) - window_size + 1, window_size):
                        temp = weekly_data.iloc[i: i + window_size].copy()
                        temp.reset_index(inplace=True)  # Reset index to make 'datetime' a column again
                        window_data.append(temp)

    # Restore the original index if it was not 'datetime'
    if df.index.name != 'datetime':
        df.reset_index(inplace=True)
        df.set_index(original_index, inplace=True)

    return window_data