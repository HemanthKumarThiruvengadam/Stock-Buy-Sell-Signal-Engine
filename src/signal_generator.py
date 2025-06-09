import streamlit as st
import pandas as pd
from backtest import back_testing
import plotly.graph_objects as plo
def signal_bars(buy_perc,sell_perc):
    fig = plo.Figure()
    fig.add_trace(plo.Bar(
        y = ["BUY"],
        x = [buy_perc],
        orientation = 'h',
        marker=dict(
            color = 'limegreen',
            line = dict(color = 'green',width = 3),   
        ),
        text = f"{buy_perc:.2f}%",
        textposition = 'inside',
        name = 'BUY'
    ))
    fig.add_trace(plo.Bar(
        y = ["SELL"],
        x = [sell_perc],
        orientation = 'h',
        marker=dict(
            color = 'red',
            line = dict(color = 'darkred',width = 3),   
        ),
        text = f"{sell_perc:.2f}%",
        textposition = 'inside',
        name = 'SELL'
    ))
    fig.update_layout(
        barmode = 'stack',
        height = 200,
        margin = dict(l = 40,r = 40,t = 40,b = 40),
        xaxis = dict(range = [0,100],
                     showgrid = False,zeroline = False,showticklabels = False),
        yaxis = dict(showgrid = False,zeroline = False),
        plot_bgcolor = 'black',
        paper_bgcolor = 'black',
        font = dict(color = 'white',size = 16,family = "Courier New"),
        title = "🚀 Buy/Sell Signal Confidence",
    )
    st.plotly_chart(fig,use_container_width = True)


def generate_signal_data(data):
    empty_data = pd.DataFrame(index = data.index,columns = ['Signal_Buy_Sell'])
    for index in range(len(data)):
        Total_Indicators = 7
        Buy_Indicators = 0
        Sell_Indicators = 0
        if(data['rsi'].iloc[index] > 70):
            Sell_Indicators += 1
        if(data['rsi'].iloc[index] < 30):
            Buy_Indicators += 1
        if(data['50_day_MA'].iloc[index] > data['200_day_MA'].iloc[index]):
            Buy_Indicators += 1
        else:
            Sell_Indicators += 1
        if(data['MACD'].iloc[index] > data['Signal'].iloc[index]):
            Buy_Indicators += 1
        else:
            Sell_Indicators += 1
        if(data['MACD'].iloc[index] < 0 and data['Signal'].iloc[index] < 0):
            Buy_Indicators += 1
        if(data['MACD'].iloc[index] > 0 and data['Signal'].iloc[index] > 0):
            Sell_Indicators += 1
        if(data['LB'].iloc[index] >= data['Close'].iloc[index] and data['rsi'].iloc[index] < 30):
            Buy_Indicators += 1
        if(data['UB'].iloc[index] <= data['Close'].iloc[index] and data['rsi'].iloc[index] > 70):
            Sell_Indicators += 1
        if(data['UB'].iloc[index] < data['Close'].iloc[index] and data['Volume'].iloc[index] > data['avg_volume_5'].iloc[index]):
            Buy_Indicators += 1
        if(data['LB'].iloc[index] > data['Close'].iloc[index] and data['Volume'].iloc[index] > data['avg_volume_5'].iloc[index]):
            Sell_Indicators += 1
        Buy_Confidence_Percentage = (Buy_Indicators / Total_Indicators) * 100
        Sell_Confidence_Percentage = (Sell_Indicators / Total_Indicators) * 100
        if(Buy_Confidence_Percentage > Sell_Confidence_Percentage):
            empty_data.loc[data.index[index],'Signal_Buy_Sell'] = "Buy"
        elif(Sell_Confidence_Percentage > Buy_Confidence_Percentage):
            empty_data.loc[data.index[index],'Signal_Buy_Sell'] = "Sell"
        else:
            empty_data.loc[data.index[index],'Signal_Buy_Sell'] = "Hold"
    data['Signal_Buy_Sell'] = empty_data
    return data
def generate_signal(data):
    Total_Indicators = 7
    Buy_Indicators = 0
    Sell_Indicators = 0
    latest_date = data.index.max()
    if(data['rsi'].loc[latest_date] > 70):
        Sell_Indicators += 1
    if(data['rsi'].loc[latest_date] < 30):
        Buy_Indicators += 1
    if(data['50_day_MA'].loc[latest_date] > data['200_day_MA'].loc[latest_date]):
        Buy_Indicators += 1
    else:
        Sell_Indicators += 1
    if(data['MACD'].loc[latest_date] > data['Signal'].loc[latest_date]):
        Buy_Indicators += 1
    else:
        Sell_Indicators += 1
    if(data['MACD'].loc[latest_date] < 0 and data['Signal'].loc[latest_date] < 0):
        Buy_Indicators += 1
    if(data['MACD'].loc[latest_date] > 0 and data['Signal'].loc[latest_date] > 0):
        Sell_Indicators += 1
    if(data['LB'].loc[latest_date] >= data['Close'].loc[latest_date] and data['rsi'].loc[latest_date] < 30):
        Buy_Indicators += 1
    if(data['UB'].loc[latest_date] <= data['Close'].loc[latest_date] and data['rsi'].loc[latest_date] > 70):
        Sell_Indicators += 1
    if(data['UB'].loc[latest_date] < data['Close'].loc[latest_date] and data['Volume'].loc[latest_date] > data['avg_volume_5'].loc[latest_date]):
        Buy_Indicators += 1
    if(data['LB'].loc[latest_date] > data['Close'].loc[latest_date] and data['Volume'].loc[latest_date] > data['avg_volume_5'].loc[latest_date]):
        Sell_Indicators += 1
    Buy_Confidence_Percentage = (Buy_Indicators / Total_Indicators) * 100
    Sell_Confidence_Percentage = (Sell_Indicators / Total_Indicators) * 100
    if(Buy_Confidence_Percentage > Sell_Confidence_Percentage):
        st.markdown('<span style = " color : limegreen;">Buy Signal</span>',unsafe_allow_html = True)
        signal_bars(Buy_Confidence_Percentage,Sell_Confidence_Percentage)
    elif(Sell_Confidence_Percentage > Buy_Confidence_Percentage):
        st.markdown('<span style = " color : red;">Sell Signal</span>',unsafe_allow_html = True)
        signal_bars(Buy_Confidence_Percentage,Sell_Confidence_Percentage)
    else:
        st.write("HOLD")
        signal_bars(Buy_Confidence_Percentage,Sell_Confidence_Percentage)
    data = generate_signal_data(data)
    back_testing(data)

