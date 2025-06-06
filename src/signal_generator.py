from rich.console import Console
from rich.progress import Progress,BarColumn,TextColumn
def generate_signal(data):
    console = Console()
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
        console.print("[bright_green]Buy Signal")
        with Progress(
            TextColumn("[bright_green]Buy",justify = "right"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Buy_Confidence_Percentage:.2f} %",style = "bright_green"),
        )as progress:
            progress.add_task("Buy",total = 100,completed = Buy_Confidence_Percentage)
        with Progress(
            TextColumn("[bright_red]SELL",justify = "left"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Sell_Confidence_Percentage:.2f} %",style = "bright_red")
        )as progress:
            progress.add_task("Sell",total = 100,completed = Sell_Confidence_Percentage)

    elif(Sell_Confidence_Percentage > Buy_Confidence_Percentage):
        console.print("[bright_red]Sell Signal")
        with Progress(
            TextColumn("[bright_green]Buy",justify = "right"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Buy_Confidence_Percentage:.2f} %",style = "bright_green"),
        )as progress:
            progress.add_task("Buy",total = 100,completed = Buy_Confidence_Percentage)
        with Progress(
            TextColumn("[bright_red]SELL",justify = "left"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Sell_Confidence_Percentage:.2f} %",style = "bright_red")
        )as progress:
            progress.add_task("Sell",total = 100,completed = Sell_Confidence_Percentage)
    else:
        console.print("[bright_white]HOLD")
        with Progress(
            TextColumn("[bright_green]Buy",justify = "right"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Buy_Confidence_Percentage:.2f} %",style = "bright_green"),
        )as progress:
            progress.add_task("Buy",total = 100,completed = Buy_Confidence_Percentage)
        with Progress(
            TextColumn("[bright_red]SELL",justify = "left"),
            BarColumn(bar_width = 50),
            TextColumn(f"{Sell_Confidence_Percentage:.2f} %",style = "bright_red")
        )as progress:
            progress.add_task("Sell",total = 100,completed = Sell_Confidence_Percentage)
