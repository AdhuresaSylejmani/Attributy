import pandas as pd

import sys
src_path = "/Users/adhuresasylejmani/Desktop/bb/Attributy"
sys.path.append(src_path)

from src.data_processor import DataProcessor

def test_add_converted_column():
    data = pd.DataFrame({
        'purchase': [100.0, None]
    })
    processor = DataProcessor(data)
    processor.add_converted_column()
    assert 'converted' in processor.data.columns
    assert processor.data['converted'].tolist() == [1, 0]

def test_add_state_abbreviation_column():
    data = pd.DataFrame({
        'state': ['New York', 'California']
    })
    processor = DataProcessor(data)
    processor.add_state_abbreviation_column()
    assert 'state_abbreviation' in processor.data.columns
    assert processor.data['state_abbreviation'].tolist() == ['NY', 'CA']

def test_add_normalized_column():
    data = pd.DataFrame({
        'purchase': [100.0, 200.0, 300.0]
    })
    processor = DataProcessor(data)
    processor.add_normalized_column('purchase')
    assert 'purchase_normalized' in processor.data.columns

def test_fill_in_missing_with_median():
    data = pd.DataFrame({
        'time_spent_seconds': [100, None, 200]
    })
    processor = DataProcessor(data)
    processor.fill_in_missing_with_median('time_spent_seconds')
    assert processor.data['time_spent_seconds'].tolist() == [100, 150, 200]
