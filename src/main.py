import os
import pandas as pd
from csv_reader import CSVReader
from data_processor import DataProcessor
from database import DatabaseConnection
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main(file_path: str):
    # Load the CSV data
    reader = CSVReader(file_path)
    reader.load_data()
    df = reader.get_dataframe()

    # Process the data
    processor = DataProcessor(df)
    processor.add_converted_column()
    processor.add_state_abbreviation_column()
    processor.add_normalized_column('purchase')
    processor.add_85_percentile_state()
    processor.add_85_percentile_nationality()
    processor.fill_in_missing_with_median('time_spent_seconds')

    # Save plots
  #  processor.store_plot(processor.get_boxplot('purchase'), 'boxplot_purchase.png')
  #  fig = processor.plot_and_save_histograms(['purchase', 'time_spent_seconds'])
  #  fig.savefig('histograms.png')

    # Connect to the database and insert data
    db = DatabaseConnection()
    db.connect()

    for _, row in processor.data.iterrows():
        data = {
            'ip_address': row['ip_address'],
            'marketing_channel': row['marketing_channel'],
            'purchase': row['purchase'],
            'state': row['state'],
            'time_spent_seconds': row['time_spent_seconds'],
            'converted': row['converted'],
            'state_abbreviation': row['state_abbreviation'],
            'purchase_normalized': row['purchase_normalized'],
            'percentile_85_state': row['85th_percentile_state'],
            'percentile_85_national': row['85th_percentile_national']
        }
        db.add_row('processed_data', data)

    db.close()

    print("Data processed and stored successfully")

if __name__ == "__main__":
 #   import sys
  #  if len(sys.argv) != 2:
   #     print("Usage: python main.py <path_to_csv_file>")
    #    sys.exit(1)
    
    file_path = "../dataset.csv"
    main(file_path)

