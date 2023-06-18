from util import *


@add_sidebar
def algo_sidebar(data, col, label):
    return data[col].unique(), label


@add_sidebar1
def algo_sidebar1(data, col, label):
    return data[col].unique(), label


@add_sidebar_date
def date_sidebar(label, year, month, day):
    return label, year, month, day





@add_slider_pl
def add_slider(label, min_value, max_value, value):
    return label, min_value, max_value, value


@read_data
def get_data():
    return "Algo.csv"


@raise_error
def raise_date_error():
    return "Error: End date should be after the start date."


@raise_error
def raise_date_error1():
    return "Data not available on the selected date."


@write_dataframe
def write_data(data):
    return data

