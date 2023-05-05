import pandas as pd
import sqlite3
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
TABLE_NAME = f"inventory_data_{CURRENT_DATE}"

con = sqlite3.connect("inventory_data.db", check_same_thread=False)

def save_df_to_db(df, table_name):
    df.to_sql(table_name, con, if_exists="replace", index=False)

def aggregate_products(filename):
    # Read the CSV file into a DataFrame. Do not use the first column as index.
    df = pd.read_csv(filename, index_col=False)

    #Drop all rows where Quantity is NaN and print the number of rows dropped
    df = df.dropna(subset=['Quantity'])

    # Group by 'ProductCode' and aggregate 'Quantity' and 'AverageCost'
    aggregated_df = df.groupby('ProductCode', as_index=False).agg({
        'Quantity': 'sum'
    })

    return aggregated_df

def load_transform_save(inventory_csv, stock_csv):
    
    #Loading all of the dataframes
    inventory_csv = pd.read_csv(inventory_csv)
    stock_csv = aggregate_products(stock_csv)

    #Merging the dataframes
    merged_df = pd.merge(inventory_csv, stock_csv, on="ProductCode", how="left")
    # Dropping the columns that are not needed
    merged_df = merged_df[["ProductCode", "Quantity", "Name", "Category", "AverageCost", "PriceTier1", "PriceTier2", "PriceTier3", "PriceTier4", "PriceTier5"]]

    #Defining all the categories to remove
    excluded_categories = ["Delivery", "Installation", "Other", "Rooms", "Service", "Courier"]

    merged_df = merged_df[~merged_df['Category'].str.contains('|'.join(excluded_categories))]

    #Removing the rows that have no quantity or NaN
    merged_df = merged_df[merged_df["Quantity"] > 0] 
    merged_df = merged_df.dropna()

    #Dropping all of the items whose product code does not begin with "P"
    merged_df = merged_df[merged_df["ProductCode"].str.startswith("P")]

    #Only keeping products whos price is greater than 10
    merged_df = merged_df[merged_df["PriceTier1"] > 10]

    final_df = merged_df

    #Save to database
    save_df_to_db(final_df, TABLE_NAME)

    return final_df
