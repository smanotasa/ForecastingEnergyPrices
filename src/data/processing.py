import pandas as pd
import datetime as dt
import glob
import os


def process_files(data_path, output_path, sub_path, output_file, column_names, column_modifications=None):
    '''
    This function processes data spread out over multiple csv entries. It takes the necessary paths, an output path and optional
    modifications to be made to the resulting dataframe. It works by gathering all relevant file formats in a path and concatenating
    said observations increasingly over time.
    '''
    files = glob.glob(os.path.join(data_path, sub_path, '*.csv'))

    df = pd.concat((pd.read_csv(f, sep=';', header=0, decimal=',', names=column_names) for f in files), ignore_index=True)
    df['date'] = pd.to_datetime(df['date'])

    if column_modifications:
        for func in column_modifications:
            df = func(df)
    
    df = df.sort_values('date').reset_index(drop=True)
    df.to_csv(os.path.join(output_path, output_file), index=False)

    return df

def process_excel(data_path, sub_path, output_file, column_names, usecols, nrows=None, column_modifications=None):
    '''
    This function processes data spread out over multiple Excel entries. It takes the necessary paths, an output path and optional
    modifications to be made to the resulting dataframe. It works by gathering all relevant file formats in a path and concatenating
    said observations increasingly over time.
    '''
    files = glob.glob(os.path.join(data_path, sub_path, '*.xlsx'))

    df = pd.concat((pd.read_excel(f, header=0, decimal=',', usecols=usecols, nrows=nrows) for f in files), ignore_index=True)
    df = df.rename(columns=dict(zip(df.columns, column_names)))
    df['date'] = pd.to_datetime(df['date'])

    if column_modifications:
        for func in column_modifications:
            df = func(df)
    
    df = df.sort_values('date').reset_index(drop=True)

    return df

def modify_capacity(df):
    '''
    Given how the capacity dataframe is set-up from the information directory. We want to have all dataframes with the same electricity measurement
    unit. This function also uses a dictionary to translate the different technologies used by power plants into English.
    '''
    df['capacity_kW'] = df['capacity_MW']*1000
    df.drop('capacity_MW', axis=1, inplace=True)
    df = df.reset_index(drop=True)

    ctech_dict = {
        'Biomasa': 'Biomass',
        'Combustible Fósil': 'Thermal (Coal/Gas)',
        'Eólico': 'Wind',
        'Hidráulica': 'Hydro',
        'Solar': 'Solar'
    }
    df['technology'] = df['technology'].replace(ctech_dict)
    return df

def melt_dataframe(df, id_vars, var_name, value_name):
    '''
    This function melts dataframes with hourly observations into a single series. From the XM website, dataframes like spot-stock price, quantity
    demanded, quantity supplied are in its raw form following a day-to-day row configuration. Where each hourly value is presented as columns (i.e:
    columns for 0:00, 1:00,...,23:00). Essentially, if we have a dataframe for a year: 365 x 24 (dimension), this function melts it into 365*24 x 1.
    '''

    df_melted = df.melt(id_vars=id_vars, 
                        var_name=var_name, 
                        value_name=value_name)

    df_melted['date'] = pd.to_datetime(df_melted['date'])
    df_melted[var_name] = pd.to_timedelta(df_melted[var_name].astype(int), unit='h')

    df_melted['datetime'] = df_melted['date'] + df_melted[var_name]

    df_melted.drop(['date', var_name], axis=1, inplace=True)
    df_melted = df_melted.sort_values('datetime').reset_index(drop=True)

    return df_melted

def replace_plant_names(df):
    '''
    Since plant names change overtime this dictionary accounts for current denominations correcting outdated entries.
    '''
    plant_dict = {
        'TERMOSIERRAB': 'TERMOSIERRA CC',
        'TERMOVALLE 1': 'TERMOVALLE CC',
        'TERMOEMCALI 1': 'TERMOEMCALI CC',
        'FLORES 1': 'FLORES 1 CC',
        'TEBSAB': 'TEBSAB CC',
        'INGENIO PROVIDENCIA': 'INGENIO PROVIDENCIA 2',
        'PARQUE EÓLICO WESP01': 'PARQUE EOLICO WESP01',
        'EL EDÉN': 'EL EDEN',
        'ALEJANDRÍA': 'ALEJANDRIA',
        'DARIO VALENCIA': 'DARIO VALENCIA SAMPER',
        'CANTAYUS': 'AUTOG CANTAYUS',
        'PCH DE LA LIBERTAD': 'PCH LA LIBERTAD',
        'AMOYA': 'AMOYA LA ESPERANZA',
        'PETALO DE CORDOBA I': 'GY SOLAR AURORA',
 #       'FLORES 2': 'FLORES 4 CC',
 #       'FLORES 3': 'FLORES 4 CC',
        'FLORES 4B': 'FLORES 4 CC',
        'FLORES I CC': 'FLORES 1 CC',
        'COGENERADOR PROENCA II': 'COGENERADOR PROENCA 2',
        'COGENERADOR PROENCA 2': 'COGENERADOR PROENCA 2',
        'PROENCA II':'COGENERADOR PROENCA 2',
        'PROENCA 2':'COGENERADOR PROENCA 2',
        'COGENERADOR PROENCA 1':'COGENERADOR PROENCA 1',
        'PROENCA I':'COGENERADOR PROENCA 1',
        'PROENCA 1':'COGENERADOR PROENCA 1',
        'PROENCA':'COGENERADOR PROENCA 1',
        'COGENERADOR PROENCA': 'COGENERADOR PROENCA 1',
        'COGENERADOR PROENCA I':'COGENERADOR PROENCA 1',
        'FLORES I':'FLORES 1 CC',    
        }
    df['plant'] = df['plant'].replace(plant_dict)
    return df

def nan_filler(df):
    """
    This function replaces all NaN values in a DataFrame with zeros. We do this given empty information from XM
    means lack of.
    """
    return df.fillna(0)

def back_filler(df):
    return df.fillna(method='bfill')

def mcost_filler(df):
    '''
    From the source (Sinergox) some dates are missing their marginal cost values from 2011 to 2013. We have requested
    these to no avail. Thus, this function computes average marginal costs for that trimester, at that hour;
    since by regulatory law marginal costs are updated every three months, this is our best approach.
    '''
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    df = df.set_index('datetime')
    
    full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H')
    
    df = df.reindex(full_range)
    
    df['year-hour'] = df.index.year.astype(str) + '-' + df.index.hour.astype(str)
    
    mean_values = df.groupby('year-hour')['hourly_mc'].transform('mean')
    
    df['hourly_mc'] = df['hourly_mc'].fillna(mean_values)
    df = df.drop(columns = ['year-hour'])
    df['hourly_mc'] = df['hourly_mc'].fillna(method='ffill')
    df = df.rename(columns={'index': 'datetime'})
    df = df.reset_index(drop=False, names='datetime')

    return df
