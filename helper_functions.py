import plotly.graph_objs as go
import pandas as pd

def plot_items_per_category(df):
    items_per_category = df.groupby('Category')['ProductCode'].count().sort_values()
    fig = go.Figure(go.Bar(x=items_per_category.index, y=items_per_category.values, marker=dict(color='green')))
    fig.update_layout(
        autosize=True,
        margin=dict(l=30, r=30, t=30, b=30),
        title='Number of Unique SKUs per Category',
        yaxis_title='Number of Unique SKUs'
    )
    return fig

def plot_quantity_per_category(df):
    quantity_per_category = df.groupby('Category')['Quantity'].sum().sort_values()
    fig = go.Figure(go.Bar(x=quantity_per_category.index, y=quantity_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Total Quantity of Items per Category',
                    yaxis_title='Total Quantity',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_total_value_per_category(df):
    df['TotalValue'] = df['AverageCost'] * df['Quantity']
    total_value_per_category = df.groupby('Category')['TotalValue'].sum().sort_values()
    fig = go.Figure(go.Bar(x=total_value_per_category.index, y=total_value_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Total Value based off Average Cost per Category',
                    yaxis_title='Total Value (ZAR)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_unrealised_value_per_category(df):
    df['UnrealisedValue'] = (df['PriceTier1'] - df['AverageCost']) * df['Quantity']
    unrealised_value_per_category = df.groupby('Category')['UnrealisedValue'].sum().sort_values()
    fig = go.Figure(go.Bar(x=unrealised_value_per_category.index, y=unrealised_value_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Unrealised Gross Profit per Category',
                    yaxis_title='Unrealised Gross Profit (ZAR)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def avg_gross_margin_per_category(df):
    df['UnrealisedValue'] = (df['PriceTier1'] - df['AverageCost']) * df['Quantity']
    unrealised_value_per_category = df.groupby('Category')['UnrealisedValue'].sum().sort_values()
    total_value_per_category = df.groupby('Category')['TotalValue'].sum().sort_values()
    avg_gross_margin_per_category = unrealised_value_per_category / total_value_per_category
    avg_gross_margin_per_category = avg_gross_margin_per_category.sort_values()
    fig = go.Figure(go.Bar(x=avg_gross_margin_per_category.index, y=avg_gross_margin_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Average Gross Margin per Category',
                    yaxis_title='Average Gross Margin (%)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

import plotly.graph_objs as go

def plot_top_10_sku_increase(current_df, previous_df):
    # Calculate the difference in quantity for each SKU
    sku_difference = current_df[['ProductCode', 'Quantity']].merge(
        previous_df[['ProductCode', 'Quantity']], on='ProductCode', how='left', suffixes=('_current', '_previous')
    ).fillna(0)
    sku_difference['Quantity_difference'] = sku_difference['Quantity_current'] - sku_difference['Quantity_previous']

    # Sort the SKUs by the difference in quantity in descending order, select the top 10, and then sort in ascending order
    top_10_sku_increase = sku_difference.nlargest(10, 'Quantity_difference').sort_values(by='Quantity_difference')

    # Create a bar plot using Plotly
    fig = go.Figure(go.Bar(x=top_10_sku_increase['ProductCode'], y=top_10_sku_increase['Quantity_difference'], marker=dict(color='green')))
    fig.update_layout(title='Top 10 SKUs with Largest Quantity Increase',
                    xaxis_title='ProductCode',
                    yaxis_title='Quantity Increase',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))

    return fig

def plot_top_10_stagnated_skus(current_df, previous_df):
    # Calculate the difference in quantity for each SKU
    sku_difference = current_df[['ProductCode', 'Quantity']].merge(
        previous_df[['ProductCode', 'Quantity']], on='ProductCode', how='left', suffixes=('_current', '_previous')
    ).fillna(0)
    sku_difference['Quantity_difference'] = sku_difference['Quantity_current'] - sku_difference['Quantity_previous']

    # Filter the SKUs with non-negative quantity difference and sort by the difference in ascending order, then select the top 10
    top_10_stagnated_skus = sku_difference[sku_difference['Quantity_difference'] >= 0].nsmallest(10, 'Quantity_difference')

    # Create a bar plot using Plotly
    fig = go.Figure(go.Bar(x=top_10_stagnated_skus['ProductCode'], y=top_10_stagnated_skus['Quantity_difference'], marker=dict(color='orange')))
    fig.update_layout(title='Top 10 Stagnated SKUs',
                    xaxis_title='ProductCode',
                    yaxis_title='Quantity Difference',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))

    return fig

def plot_category_quantity_change(current_df, previous_df):
    # Group the DataFrames by category and sum their quantities
    current_quantities = current_df.groupby('Category')['Quantity'].sum().reset_index()
    previous_quantities = previous_df.groupby('Category')['Quantity'].sum().reset_index()

    # Merge the two DataFrames on the 'Category' column
    category_difference = current_quantities.merge(
        previous_quantities, on='Category', how='left', suffixes=('_current', '_previous')
    ).fillna(0)

    # Calculate the quantity difference for each category
    category_difference['Quantity_difference'] = category_difference['Quantity_current'] - category_difference['Quantity_previous']

    # Create a bar plot using Plotly
    fig = go.Figure(go.Bar(x=category_difference['Category'], y=category_difference['Quantity_difference'], marker=dict(color='purple')))
    fig.update_layout(title='Change in Total Quantity for Each Category',
                    xaxis_title='Category',
                    yaxis_title='Quantity Change',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))

    return fig

def plot_category_value_change(current_df, previous_df):
    # Calculate the total value for each item
    current_df['TotalValue'] = current_df['Quantity'] * current_df['AverageCost']
    previous_df['TotalValue'] = previous_df['Quantity'] * previous_df['AverageCost']

    # Group the DataFrames by category and sum their total values
    current_values = current_df.groupby('Category')['TotalValue'].sum().reset_index()
    previous_values = previous_df.groupby('Category')['TotalValue'].sum().reset_index()

    # Merge the two DataFrames on the 'Category' column
    category_difference = current_values.merge(
        previous_values, on='Category', how='left', suffixes=('_current', '_previous')
    ).fillna(0)

    # Calculate the value difference for each category
    category_difference['Value_difference'] = category_difference['TotalValue_current'] - category_difference['TotalValue_previous']

    # Create a bar plot using Plotly
    fig = go.Figure(go.Bar(x=category_difference['Category'], y=category_difference['Value_difference'], marker=dict(color='orange')))
    fig.update_layout(title='Change in Total Value based off Average Cost for Each Category',
                    xaxis_title='Category',
                    yaxis_title='Value Change (ZAR)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))

    return fig



