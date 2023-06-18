from functools import wraps
import pandas as pd
import datetime
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_option_menu import option_menu


def read_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        s = func(*args, **kwargs)
        df = pd.read_csv(s)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)  # , format="%d-%m-%Y")
        df["Date"] = df["Date"].dt.date
        df['ExitRate'].replace('nil', 0, inplace=True)
        df['ExitRate'] = df['ExitRate'].astype(float)
        #TODO Time into categoty
        df['EntryAt'] = pd.to_datetime(df['EntryAt'], format="%H.%M.%S")
        df['Time'] = df['EntryAt'].apply(lambda time: "09.00-11.00" if 9 <= time.hour <= 10
        else "11.00-01.00" if 11 <= time.hour <= 12
        else "01.00-03.00" if 13 <= time.hour <= 14 else "03.00-03.30")

        def calculate_gross_pl(row):
            if row['Signal'] == 'BUY':
                if row['Closure'] == 'SL':
                    return (row['SL'] - row['Rate']) * row['QTY']
                elif row['Closure'] == 'TGT':
                    return (row['TGT'] - row['Rate']) * row['QTY']
                elif row['Closure'] == 'EXIT':
                    return (row['ExitRate'] - row['Rate']) * row['QTY']
            elif row['Signal'] == 'SELL':
                if row['Closure'] == 'SL':
                    return (row['Rate'] - row['SL']) * row['QTY']
                elif row['Closure'] == 'TGT':
                    return (row['Rate'] - row['TGT']) * row['QTY']
                elif row['Closure'] == 'EXIT':
                    return (row['Rate'] - row['ExitRate']) * row['QTY']
            return 0

        df['Gross_PL'] = df.apply(calculate_gross_pl, axis=1)

        df['Result'] = np.where(df['Gross_PL'] >= 0, "Profit", "Loss")

        # creating columns for profit Amount & loss Amount
        df['P_Amount'] = np.where(df['Gross_PL'] >= 0, df['Gross_PL'], 0)
        df['L_Amount'] = np.where(df['Gross_PL'] < 0, df['Gross_PL'], 0)

        df['Closure1'] = np.where((df['Closure'] == 'TGT'), 'TGT',
                                  np.where((df['Closure'] == 'SL') & (df['Gross_PL'] >= 0), 'TSL',
                                           np.where((df['Closure'] == 'SL') & (df['Gross_PL'] < 0), 'SL',
                                                    np.where((df['Closure'] == 'EXIT') & (df['Gross_PL'] > 0),
                                                             'EXIT PROFIT',
                                                             'EXIT LOSS'))))

        PL = df['Gross_PL'].unique().tolist()
        return df

    return wrapper


def add_slider_pl(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Algo Number:
        label, min_value, max_value, value = func(*args, **kwargs)
        df_algo = st.slider(label, min_value, max_value, value)
        return df_algo

    return wrapper


def add_sidebar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Algo Number:
        options, label = func(*args, **kwargs)
        df_algo = st.sidebar.selectbox(options=options,
                                       label=label)
        return df_algo

    return wrapper


def add_sidebar1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Algo Number:
        options, label = func(*args, **kwargs)
        df_algo = st.multiselect(options=options,
                                         label=label)
        return df_algo

    return wrapper





def add_sidebar_date(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Algo Number:
        label, year, month, day = func(*args, **kwargs)
        df_algo = st.sidebar.date_input(label, datetime.date(year, month, day))
        return df_algo

    return wrapper


def raise_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        msg = func(*args, **kwargs)
        st.error(msg)
        return msg

    return wrapper


def write_dataframe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        st.write(df)
        return df

    return wrapper

