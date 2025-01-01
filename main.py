import yfinance as yf
import pandas as pd
from analysis import get_biggest_losers, calculate_return, analyze_results
from datetime import timedelta
from tqdm import tqdm
from datetime import datetime
import pytz  # Import for timezone handling

# Set the precise 5-year window ending 2 years ago
# Set the precise 5-year window ending 2 years ago
end_date = datetime.now() - timedelta(days=365*2)
start_date = end_date - timedelta(days=365*5)

# Make both start_date and end_date timezone-aware (UTC)
ny_tz = pytz.timezone('America/New_York')
end_date = ny_tz.localize(end_date.replace(hour=0, minute=0, second=0, microsecond=0))
start_date = ny_tz.localize(start_date.replace(hour=0, minute=0, second=0, microsecond=0))





def main():
    
    #May need the link to the current symbols for the daily listener. 
    #sp500_symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    sp500_symbols = pd.read_csv('FinalTickers.csv', header=None).squeeze().tolist()
    data = {}
    for symbol in sp500_symbols:
        try:
            stock = yf.Ticker(symbol)
            # Fetch historical data within the specific 5-year window
            hist_data = stock.history(start=start_date, end=end_date)
            
            # Store the filtered data
            if not hist_data.empty:
                data[symbol] = hist_data
                #print(f"Running {symbol}: data IS available in time window")
            else:
                x = 0
                # print(f"Skipping {symbol}: No data available in time window")
        except Exception as e:
            # print(f"Error fetching data for {symbol}: {e}")
            y =0

    # Step 2: Analyze each day and store the results
    results = []
    # Ensure we analyze dates within the 5-year window
    # analysis_start_date = max(start_date, data['AAPL'].index[0])  # Use AAPL or another reliable stock
    # analysis_dates = data['AAPL'].loc[analysis_start_date:].index
    analysis_dates = pd.date_range(
        start=start_date, 
        end=end_date, 
        tz='America/New_York',  # Use America/New_York for timezone
        name="Date"  # Assign the name 'Date' to the index
    )

# Ensure frequency is set to None (by converting to a list and back to DatetimeIndex)
    analysis_dates = pd.DatetimeIndex(analysis_dates.tolist(), name="Date")

    # Loop over the analysis dates
    for date in analysis_dates:
        # data = {}
        # hist_data = None
        # for symbol in sp500_symbols:
        #     try:
        #         stock = yf.Ticker(symbol)
        #         temp_end_date = date + timedelta(days=365*2)
        #         # Fetch historical data within the specific 5-year window
        #         hist_data = stock.history(start=date, end=temp_end_date)
                
        #         # Store the filtered data
        #         if not hist_data.empty:
        #             data[symbol] = hist_data
        #         else:
        #             print(f"Skipping {symbol}: No data available in time window")
        #     except Exception as e:
        #         print(f"Error fetching data for {symbol}: {e}")
        losers = get_biggest_losers(data, date)
        for loser in losers:
            return_2y = calculate_return(data, loser, date)
            if return_2y is not None:
                results.append({
                    'date': date,
                    'loser': loser,
                    'return_2y': return_2y
                })
    
    # Step 3: Analyze results
    df_results = pd.DataFrame(results)
    analyze_results(df_results, start_date, end_date)

if __name__ == "__main__":
    main()
