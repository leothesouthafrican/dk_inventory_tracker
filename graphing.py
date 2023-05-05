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



