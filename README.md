# Data Processing and Analysis Application

This application processes CSV data, performs basic data analysis and manipulation, and provides a FastAPI interface for accessing the data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## Prerequisites

- Python 3.7 or higher
- PostgreSQL

## Setup

1. **Clone the repository:**

    ```sh
    git clone git@github.com:AdhuresaSylejmani/Attributy.git
    cd Attributy
    ```

2. **Create and activate python virtual enviorment and Install dependencies:**

    ```sh
    python3 -m venv attributy_interview
    source ./attributy_interview/bin/activate
    pip install -r requirments.txt
    pip install pytest
    ```

3. **Set up environment variables:**

    ```sh
    export DATABASE_URL=postgresql://<username>:<password>@localhost:5432<database_name>
    ```

## Database Migrations

1. **Initialize Alembic:**

    ```sh
    alembic init migrations
    ```

2. **Configure Alembic:**

    Update `alembic.ini` and `migrations/env.py` to use the correct database URL from the environment variable.

    In `alembic.ini`:

    ```ini
    sqlalchemy.url = postgresql://<username>:<password>@localhost:5432/<database_name>
    ```

    In `migrations/env.py`:

    ```python
    from dotenv import load_dotenv
    import os

    load_dotenv()

    config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
    ```

3. **Create and apply migrations:**

    ```sh
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```

## Running the Application

1. **Run the main script to process the CSV and store data in the database:**

    ```sh
        python src/main.py
    ```

2. **Run the FastAPI server:**

    ```sh
    uvicorn api:app --host 127.0.0.1 --port 8000 --reload    
    ```

3. **Access the FastAPI documentation:**

    Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

- **`POST /process_data/`**: Process and store data from the request body.

    - Request Body:

        ```json
        {
            "data": [
                {
                    "ip_address": "192.168.1.1",
                    "marketing_channel": "A",
                    "purchase": 100.0,
                    "state": "NY",
                    "time_spent_seconds": 120,
                    "converted": 1,
                    "state_abbreviation": "NY",
                    "purchase_normalized": 0.5,
                    "percentile_85_state": 1,
                    "percentile_85_national": 0
                },
                {
                    "ip_address": "192.168.1.2",
                    "marketing_channel": "B",
                    "purchase": 150.0,
                    "state": "CA",
                    "time_spent_seconds": 180,
                    "converted": 1,
                    "state_abbreviation": "CA",
                    "purchase_normalized": 0.7,
                    "percentile_85_state": 0,
                    "percentile_85_national": 1
                }
            ]
        }
        ```

    - Response:

        ```json
        {
            "message": "Data processed and stored successfully"
        }
        ```

- **`GET /data/`**: Retrieve all processed data from the database.

    - Response:

        ```json
        [
            {
                "id": 1,
                "ip_address": "192.168.1.1",
                "marketing_channel": "A",
                "purchase": 100.0,
                "state": "NY",
                "time_spent_seconds": 120,
                "converted": 1,
                "state_abbreviation": "NY",
                "purchase_normalized": 0.5,
                "percentile_85_state": 1,
                "percentile_85_national": 0
            },
            ...
        ]
        ```

## Project Structure

- `src/`
    - `api.py`: Contains the FastAPI endpoints.
    - `main.py`: Script to process the CSV and store data in the database.
    - `csv_reader.py`: Contains the `CSVReader` class for reading CSV files.
    - `data_processor.py`: Contains the `DataProcessor` class for data manipulation and analysis.
    - `database.py`: Contains the `DatabaseConnection` class for database operations.
    - `models.py`: Contains the SQLAlchemy model for the `processed_data` table.
- `migrations/`: Contains Alembic migration files.
- `tests/`: Contains unit tests.

