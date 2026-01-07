import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

DATA_PATH = "processed_sales.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

# -----------------------------
# Load + clean data
# -----------------------------
df = pd.read_csv(DATA_PATH)

df.columns = [c.strip().lower() for c in df.columns]

# Parse date
df["date"] = pd.to_datetime(df["date"])

# Normalize region text (just in case)
df["region"] = df["region"].astype(str).str.strip().str.lower()

# Make sure sales is numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Drop bad rows (if any)
df = df.dropna(subset=["sales", "date", "region"])

def build_figure(selected_region: str):
    # Filter
    if selected_region == "all":
        plot_df = (
            df.groupby("date", as_index=False)["sales"]
            .sum()
            .sort_values("date")
        )
        title = "Pink Morsel Sales Over Time (All Regions)"
    else:
        plot_df = (
            df[df["region"] == selected_region]
            .groupby("date", as_index=False)["sales"]
            .sum()
            .sort_values("date")
        )
        title = f"Pink Morsel Sales Over Time ({selected_region.title()})"

    # Build line chart
    fig = px.line(
        plot_df,
        x="date",
        y="sales",
        title=title,
        labels={"date": "Date", "sales": "Total Sales ($)"},
        template="plotly_white",
    )


    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE,
        x1=PRICE_INCREASE_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(width=2, dash="dash"),
    )

    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (2021-01-15)",
        showarrow=False,
        yanchor="bottom",
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=80, b=40),
        height=520,
    )

    return fig


# -----------------------------
# Dash app
# -----------------------------
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "30px 20px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "marginBottom": "8px"},
        ),
        html.P(
            "Filter by region. Select 'All' to see total sales across all regions.",
            style={"textAlign": "center", "marginTop": "0", "color": "#444"},
        ),

        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "margin": "18px 0 10px 0",
                "padding": "14px",
                "borderRadius": "12px",
                "border": "1px solid #e6e6e6",
                "background": "#fafafa",
            },
            children=[
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"fontSize": "16px"},
                    inputStyle={"marginRight": "6px", "marginLeft": "14px"},
                )
            ],
        ),

        html.Div(
            style={
                "border": "1px solid #e6e6e6",
                "borderRadius": "12px",
                "padding": "10px",
                "background": "white",
            },
            children=[
                dcc.Graph(
                    id="sales-graph",
                    figure=build_figure("all"),
                    config={"displayModeBar": True},
                )
            ],
        ),
    ],
)

@app.callback(
    Output("sales-graph", "figure"),
    Input("region-radio", "value"),
)
def update_graph(selected_region):
    return build_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)
