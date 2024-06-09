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
    """
    Redirects the root URL to the API documentation.

    Returns
    -------
    RedirectResponse
        A response that redirects the user to the /docs endpoint.
    """
    return RedirectResponse(url="/docs")

class DataRow(BaseModel):
    """
    A Pydantic model representing a single row of data.

    Attributes
    ----------
    ip_address : str
        IP address of the user.
    marketing_channel : str
        Marketing channel through which the user was acquired.
    purchase : float, optional
        Purchase amount made by the user.
    state : str
        State where the user is located.
    time_spent_seconds : int, optional
        Time spent by the user on the site in seconds.
    converted : int, optional
        Indicates if the user made a purchase (1 if true, 0 if false).
    state_abbreviation : str, optional
        Abbreviation of the state where the user is located.
    purchase_normalized : float, optional
        Normalized purchase amount.
    percentile_85_state : int, optional
        Indicates if the user's purchase is in the 85th percentile within their state (1 if true, 0 if false).
    percentile_85_national : int, optional
        Indicates if the user's purchase is in the 85th percentile nationally (1 if true, 0 if false).
    """
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
    """
    A Pydantic model representing a list of data rows.

    Attributes
    ----------
    data : List[DataRow]
        A list of data rows.
    """
    data: List[DataRow]

@app.post("/process_data/")
def process_data(data_input: DataInput):
    """
    Processes the input data and stores it in the database.

    Parameters
    ----------
    data_input : DataInput
        Input data to be processed.

    Returns
    -------
    dict
        A message indicating that the data was processed and stored successfully.
    """
    data = data_input.data
    df = pd.DataFrame([row.dict() for row in data])
    
    processor = DataProcessor(df)

    processor.add_converted_column()
    processor.add_state_abbreviation_column()
    processor.add_normalized_column('purchase')
    processor.add_85_percentile_state()
    processor.add_85_percentile_nationality()
    processor.fill_in_missing_with_median('time_spent_seconds')

    # Uncomment these lines to save the plots
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
    """
    Retrieves all data from the database.

    Returns
    -------
    List[dict]
        A list of dictionaries representing the rows of data in the database.
    """
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
