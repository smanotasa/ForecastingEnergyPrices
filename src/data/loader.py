import pandas as pd

def load_soi():
    soi = pd.read_csv('/data/interim/soi.csv')
    soi['date'] = pd.to_datetime(soi['date'])
    return soi

def load_capacity():
    capacity = pd.read_csv('/data/interim/d_netcapacity.csv')
    capacity['total_capacity'] = capacity.groupby('date')['capacity_kW'].transform('sum')
    capacity['share'] = capacity['capacity_kW'] / capacity['total_capacity']
    return capacity

def load_askprice():
    askprice = pd.read_csv('/data/interim/d_supplyprice.csv')
    askprice['date'] = pd.to_datetime(askprice['date'])
    return askprice

def load_bidprice():
    bidprice = pd.read_csv('/data/interim/h_stockprice.csv')
    bidprice['datetime'] = pd.to_datetime(bidprice['datetime'])
    return bidprice

def load_resource():
    return pd.read_csv('/data/interim/resource.csv')

def load_demand():
    return pd.read_csv('/data/interim/h_demand.csv')

def load_supply():
    return pd.read_csv('/data/interim/h_supply.csv')

def load_price_fuel():
    return pd.read_csv('/data/interim/d_pricexfuel.csv')

def load_mcost():
    return pd.read_csv('/data/interim/h_marginalcost.csv')

def load_generation():
    return pd.read_csv('/data/interim/h_generation.csv')

def data_loader(*args):
    # Map dataframe names to loading functions
    loaders = {
        'soi': load_soi,
        'capacity': load_capacity,
        'askprice': load_askprice,
        'bidprice': load_bidprice,
        'resource': load_resource,
        'demand': load_demand,
        'supply': load_supply,
        'price_fuel': load_price_fuel,
        'mcost': load_mcost,
        'generation': load_generation
    }

    # If no arguments, load all dataframes
    if not args:
        return tuple(loader() for loader in loaders.values())

    # If there are arguments, only load those dataframes
    return tuple(loaders[arg]() for arg in args)
