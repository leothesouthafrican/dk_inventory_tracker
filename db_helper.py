import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the SQLite database
con = sqlite3.connect("inventory_data.db", check_same_thread=False)

# Function to save the DataFrame to a new table
def save_df_to_db(df, table_name):
    df.to_sql(table_name, con, if_exists="replace", index=False)

# Function to load a DataFrame from a specific table
def load_df_from_db(table_name: str):
    return pd.read_sql_query(f'SELECT * FROM "{table_name}"', con)

# Function to get a list of table names in the database
def get_table_names():
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [t[0] for t in cursor.fetchall()]
    return table_names


