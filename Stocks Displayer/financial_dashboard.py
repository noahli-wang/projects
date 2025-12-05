import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import streamlit as st
from datetime import datetime, timedelta

def get_data(ticker,start_date,end_date):
    df = yf.download(ticker,start=start_date,end=end_date)
    return df

def add_moving_average(df,window=20):
    df['MA'] = df["Close"].rolling(window=window).mean()
    return df

def plot_price(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name='Close'))
    if 'MA' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA'], name='Moving Avg'))
    fig.update_layout(title=f'{ticker} Price', xaxis_title='Date', yaxis_title='Price')
    return fig



st.title("📈 Financial Data Dashboard")


# Sidebar controls
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=datetime.today() - timedelta(days=180))
end_date = st.sidebar.date_input("End Date", value=datetime.today())
ma_window = st.sidebar.slider("Moving Avg Window", min_value=5, max_value=60, value=20)

# Load data
df = get_data(ticker, start_date, end_date)

if not df.empty:
    df = add_moving_average(df, window=ma_window)

    st.dataframe(df.tail(10))

    st.plotly_chart(plot_price(df, ticker))

    # (Bonus) Download data
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime='text/csv',
    )
else:
    st.write("No data found for the selected ticker and date range.")



