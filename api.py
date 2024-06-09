from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from csv_reader import CSVReader
from data_processor import DataProcessor
from database import DatabaseConnection
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

class DataRow(BaseModel):
    ip_address: str
    marketing_channel: str
    purchase: Optional[float] = None
    state: str
    time_spent_seconds: Optional[int] = None
    converted: Optional[int] = None
    state_abbreviation: Optional[str] = None
    purchase_normalized: Optional[float] = None
    percentile_85_state: Optional[int] = None
    percentile_85_national: Optional[int] = None

class DataInput(BaseModel):
    data: List[DataRow]

@app.post("/process_data/")
def process_data(data_input: DataInput):
    data = data_input.data
    df = pd.DataFrame([row.dict() for row in data])
    
    processor = DataProcessor(df)

    processor.add_converted_column()
    processor.add_state_abbreviation_column()
    processor.add_normalized_column('purchase')
    processor.add_85_percentile_state()
    processor.add_85_percentile_nationality()
    processor.fill_in_missing_with_median('time_spent_seconds')

    # processor.store_plot(processor.get_boxplot('purchase'), 'boxplot_purchase.png')
    # fig = processor.plot_and_save_histograms(['purchase', 'time_spent_seconds'])
    # fig.savefig('histograms.png')

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
            'percentile_85_state': row['percentile_85_state'],
            'percentile_85_national': row['percentile_85_national']
        }
        db.add_row('processed_data', {k: None if pd.isna(v) else v for k, v in data.items()})

    db.close()

    return {"message": "Data processed and stored successfully"}

@app.get("/data/")
def get_data():
    db = DatabaseConnection()
    db.connect()
    query = 'SELECT * FROM processed_data'
    data = db.fetch_data(query)
    db.close()

    # Convert data to a format that handles NaN values
    sanitized_data = [
        {k: None if pd.isna(v) else v for k, v in row.items()}
        for row in data
    ]

    return sanitized_data
