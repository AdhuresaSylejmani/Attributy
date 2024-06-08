import pandas as pd


class CSVReader:


    def __init__(self, file_path: str):

        self.file_path = file_path
        self.dataframe = None

    def load_data(self) -> None:

        try:
            self.dataframe = pd.read_csv(self.file_path)
            print(f"Data loaded successfully from {self.file_path}")
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except pd.errors.EmptyDataError:
            print(f"No data: {self.file_path}")
        except pd.errors.ParserError:
            print(f"Parse error: {self.file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe

