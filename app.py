from datetime import datetime
import streamlit as st
import pandas as pd
from helper_functions import plot_items_per_category, plot_quantity_per_category, plot_total_value_per_category, plot_unrealised_value_per_category, avg_gross_margin_per_category, plot_top_10_sku_increase, plot_top_10_stagnated_skus, plot_category_quantity_change, plot_category_value_change
from db_helper import get_table_names, load_df_from_db, save_df_to_db

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

    previous_data = st.selectbox("Select Previous Data", get_table_names())

# ----------------------------------------------------
#                    Data Processing
#-----------------------------------------------------
if product_csv and stock_levels_csv:
    product_df = pd.read_csv(product_csv)
    stock_levels_df = pd.read_csv(stock_levels_csv)
    
    stock_levels_df["Quantity"] = stock_levels_df["ProductCode"]
    stock_levels_df["ProductCode"] = stock_levels_df.index
    stock_levels_df = stock_levels_df[["ProductCode", "Quantity"]]


    # Ensure that both "ProductCode" columns have the same data type
    product_df["ProductCode"] = product_df["ProductCode"].astype(str)
    stock_levels_df["ProductCode"] = stock_levels_df["ProductCode"].astype(str)

    df = pd.merge(product_df, stock_levels_df, on="ProductCode", how="left")

    #keep only the following columns: ProductCode, Quantity, Name, Category, PriceTier1, PriceTier2, PriceTier3, PriceTier4, PriceTier5, AverageCost
    df = df[["ProductCode", "Quantity", "Name", "Category", "PriceTier1", "PriceTier2", "PriceTier3", "PriceTier4", "PriceTier5", "AverageCost"]]

    #Drop all rows where Category contains one of the following: "Delivery JHB", "Delivery PTA", "Installation", "Other", "Rooms", "Service"
    # Define the categories to remove
    excluded_categories = ["Delivery", "Installation", "Other", "Rooms", "Service", "Courier"]

    # Filter out rows containing the specified categories
    df = df[~df['Category'].str.contains('|'.join(excluded_categories))]

    #if the Quantity is NaN, set it to 0
    df["Quantity"] = df["Quantity"].fillna(0)

    #drop a row if the price is < 10
    final_df = df[df["PriceTier1"] > 10]

    #Save to database
    save_df_to_db(final_df, TABLE_NAME)

    previous_df = load_df_from_db(previous_data)

# ----------------------------------------------------
#               Plotting Current Data
#-----------------------------------------------------

    #plot the number of items per category
    items_cat = plot_items_per_category(final_df)

    #plot the total quantity of items per category
    quant_cat = plot_quantity_per_category(final_df)

    #plot the total value of items per category
    tv_cat = plot_total_value_per_category(final_df)

    #plot the unrealised value of items per category
    unrealised_gp_cat = plot_unrealised_value_per_category(final_df)

    #plot the average gross margin per category
    avg_gp_cat = avg_gross_margin_per_category(final_df)

    st.plotly_chart(items_cat, use_container_width=True)
    st.markdown("---")
    st.plotly_chart(quant_cat, use_container_width=True)
    st.markdown("---")
    st.plotly_chart(tv_cat, use_container_width=True)
    st.markdown("---")
    st.plotly_chart(unrealised_gp_cat, use_container_width=True)
    st.markdown("---")
    st.plotly_chart(avg_gp_cat, use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_top_10_sku_increase(final_df, previous_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_top_10_stagnated_skus(final_df, previous_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_category_quantity_change(final_df, previous_df), use_container_width=True)
    st.markdown("---")
    st.plotly_chart(plot_category_value_change(final_df, previous_df), use_container_width=True)



