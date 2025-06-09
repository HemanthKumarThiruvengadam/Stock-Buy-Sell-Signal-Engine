import streamlit as st
from yahooquery import search
from data_loaders import fetch_stock_data
def main():
# 🧠 Cache to persist ticker search results
    if 'tickers' not in st.session_state:
        st.session_state.tickers = []
    if 'data_ready' not in st.session_state:
        st.session_state.data_ready = False

    st.title("📈 Stock Buy/Sell Signal Engine")

    company_name = st.text_input("Enter Company Name")

    if st.button("Search Tickers"):
        results = search(company_name)
        st.session_state.tickers = [res['symbol'] for res in results['quotes'] if 'symbol' in res]
        st.session_state.data_ready = False  


    if st.session_state.tickers:
        ticker = st.selectbox("Choose a Stock Ticker", st.session_state.tickers)

        if st.button("Run Signal Engine"):
            st.session_state.selected_ticker = ticker
            st.session_state.data_ready = True

   
    if st.session_state.get('data_ready', False):
        data = fetch_stock_data(st.session_state.selected_ticker)

if __name__ == "__main__":
    main()

