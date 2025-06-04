from yahooquery import search 
def main():
    company_name = input("Enter Company's Name: ")
    results = search(company_name)
    tickers = []
    for index,result in enumerate(results['quotes'],start = 1):
        
        symbol = result['symbol']
        tickers.append(symbol)
        name = result.get('shortname','N/A')
        print(f"[{index}] {symbol} - {name}")
    index = int(input("Enter the correct ticker (Enter the number): "))
    print("You have selected ticker: " + tickers[index - 1])

if __name__ == "__main__":
    main()

