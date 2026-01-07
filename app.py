import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load the processed sales data
df = pd.read_csv("processed_sales.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Aggregate total sales per day
daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

# Sort by date
daily_sales = daily_sales.sort_values("Date")

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales ($)"
    }
)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center"}
        ),
        dcc.Graph(
            figure=fig
        )
    ]
)

# Run the app
if __name__ == "__main__":
    app.run()


