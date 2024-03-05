import pandas as pd
import datetime as dt
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import glob
import os

def datetimer(df, col_name='datetime'):
    '''
    Turns the datetime column into a datetime object, a recurrent function for the project (if not specified, will assume
    'datetime' is the column to parse)
    '''
    df[col_name] = pd.to_datetime(df[col_name])
    
    return df

def iqr_filter_yearly(df, col_name):
    '''
    Filters a dataframe by the interquartile range of any given column, on a yearly basis. 
    '''

    # Ensure 'datetime' is in datetime format
    df = datetimer(df)

    # Create 'year' column
    df['year'] = df['datetime'].dt.year

    # Group by year, apply IQR filtering within each group
    filtered_df = df.groupby('year').apply(lambda group: iqr_filter(group, col_name))

    # Reset index
    filtered_df = filtered_df.reset_index(drop=True)

    return filtered_df


def iqr_filter(df, col_name):
    '''
    Filters a dataframe by the interquartile range of any given column. 
    '''
    q1, q3 = np.percentile(df[col_name], [25, 75])
    iqr = q3 - q1
    lfence = q1 - (1.5*iqr)
    hfence = q3 + (1.5*iqr)
    filtered_df = df[(df[col_name] >= lfence) & (df[col_name] <= hfence)]

    return filtered_df

class CyclicalDateTimeFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        # Assuming X is a DataFrame with a datetime column named 'datetime'
        X_transformed = X.copy()
        
        # Hour cyclical features
        X_transformed['hour_sin'] = np.sin(2 * np.pi * X_transformed['datetime'].dt.hour / 24)
        X_transformed['hour_cos'] = np.cos(2 * np.pi * X_transformed['datetime'].dt.hour / 24)
        
        # Day of month cyclical features
        # Adjust by using .max() for each month to handle different month lengths
        X_transformed['day_sin'] = np.sin(2 * np.pi * X_transformed['datetime'].dt.day / X_transformed['datetime'].dt.days_in_month)
        X_transformed['day_cos'] = np.cos(2 * np.pi * X_transformed['datetime'].dt.day / X_transformed['datetime'].dt.days_in_month)
        
        # Day of week cyclical features
        X_transformed['dayofweek_sin'] = np.sin(2 * np.pi * X_transformed['datetime'].dt.dayofweek / 7)
        X_transformed['dayofweek_cos'] = np.cos(2 * np.pi * X_transformed['datetime'].dt.dayofweek / 7)
        
        # Month cyclical features
        X_transformed['month_sin'] = np.sin(2 * np.pi * X_transformed['datetime'].dt.month / 12)
        X_transformed['month_cos'] = np.cos(2 * np.pi * X_transformed['datetime'].dt.month / 12)
        
        return X_transformed.drop('datetime', axis=1)


