import pandas as pd     #read csv file and upload to database
import pypyodbc as odbc     #connecting to database
from sqlalchemy import create_engine    #creates database engine 
from sqlalchemy.engine import URL       #creates connection string
import os

os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'   
os.environ['LD_LIBRARY_PATH'] = '/opt/homebrew/lib'

my_server_name = 'sqlserverparth.database.windows.net'
my_database_name = 'sqldb_parth'
driver_type = '{ODBC Driver 18 for SQL Server}'
username = 'saparth'
password = 'Superman7060$'

connection_string = URL.create(
    "mssql+pyodbc",
    query={
        "odbc_connect": (
            f"DRIVER={driver_type};"
            f"SERVER={my_server_name};"
            f"DATABASE={my_database_name};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt=yes;TrustServerCertificate=no;"
        )
    }
)

new_engine = create_engine(connection_string, module=odbc)
csv_file_name = '/Users/parthpatel/Downloads/USEDATA.csv'

read_data = pd.read_csv(
    csv_file_name,
    dtype={8: str, 9: str, 10: str, 11: str, 12: str},  
    low_memory=False,
    nrows=500 
)

read_data.to_sql("NewStagingTable", new_engine, if_exists="replace", index=False, chunksize=100)
