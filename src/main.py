from data_loaders import fetch_stock_data
from yahooquery import search 
from rich.console import Console
def main():
    console = Console()
    company_name = input("Enter Company's Name: ")
    results = search(company_name)
    tickers = []
    for index,result in enumerate(results['quotes'],start = 1):
        
        symbol = result['symbol']
        tickers.append(symbol)
        name = result.get('shortname','N/A')
        console.print(f"[bright_white][{index}] {symbol} - {name}")
    index = int(input("Enter the correct ticker (Enter the number): "))
    ticker = tickers[index - 1]
    console.print("[bright_blue]You have selected ticker: " + ticker)
    fetch_stock_data(ticker)



if __name__ == "__main__":
    main()

