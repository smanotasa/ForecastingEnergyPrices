import pandas as pd
import numpy as np

def calculate_rsi(df):
    """
    This function calculates the Residual Supply Index (RSI) for each agent at each timestamp.
    RSI is calculated as (Total Supply - Agent's Supply) / Total Demand.
    """
    # Calculate total supply by each agent
    total_supply_by_agent = df.groupby(['agent_code', 'datetime'])['supply_hourly'].sum().reset_index()
    total_supply_by_agent.rename(columns={'supply_hourly': 'total_supply_agent'}, inplace=True)

    total_supply_at_time = df.groupby(['datetime'])['supply_hourly'].sum().reset_index()
    total_supply_at_time.rename(columns={'supply_hourly': 'total_supply_t'}, inplace=True)


    # Merge this back to the df
    df = pd.merge(df, total_supply_by_agent, on=['agent_code', 'datetime'], how='left')
    df = pd.merge(df, total_supply_at_time, on=['datetime'], how='left')


    # Calculate the residual supply
    df['residual_supply'] = df['total_supply_t'] - df['total_supply_agent']

    # Calculate the RSI
    df['rsi_agent'] = df['residual_supply'] / df['demand_hourly']

    # Calculate market share for each agent
    df['market_share_agent'] = df['total_supply_agent'] / df['total_supply_t']
    df['market_share_agent'] = df['market_share_agent'].fillna(0)

    return df

def calculate_lerner(df):
    """
    This function calculates the markup (Price - Marginal Cost) and the 
    Lerner Index (Markup / Price) for each row in the dataframe. It calculates 2 versions for each, one assuming
    competitive pricing where P = MC, using the demand price; and one using the actual MC reported.
    """
    df['markup'] = df['daily_ask'] - df['hourly_mc']
    df['lerner'] = df['markup'] / df['daily_ask']

    df['comp_markup'] = df['daily_ask'] - df['hourly_bid']
    df['comp_lerner'] = df['comp_markup'] / df['daily_ask']

    df['comp_lerner'] = df['comp_lerner'].fillna(0)   
    df['lerner'] = df['lerner'].fillna(0)

    df['lerner'].replace([np.inf, -np.inf], 0, inplace=True)
    df['comp_lerner'].replace([np.inf, -np.inf], 0, inplace=True)
    return df
