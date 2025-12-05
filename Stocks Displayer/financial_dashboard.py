import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import streamlit as st
from datetime import datetime, timedelta


#Uses Yahoo Finance API to get the data of the specific Ticker 
def get_data(ticker,start_date,end_date):
    df = yf.download(ticker,start=start_date,end=end_date)
    return df

#Finds the moving average 
def add_moving_average(df,window=20):
    #Gets the mean of the closing price over a rolling window
    df['MA'] = df["Close"].rolling(window=window).mean()
    return df


#Plots the graph
def plot_price(df, ticker, window):
    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Closing Price"
    ))
    #If MA exists 
    if "MA" in df.columns:
        #Plotting data
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["MA"],
            mode="lines",
            name=f"{window}-Day Moving Avg"
        ))

    #Adding labels 
    fig.update_layout(
        title=f"{ticker.upper()} Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )

    return fig


st.title("Financial Data Dashboard")


# Sidebar controls

#For choosing when the data should be 
max_date = datetime.today()
min_date = max_date - timedelta(days=365 * 5)  # Only allow last 5 years

ticker = st.sidebar.text_input("Ticker Symbol (e.g. AAPL)", value="AAPL")

start_date = st.sidebar.date_input(
    "Start Date",
    value=max_date - timedelta(days=180),
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=start_date,
    max_value=max_date
)

ma_window = st.sidebar.slider("Moving Avg Window", 5, 60, 20)

# Load data
# Prevent invalid date input 
if start_date > end_date:
    st.error("Start date must be earlier than end date.")
    st.stop()
    
with st.spinner("Loading stock data..."):
    df = get_data(ticker, start_date, end_date)

if df is not None and not df.empty:
    df = add_moving_average(df, window=ma_window)

    st.subheader("Recent Data")
    st.dataframe(df.tail(10))

    st.subheader("Stock Chart")
    st.plotly_chart(plot_price(df, ticker,ma_window), use_container_width=True)

    # Download button for wanting to download the data
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        "Download Data as CSV",
        csv,
        f"{ticker}_data.csv",
        "text/csv",
    )
else:
    st.error("No data available. Try a different ticker or date range.")


