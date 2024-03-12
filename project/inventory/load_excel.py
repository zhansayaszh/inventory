import psycopg2
import pandas as pd
from datetime import datetime

def load_excel(file):
  return pd.read_excel(file,dtype=str)

def agrofintech_clean(df):
    df = df.dropna(how='all')
    df = df[['ТОО "AgroFinTech"', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 6', 'Unnamed: 17']]
    df = df.iloc[4:]
    
    new_columns = {'ТОО "AgroFinTech"': 'name',
                'Unnamed: 2': 'date',
              'Unnamed: 3': 'item_idx',
              'Unnamed: 6': 'initial_price',
              'Unnamed: 17': 'residual_price'}

  # Rename the columns using the rename() method
    df.rename(columns=new_columns, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
    
    # Handle numeric columns
    numeric_columns = ['initial_price', 'residual_price']

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1)  # Replace NaN with 0
        
  # Separate DataFrame with non-NaN values in 'item_id'
    df_values = df[df['item_idx'].notna()][['name', 'item_idx','date','initial_price','residual_price']]

  # Add "BH" to all values in 'Column1'
    df_values['qr_id'] = 'AG' +df_values['item_idx']
    
    df_nan_values = df[df['item_idx'].isna()][['name', 'item_idx','date','initial_price','residual_price']]
    df_nan_values=df_nan_values[~df_nan_values['name'].isin(["Основное подразделение", "Итого"])]
    # df_values['company_id'] = 1
    
    return df_values,df_nan_values

def bass_holding_clean(df):
  # Remove rows with NaN values
  df = df.dropna(how='all')
#   df = df.iloc[:, :df.columns.get_loc('Unnamed: 2') + 1]
  df = df[['ТОО "BASS Holding"', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 16']]
    
  df = df.iloc[4:]

  new_columns = {'ТОО "BASS Holding"': 'name',
                'Unnamed: 2': 'item_idx',
                'Unnamed: 4':'initial_price',
                'Unnamed: 16':'residual_price'}

  # Rename the columns using the rename() method
  df.rename(columns=new_columns, inplace=True)
  #df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
  # Replace empty cells in 'residual_price' with None
  df['initial_price'] = df['initial_price'].apply(lambda x: x if pd.notna(x) and str(x).strip() != '' else None)
  # Replace empty cells in 'residual_price' with None
  df['residual_price'] = df['residual_price'].apply(lambda x: x if pd.notna(x) and str(x).strip() != '' else None)
  # Separate DataFrame with non-NaN values in 'item_id'
  df_values = df[df['item_idx'].notna()][['name', 'item_idx','initial_price','residual_price']]

  # Add "BH" to all values in 'Column1'
  df_values['qr_id'] = 'BH' +df_values['item_idx']
    
  df_nan_values = df[df['item_idx'].isna()][['name', 'item_idx','initial_price','residual_price']]

  group_names=['Земельные участки','Компьютеры','Мебель','Принтеры','Техника','Итого']
  # Delete rows where the value in column 1 is in the list of values to delete
  df_nan_values = df_nan_values[~df_nan_values['name'].isin(group_names)]

  return df_values,df_nan_values

def bass_gold_clean(df):
    df = df.dropna(how='all')
    df = df.iloc[5:]

    df = df[['ТОО "BASS Gold"', 'Unnamed: 9', 'Unnamed: 12', 'Unnamed: 19','Unnamed: 30']]
    new_columns = {'ТОО "BASS Gold"': 'name',
                'Unnamed: 9': 'item_idx',
                'Unnamed: 12': 'date',
              'Unnamed: 19': 'initial_price',
              'Unnamed: 30': 'residual_price'}

  # Rename the columns using the rename() method
    df.rename(columns=new_columns, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
    # Replace empty cells in 'residual_price' with None
    df['initial_price'] = df['initial_price'].apply(lambda x: x if pd.notna(x) and str(x).strip() != '' else None)
    # Replace empty cells in 'residual_price' with None
    df['residual_price'] = df['residual_price'].apply(lambda x: x if pd.notna(x) and str(x).strip() != '' else None)
    df=df.dropna(how='all')
    trash=['<...>','Итого','Руководитель:','Главный бухгалтер:','Ответственный:']
  # Delete rows where the value in column 1 is in the list of values to delete
    df = df[~df['name'].isin(trash)]
    df = df.dropna(how='all')
    #Indexing of df
    df.reset_index(drop=True, inplace=True)
    
    # Separate DataFrame with non-NaN values in 'item_id'
    df_values = df[df['item_idx'].notna()][['name', 'item_idx','date','initial_price','residual_price']]
  # Add "BH" to all values in 'Column1'
    df_values['qr_id'] = 'FP' +df_values['item_idx']
    #Indexing of df_values
    df_values.reset_index(drop=True, inplace=True)
    
    df_nan_values = df[df['item_idx'].isna()][['name', 'item_idx','date','initial_price','residual_price']]
    
    #Indexing of df_nan_values
    df_nan_values.reset_index(drop=True, inplace=True)
    
    return df_values,df_nan_values