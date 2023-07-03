import al2
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


def start_app():
    df = al2.get_data()
    st.markdown("<h2 style='text-align: center; color: Blue;'>MAV_Algo Performance</h2>", unsafe_allow_html=True)
    algo_name = al2.algo_sidebar(df, "AlgoName", "Select AlgoName")
    algo_filter = df['AlgoName'] == algo_name
    df = df[algo_filter].copy()
    start_date = al2.date_sidebar("Start date", 2023, 1, 1)
    end_date = al2.date_sidebar("End date", 2023, 7, 31)
    col1, col2, col3=st.columns(3)
    with col1:
        Signal = al2.algo_sidebar1(df, "Signal", "Select Signal")
    with col2:
        Time = al2.algo_sidebar1(df, "Time", "Select Entry Time")
    with col3:
        PL = df['Rate'].unique().tolist()
        df_rate = al2.add_slider('select range of Rate',
                                    min(PL, default=0),
                                    max(PL, default=0),
                                    (min(PL, default=0), max(PL, default=0)))

    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{:.1f}%\n({v:d})'.format(pct, v=val)

        return my_format

    def convert_df(df):
        return df.to_csv().encode('utf-8')

    def add_plot():
        counts = df['Result'].value_counts()
        fig = plt.figure(figsize=(4, 4))
        colors = {'Loss': 'red',
                  'Profit': 'green'
                  }
        plt.pie(counts.values, labels=counts.index, autopct=autopct_format(counts), textprops={'fontsize': 10},
                colors=[colors[key] for key in counts.index])

        st.pyplot(fig)

    def add_plot1():

        counts = df['Closure1'].value_counts()
        fig1 = plt.figure(figsize=(14, 14))
        colors = {'EXIT LOSS': 'red',
                  'EXIT PROFIT': 'green',
                  'SL': 'red',
                  'TGT': 'green',
                  'TSL': 'green'}
        plt.pie(counts.values, labels=counts.index, autopct=autopct_format(counts), textprops={'fontsize': 24},
                wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, colors=[colors[key] for key in counts.index])

        st.pyplot(fig1)

    def plot_pl():
        PL = df.groupby("Date")[['P_Amount', 'L_Amount', 'Gross_PL']].sum().reset_index()
        fig = px.line(PL, x='Date', y=['P_Amount', 'L_Amount', 'Gross_PL'],
                      color_discrete_map={"Gross_PL": "blue", "P_Amount": "green", "L_Amount": "red"})
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    def button():
        csv = convert_df(t)
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='PL_count.csv',
            mime='text/csv',
        )

    def button1():
        csv = convert_df(t)
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='Closure_count.csv',
            mime='text/csv',
        )

    def button2():
        csv = convert_df(t)
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='Gross_PL.csv',
            mime='text/csv',
        )

    def dataframe():
        al2.write_data(t.round(2))

    #st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Count</h6>", unsafe_allow_html=True)

    #col1, col2 = st.columns(2)

    if end_date < start_date:
        al2.raise_date_error()

    elif df.shape[0] == 0:
        al2.raise_date_error1()


    elif algo_name and Signal and Time:
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Count based on Signal & Time</h6>",
                    unsafe_allow_html=True)

        filter = (df['AlgoName'] == algo_name) & (df['Signal'].isin(Signal)) & (df['Time'].isin(Time)) & (
            df['Rate'].between(*df_rate))
        df = df[filter]
        col1, col2 = st.columns(2)
        with col1:

            add_plot()
            t = df.groupby(['Date', 'Signal', 'Time', 'Result'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button()
        with col2:

            add_plot1()
            t = df.groupby(['Date', 'Signal', 'Time', 'Closure1'])['Gross_PL'].agg(Count='count', Total='sum')
                # dataframe()
            button1()
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Amount based on Signal & Time</h6>",
                    unsafe_allow_html=True)
        plot_pl()
        t = df.groupby(['Date', 'Signal', 'Time'])[['P_Amount', 'L_Amount', 'Gross_PL']].agg(
            {'P_Amount': ['sum'], 'L_Amount': ['sum'], 'Gross_PL': ['count', 'sum']})
        # dataframe()
        button2()

    elif algo_name and Signal:
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Count based on Signal</h6>",
                    unsafe_allow_html=True)
        filter = (df['AlgoName'] == algo_name) & (df['Signal'].isin(Signal)) & (df['Rate'].between(*df_rate))
        df = df[filter]
        col1, col2 = st.columns(2)
        with col1:

            add_plot()
            t = df.groupby(['Date', 'Signal', 'Result'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button()
        with col2:

            add_plot1()
            t = df.groupby(['Date', 'Signal', 'Closure1'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button1()

        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Amount based on Signal</h6>",
                    unsafe_allow_html=True)
        plot_pl()
        t = df.groupby(['Date', 'Signal'])[['P_Amount', 'L_Amount', 'Gross_PL']].agg(
            {'P_Amount': ['sum'], 'L_Amount': ['sum'], 'Gross_PL': ['count', 'sum']})
        # dataframe()
        button2()

    elif algo_name and Time:
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Count based on Time</h6>",
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        filter = (df['AlgoName'] == algo_name) & (df['Time'].isin(Time)) & (df['Rate'].between(*df_rate))
        df = df[filter]
        with col1:
            add_plot()
            t = df.groupby(['Date', 'Time', 'Result'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button()
        with col2:
            add_plot1()
            t = df.groupby(['Date', 'Time', 'Closure1'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button1()
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Amount based on Time</h6>",
                    unsafe_allow_html=True)
        plot_pl()
        t = df.groupby(['Date', 'Time'])[['P_Amount', 'L_Amount', 'Gross_PL']].agg(
            {'P_Amount': ['sum'], 'L_Amount': ['sum'], 'Gross_PL': ['count', 'sum']})
        # dataframe()
        button2()

    elif algo_name:
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Count</h6>",
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        filter = (df['AlgoName'] == algo_name) & (df['Rate'].between(*df_rate))
        df = df[filter]
        with col1:
            #st.title("Profit Loss Count")
            add_plot()
            t = df.groupby(['Date', 'Result'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button()
        with col2:
            #st.subheader("")
            add_plot1()
            t = df.groupby(['Date', 'Closure1'])['Gross_PL'].agg(Count='count', Total='sum')
            # dataframe()
            button1()
        st.markdown("<h6 style='text-align: left; color: Black;'>Profit Loss Amount</h6>",
                    unsafe_allow_html=True)
        plot_pl()
        t = df.groupby(['Date'])[['P_Amount', 'L_Amount', 'Gross_PL']].agg(
            {'P_Amount': ['sum'], 'L_Amount': ['sum'], 'Gross_PL': ['count', 'sum']})
        #dataframe()
        button2()


if __name__ == "__main__":
    start_app()
