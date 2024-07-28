# Import candles from a directory of csv files containing OHLCV data into Jesse
# matching to the csv files from Interactive Brokers
# jesse expects each row to be 1m candlestick

import os
import pandas as pd
import numpy
from jesse import research
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='File path or directory containing candles to import', required=True)
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not import candles to database')
    args = parser.parse_args()
    return args


def flow_from_df(dataframe: pd.DataFrame, chunk_size: int = 10):
    for start_row in range(0, dataframe.shape[0], chunk_size):
        end_row  = min(start_row + chunk_size, dataframe.shape[0])
        yield dataframe.iloc[start_row:end_row, :]

    
def parse_exchange(filename):
    if '__' in filename and filename.endswith('.csv'):
        return filename.split('__')[-1].split('.csv')[0]
    else:
        return None

def import_candles(destination, dry_run=False):
    if not os.path.isdir(destination):
        directory, filename = os.path.split(destination)
        _import_candles(directory, filename, dry_run)
    else:
        for file in os.listdir(destination):
            filename = os.fsdecode(file)
            _import_candles(destination, filename, dry_run)

def _import_candles(directory, filename, dry_run=False):
    if filename.endswith(".csv"): 
        symbol = filename.split('__').pop(0)
        
        # We need to add *-USD posix otherwise backtests will fail later
        symbol += '-USD'
        print ("importing " + symbol)
        
        # Read the file into a pandas dataframe 
        df = pd.read_csv(os.path.join(directory, filename))
        df['date'] = pd.to_datetime(df['date'])
        df.rename(columns={'date': 'timestamp'}, inplace=True)
        df['timestamp'] = df['timestamp'].astype(int) / 1e6  # convert datetime to unix timestamp


        # Reorder columns as jesse expects candles to be in format:
        # 'timestamp', 'open', 'close', 'high', 'low', volume'
        df = df[['timestamp', 'open', 'close', 'high', 'low', 'volume']]
        
        # Import them candles in batches
        for chunk in flow_from_df(df, 1000):
            candles = chunk.to_numpy()
            print(f"{'DRY RUN: ' if dry_run else ''} Storing chunk of {len(candles)} candles for {symbol}")
            # exchange = parse_exchange(filename)
            exchange = 'Binance Spot'
            if not dry_run:
                research.store_candles(candles, exchange, symbol)
    else:
        print ("ignoring " + filename)

if __name__ == '__main__':
    args = parse_args()
    import_candles(args.path, args.dry_run)