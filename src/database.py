import logging
import os
import traceback

import psycopg2
from dotenv import find_dotenv, load_dotenv
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    A class to handle database connections and operations.

    Attributes
    ----------
    db_url : str
        The database URL from the environment variables.
    connection : psycopg2.extensions.connection
        The connection object to the PostgreSQL database.

    Methods
    -------
    connect():
        Establishes a connection to the database.
    close():
        Closes the database connection.
    fetch_data(query, params=None):
        Fetches data from the database based on the provided SQL query and parameters.
    add_row(table_name: str, data: dict, return_id: str = 'id') -> int:
        Adds a row to the specified table in the database and returns the ID of the new row.
    delete_row(table_name: str, row_id: int):
        Deletes a row from the specified table in the database based on the provided row ID.
    """

    def __init__(self):
        """
        Initializes the DatabaseConnection class by setting the database URL
        from the environment variables and initializing the connection attribute.
        """
        self.db_url = os.environ.get('DATABASE_URL')
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the database using the database URL.

        Logs a message indicating whether the connection was successful or if an error occurred.
        """
        try:
            self.connection = psycopg2.connect(self.db_url)
            logger.info('Connected to the database successfully.')
        except psycopg2.Error as e:
            logger.error(f'Error connecting to the database: {e}')
            self.connection = None

    def close(self):
        """
        Closes the database connection if it is open.

        Logs a message indicating that the connection has been closed.
        """
        if self.connection:
            self.connection.close()
            logger.info('Database connection closed.')

    def fetch_data(self, query, params=None):
        """
        Fetches data from the database based on the provided SQL query and parameters.

        Parameters
        ----------
        query : str
            The SQL query to be executed.
        params : tuple, optional
            The parameters to be used in the SQL query.

        Returns
        -------
        list of dict
            The fetched data from the database.

        Raises
        ------
        Exception
            If there is no database connection.
        """
        if not self.connection:
            logger.error('No database connection.')
            raise Exception('No database connection.')
        cursor = None
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            data = cursor.fetchall()
            logger.info('Data fetched successfully.')
            return data
        except psycopg2.Error as e:
            logger.error(f'Error fetching data: {e}')
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()

    def add_row(self, table_name: str, data: dict, return_id: str = 'id') -> int:
        """
        Adds a row to the specified table in the database and returns the ID of the new row.

        Parameters
        ----------
        table_name : str
            The name of the table where the row should be added.
        data : dict
            The data to be added to the table.
        return_id : str, optional
            The name of the column that contains the ID to be returned (default is 'id').

        Returns
        -------
        int
            The ID of the newly added row.

        Raises
        ------
        Exception
            If there is no database connection.
        """
        if not self.connection:
            logger.error('No database connection.')
            raise Exception('No database connection.')
        cursor = None
        try:
            columns = data.keys()
            values = data.values()
            query = sql.SQL(
                ('INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING {id}')
            ).format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                values=sql.SQL(', ').join(sql.Placeholder() * len(values)),
                id=sql.Identifier(return_id),
            )
            cursor = self.connection.cursor()
            cursor.execute(query, list(values))
            new_row_id = cursor.fetchone()[0]
            self.connection.commit()
            return new_row_id
        except psycopg2.Error as e:
            logger.error(f'Error adding data @{table_name}: {e}')
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def delete_row(self, table_name: str, row_id: int) -> None:
        """
        Deletes a row from the specified table in the database based on the provided row ID.

        Parameters
        ----------
        table_name : str
            The name of the table from which the row should be deleted.
        row_id : int
            The ID of the row to be deleted.

        Raises
        ------
        Exception
            If there is no database connection.
        """
        if not self.connection:
            logger.error('No database connection.')
            raise Exception('No database connection.')
        cursor = None
        try:
            query = sql.SQL('DELETE FROM {table} WHERE id = %s').format(
                table=sql.Identifier(table_name),
            )
            cursor = self.connection.cursor()
            cursor.execute(query, (row_id,))
            self.connection.commit()
        except psycopg2.Error as e:
            logger.error(f'Error deleting data @{table_name}: {e}')
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()
