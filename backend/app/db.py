"""Backend database.
"""
import os
import sqlite3
import typing as tp

from models import Run


class NoRunError(Exception):
    """Error raised when expected run is not found."""

    def __init__(self, message: str, date: str):
        super().__init__(message)
        self.date = date


class RunningDatabase(object):
    """Stores runs created in the app.
    """
    name = 'running'

    def __init__(self):
        pass

    @property
    def db(self):
        """Connect to the database.
        """
        connection = sqlite3.connect(f'{self.name}.db')
        connection.row_factory = sqlite3.Row
        return connection

    def execute(
        self,
        query,
        query_args: tp.Optional[tuple] = None,
        expect_data: bool = False
    ) -> tp.Union[None, list]:
        """Execute a query.
        """
        conn = self.db
        try:
            cursor = conn.cursor()
            if query_args is not None:
                cursor.execute(query, query_args)
            else:
                cursor.execute(query)
            if expect_data:
                return cursor.fetchall()
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    def create(self):
        """Create database and tables.
        """
        create_query = f"""CREATE TABLE runs (
            date DATE PRIMARY KEY,
            distance_miles FLOAT NOT NULL,
            duration_mins FLOAT NOT NULL,
            comments TEXT
        )"""
        self.execute(create_query)
       
    def clean(self, check=False):
        """Clean a database ready to start again.
        """
        if check and input('Are you sure? (yes to continue)') != 'yes':
            print('Clean operation not confirmed, tables still exist.')
            return

        self.execute(f'DROP TABLE IF EXISTS run')
        os.remove(f'{self.name}.db')

    def exists(self) -> bool:
        """Whether the tables exist yet.
        """
        expected = {"runs"}
        query = 'SELECT name from sqlite_master where type= "table"'
        tables = self.execute(query, expect_data=True)
        for table in tables:
            if table["name"] in expected:
                expected.remove(table["name"])
            else:
                print(f'Found unexpected table {table["name"]}')
        if expected:
            print(f"Tables {expected} were expected to exist but not found.")
            return False
        return True

    def store_run(self, run: Run) -> bool:
        """Store a run.
        """
        query = f"INSERT INTO runs VALUES (?, ?, ?, ?)"
        query_args = (run.date, run.distance_miles, run.duration_mins, run.comments)
        try:
            self.execute(query, query_args=query_args)
            return True
        except:
            return False
    
    def delete_run_on_date(self, date: str) -> bool:
        """Store a run."""
        query = f"DELETE FROM runs WHERE date = ?"
        try:
            self.execute(query, query_args=(date,))
            return True
        except:
            return False

    def get_run_on_date(self, date: str) -> Run:
        """Retrieve run on a date."""
        query = f"""
            SELECT date, distance_miles, duration_mins, comments
            FROM runs
            WHERE date = ?
        """
        try:
            run, *_ = self.execute(query, query_args=(date,), expect_data=True)
            return Run(**run)
        except ValueError:
            raise NoRunError(f"No run found on {date}", date)

    def get_runs_in_date_range(self, start_date: tp.Optional[str] = None, end_date: tp.Optional[str] = None):
        """Retrieve runs, optionally between two dates."""
        where_clause = ""
        query_args = []
        if start_date is not None:
            where_clause += f"AND date >= ?"
            query_args.append(start_date)
        if end_date is not None:
            where_clause += f"AND date <= ?"
            query_args.append(end_date)
        query = f"""
            SELECT date, distance_miles, duration_mins, comments
            FROM runs
            WHERE 1 = 1
            {where_clause}
            ORDER BY date ASC 
        """
        results = self.execute(query, query_args=query_args, expect_data=True)
        return {run["date"]: Run(**run) for run in results}
