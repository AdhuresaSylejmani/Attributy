import logging
import os
import traceback

import psycopg2
from dotenv import find_dotenv, load_dotenv
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

load_dotenv(find_dotenv(), override=True)

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(self.db_url)
            logger.info('Connected to the database successfully.')
        except psycopg2.Error as e:
            logger.error(f'Error connecting to the database: {e}')
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info('Database connection closed.')

    def fetch_data(self, query, params=None):
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

    def add_row(self, table_name: str, data: dict, return_id: str = 'id') -> None:
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
