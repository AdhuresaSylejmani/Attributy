import pandas as pd

class CSVReader:
    """
    A class to read CSV files and load them into a pandas DataFrame.

    Attributes
    ----------
    file_path : str
        Path to the CSV file.
    dataframe : pd.DataFrame or None
        DataFrame to store the loaded data. Initialized to None.

    Methods
    -------
    load_data() -> None
        Loads data from the CSV file into the dataframe attribute.
    get_dataframe() -> pd.DataFrame
        Returns the loaded DataFrame.
    """

    def __init__(self, file_path: str):
        """
        Constructs all the necessary attributes for the CSVReader object.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to be read.
        """
        self.file_path = file_path
        self.dataframe = None

    def load_data(self) -> None:
        """
        Loads data from the CSV file into the dataframe attribute.

        This method attempts to read a CSV file from the path specified during 
        the initialization of the object and stores it in the dataframe attribute. 
        It handles various exceptions that may occur during this process.
        
        Raises
        ------
        FileNotFoundError
            If the file is not found at the specified path.
        pd.errors.EmptyDataError
            If the file is empty.
        pd.errors.ParserError
            If there is an error parsing the file.
        Exception
            For any other exceptions that occur.
        """
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
        """
        Returns the loaded DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the loaded data.
        """
        return self.dataframe
