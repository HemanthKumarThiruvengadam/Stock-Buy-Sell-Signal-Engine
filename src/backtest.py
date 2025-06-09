import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
def display_back_testing(data):
    fig4 = plt.figure(figsize = (12,6))
    plt.plot(data.index,data['Portfolio_Value'],label = "Portfolio_Value",color = "red")
    plt.title("Portfolio_Value Vs Date")
    plt.xlabel("Date")
    plt.ylabel("Portfolio_Value")
    plt.legend()
    plt.grid(True)
    st.pyplot(fig4)
def back_testing(data):
    st.write("Back_Testing The Signals")
    st.write("Initial Amount: 10000")
    Portfolio_Value = []
    Amount = 10000
    Position = 0
    for index in range(len(data)):
        if index % 7 == 0:
            price = data['Close'].iloc[index]
            signal = data['Signal_Buy_Sell'].iloc[index]
        if signal == "Buy" and Position == 0:
            Position = Amount / price
            Amount = 0
        elif signal == "Sell" and Position > 0:
            Amount = Position * price
            Position = 0
        Total_Value = Amount + Position * price
        Portfolio_Value.append(Total_Value)
    data['Portfolio_Value'] = Portfolio_Value
    display_back_testing(data)
    st.write(f"In One Year The Final_Amount = {data['Portfolio_Value'].iloc[-1]}")
