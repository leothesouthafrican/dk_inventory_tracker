from datetime import datetime
import streamlit as st
import pandas as pd
from graphing import plot_items_per_category, plot_quantity_per_category, plot_total_value_per_category, plot_unrealised_value_per_category, plot_decreased_items, plot_gross_profit, plot_least_sold_categories
from db_helper import get_table_names, load_df_from_db
from data_cleaning import load_transform_save


#Setting variables
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
TABLE_NAME = f"inventory_data_{CURRENT_DATE}"

st.set_page_config(layout="wide")

# Custom CSS to reduce margins
custom_css = """
<style>
    .reportview-container .main .block-container {
        max-width: 95%;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.header("DasKasas Inventory Tracker")

#horizontal line
st.markdown("---")

# ----------------------------------------------------
#                    SIDEBAR
#-----------------------------------------------------
with st.sidebar:
    product_csv = st.file_uploader("Please Upload Updated Inventory CSV Export from DEAR Inventory.")
    
    stock_levels_csv = st.file_uploader("Please Upload Updated Stock Levels CSV Export from DEAR Inventory.")

    previous_data = st.selectbox("Select Previous Data", get_table_names("inventory_data.db"))

# ----------------------------------------------------
#                    Data Processing
#-----------------------------------------------------
if product_csv and stock_levels_csv:

    #Loading, transforming and saving the current data (uploaded today)
    current_df = load_transform_save(product_csv, stock_levels_csv)

    #Loading the previous data (selected from the dropdown)
    previous_df = load_df_from_db(previous_data)

    #Creating a df that merges the two and shows the difference in quantity
    merged_df = pd.merge(current_df, previous_df, on="ProductCode", how="left")
    merged_df["QuantityChange"] = merged_df["Quantity_x"] - merged_df["Quantity_y"]
    merged_df = merged_df[["ProductCode", "Quantity_x", "Quantity_y", "QuantityChange", "Name_x", "Category_x", "AverageCost_x", "PriceTier1_x", "PriceTier2_x", "PriceTier3_x", "PriceTier4_x", "PriceTier5_x"]]
    merged_df = merged_df.rename(columns={"Quantity_x": "CurrentQuantity", "Quantity_y": "PreviousQuantity", "Name_x": "Name", "Category_x": "Category", "AverageCost_x": "AverageCost", "PriceTier1_x": "PriceTier1", "PriceTier2_x": "PriceTier2", "PriceTier3_x": "PriceTier3", "PriceTier4_x": "PriceTier4", "PriceTier5_x": "PriceTier5"})
    
    #Saving the merged file to a new table in the database
    merged_df.to_sql(f"merged_data_{CURRENT_DATE}", "sqlite:///inventory_data.db", if_exists="replace", index=False)

# ----------------------------------------------------
#               Plotting Current Data
#-----------------------------------------------------

    st.plotly_chart(plot_items_per_category(current_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_quantity_per_category(current_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_total_value_per_category(current_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_unrealised_value_per_category(current_df), use_container_width=True)
    st.markdown("---")
    st.header("Comparative Graphs")

    #Number of ProductCodes to display
    num_product_codes = st.slider('Number of Product Codes to Display', min_value=1, max_value=30, value=10)
    # Only if there is a QuantityChange
    if 'QuantityChange' in merged_df.columns:
        st.plotly_chart(plot_decreased_items(merged_df, num_product_codes), use_container_width=True)

    st.markdown("---")
    # Number of ProductCodes to display for gross profit plot
    num_product_codes_gross_profit = st.slider('Number of Product Codes to Display for Gross Profit', min_value=1, max_value = 30, value=10)

    # Only if there is a GrossProfit
    if 'QuantityChange' in merged_df.columns and 'PriceTier4' in merged_df.columns and 'AverageCost' in merged_df.columns:
        st.plotly_chart(plot_gross_profit(merged_df, num_product_codes_gross_profit), use_container_width=True)

    st.markdown("---")
    # Number of categories to display for least sold categories plot
    num_categories_least_sold = st.slider('Number of Categories to Display for Least Sold Categories', min_value=1, max_value=len(merged_df['Category'].unique()), value=10)

    # Only if there is a QuantityChange
    if 'QuantityChange' in merged_df.columns:
        st.plotly_chart(plot_least_sold_categories(merged_df, num_categories_least_sold), use_container_width=True)