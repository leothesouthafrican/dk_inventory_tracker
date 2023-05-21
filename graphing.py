import plotly.graph_objs as go
import pandas as pd

def plot_items_per_category(df: pd.DataFrame) -> go.Figure:
    """
    Plot the number of unique SKUs per category in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.

    Returns:
        go.Figure: The Plotly figure object.
    """
    items_per_category = df.groupby('Category')['ProductCode'].count().sort_values()

    fig = go.Figure(go.Bar(x=items_per_category.index, y=items_per_category.values, marker=dict(color='green')))
    fig.update_layout(
        autosize=True,
        margin=dict(l=30, r=30, t=30, b=30),
        title='Number of Unique SKUs per Category',
        yaxis_title='Number of Unique SKUs'
    )
    return fig

def plot_quantity_per_category(df: pd.DataFrame) -> go.Figure:
    """
    Plot the total quantity of items per category in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.

    Returns:
        go.Figure: The Plotly figure object.
    """
    quantity_per_category = df.groupby('Category')['Quantity'].sum().sort_values()

    fig = go.Figure(go.Bar(x=quantity_per_category.index, y=quantity_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Total Quantity of Items per Category',
                    yaxis_title='Total Quantity',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_total_value_per_category(df: pd.DataFrame) -> go.Figure:
    """
    Plot the total value based off average cost per category in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.

    Returns:
        go.Figure: The Plotly figure object.
    """
    df['TotalValue'] = df['AverageCost'] * df['Quantity']
    total_value_per_category = df.groupby('Category')['TotalValue'].sum().sort_values()

    fig = go.Figure(go.Bar(x=total_value_per_category.index, y=total_value_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Total Value based off Average Cost per Category',
                    yaxis_title='Total Value (ZAR)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_unrealised_value_per_category(df: pd.DataFrame) -> go.Figure:
    """
    Plot the unrealised gross profit per category in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.

    Returns:
        go.Figure: The Plotly figure object.
    """
    df['UnrealisedValue'] = (df['PriceTier1'] - df['AverageCost']) * df['Quantity']
    unrealised_value_per_category = df.groupby('Category')['UnrealisedValue'].sum().sort_values()

    fig = go.Figure(go.Bar(x=unrealised_value_per_category.index, y=unrealised_value_per_category.values, marker=dict(color='green')))
    fig.update_layout(title='Unrealised Gross Profit per Category',
                    yaxis_title='Unrealised Gross Profit (ZAR)',
                    autosize=True,
                    margin=dict(l=30, r=30, t=30, b=30))
    return fig

def avg_gross_margin_per_category(df: pd.DataFrame) -> go.Figure:
    """
    Plot the average gross margin per category in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.

    Returns:
        go.Figure: The Plotly figure object.
    """
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

def plot_decreased_items(df: pd.DataFrame, top_n: int) -> go.Figure:
    """
    Plot the items that have decreased the most in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.
        top_n (int): Number of top items to display.

    Returns:
        go.Figure: The Plotly figure object.
    """
    decreased_items = df[df['QuantityChange'] < 0].groupby('ProductCode')['QuantityChange'].sum()
    # Sorting the values in ascending order so the most decreased items will be on the right
    decreased_items = decreased_items.sort_values(ascending=False)

    # Getting the top_n items
    decreased_items = decreased_items.tail(top_n)

    fig = go.Figure(go.Bar(x=decreased_items.index, y=decreased_items.values, marker=dict(color='purple')))
    fig.update_layout(title='Most Sold Items',
                      xaxis_title='Product Code',
                      yaxis_title='Quantity Sold',
                      autosize=True,
                      margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_gross_profit(df: pd.DataFrame, top_n: int) -> go.Figure:
    """
    Plot the items that have produced the most gross profit in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.
        top_n (int): Number of top items to display.

    Returns:
        go.Figure: The Plotly figure object.
    """
    # Calculating gross profit for each product
    df['GrossProfit'] = (df['PriceTier4'] - df['AverageCost']) * (df['QuantityChange']**2)**0.5

    gross_profit_items = df.groupby('ProductCode')['GrossProfit'].sum()
    # Sorting the values in ascending order so the most profitable items will be on the right
    gross_profit_items = gross_profit_items.sort_values(ascending=True)

    # Getting the top_n items
    gross_profit_items = gross_profit_items.tail(top_n)

    fig = go.Figure(go.Bar(x=gross_profit_items.index, y=gross_profit_items.values, marker=dict(color='purple')))
    fig.update_layout(title='Most Profitable (Gross) Items',
                      xaxis_title='Product Code',
                      yaxis_title='Gross Profit',
                      autosize=True,
                      margin=dict(l=30, r=30, t=30, b=30))
    return fig

def plot_least_sold_categories(df: pd.DataFrame, top_n: int) -> go.Figure:
    """
    Plot the categories that are stagnating (not increasing but decreasing the least) in a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame to plot.
        top_n (int): Number of top categories to display.

    Returns:
        go.Figure: The Plotly figure object.
    """
    # Group by category and sum the quantity changes
    category_changes = df.groupby('Category')['QuantityChange'].sum()

    # Filtering the categories that are not increasing
    decreasing_categories = category_changes[category_changes <= 0]

    # Sorting the categories by quantity change in ascending order 
    # So, the categories that are decreasing the least will be on the top
    least_decreasing_categories = decreasing_categories.sort_values(ascending=False)

    # Selecting the top_n categories
    least_decreasing_categories = least_decreasing_categories.head(top_n)

    fig = go.Figure(go.Bar(x=least_decreasing_categories.index, y=least_decreasing_categories.values, marker=dict(color='purple')))
    fig.update_layout(title='Least Sold Categories',
                      xaxis_title='Category',
                      yaxis_title='Quantity Change',
                      autosize=True,
                      margin=dict(l=30, r=30, t=30, b=30))
    return fig