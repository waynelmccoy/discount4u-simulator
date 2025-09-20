 
from dash import html, dcc 
from dash import dash_table 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 

def opening_message(): 
    return html.Div([
        html.H4("Welcome to the Discount4U Simulation", className="section-title"),
        html.P("Hello. In this scenario, you will act as the operational decision-maker for the mock Discount4U retail clothing company, which is a nationwide retail chain that sells trendy clothes."),
        html.P("You will be presented with current and historical data for 7 popular sales items. You are expected to analyze this data and form an understanding of what this data represents about these items and the company."),
        html.H5("Weekly Simulation Flow"),
        html.Ul([
            html.Li("Each week, you will be presented with an event that may or may not disrupt your operation."),
            html.Li("You will select from a list of available options to react to the event."),
            html.Li("Your choices will lead to operational stability and growth, instability and decline, or a combination of both."),
            html.Li("After each decision, you will receive updated data and feedback on the impact of your choices."),
        ]),
        html.H5("Collaboration & Feedback"),
        html.Ul([
            html.Li("Engage in discussion with classmates to provide feedback and advice."),
            html.Li("Instructor feedback may also provide insights."),
            html.Li("Use peer and instructor input to inform your decisions each week."),
        ]),
        html.H5("Objective"),
        html.P("The goal of this simulation is to provide you the opportunity to experience the importance of business intelligence for operational decision-making, as well as provide you an exercise to practice analysis and decision-making through realistic scenarios."),
        html.Div([
            "Good luck! Press the ",
            html.Strong('\"Display Data\"'),
            " button when you are ready to start the simulation."
        ], className="highlight-text")
    ], className="card")

def post_start_message(): 
    return html.Div([
        html.H4("Simulation Started", className="section-title"),
        html.P("Data generated. Use the controls to explore KPIs, the category pie, and the compact chart."),
        html.H5("Suggested Analysis Approaches"),
        html.Ul([
            html.Li("Study the data carefully to spot potential trends, potential developing problems, and opportunities for innovation or process improvements."),
            html.Li("Consider conducting a preliminary SWOT Analysis based on the data."),
            html.Li("Create your own visualizations to explore the data from different perspectives."),
        ]),
        html.P("The choice on how to study and understand the data is yours, but your preparation and comprehension of the data will be key to successfully navigating operational disruptions each week."),
        html.Div("Good luck!", className="highlight-text")
    ], className="card")

def _format_currency(x): 
    return f"${x:,.0f}"

def _format_number(x): 
    return f"{x:,.0f}"

def kpi_cards(revenue_total, profit_total, gm_pct, avg_inv, marketing_total): 
    cards = [
        ("Revenue", _format_currency(revenue_total)),
        ("Profit", _format_currency(profit_total)),
        ("Gross Margin", f"{gm_pct:.1f}%"),
        ("Avg Inventory", _format_number(avg_inv)),
        ("Marketing", _format_currency(marketing_total)),
    ]
    return html.Div([
        html.Div([
            html.Div(title, className="kpi-title"),
            html.Div(value, className="kpi-value"),
        ], className="kpi-card") for title, value in cards
    ], className="kpi-grid")

def raw_data_table(df: pd.DataFrame): 
    cols = [
        {"name": c, "id": c} for c in [
            "Month", "Item", "Category", "Sales Quantity", "Sales Revenue",
            "COGS", "Profit", "Inventory Quantity", "Marketing Dollars"
        ] if c in df.columns
    ]
    return dash_table.DataTable(
        id="raw-table",
        data=df.to_dict("records"),
        columns=cols,
        page_size=12,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"padding": "8px", "whiteSpace": "normal", "height": "auto", "fontSize": 14},
        style_header={"backgroundColor": "#f1f5f9", "fontWeight": "600", "border": "none"},
        style_data={"border": "none"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"}],
        persistence=True,
    )

def single_pie(df: pd.DataFrame, month: str, metric: str): 
    dff = df[df["Month"] == month].copy()
    if dff.empty:
        fig = go.Figure()
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return fig
    by_item = dff.groupby(["Item"], as_index=False)[metric].sum().sort_values(metric, ascending=False)
    fig = px.pie(by_item, names="Item", values=metric, hole=0.45)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), legend_title_text="Item")
    return fig

def compact_amounts_and_changes(df: pd.DataFrame, metrics_on=None, mom_range: int = 60, label: str = "All Items (Total)"):
    if metrics_on is None:
        metrics_on = ["qty", "revenue", "profit", "inventory"]
    monthly = df.groupby("Month", as_index=False).agg({
        "Sales Quantity": "sum",
        "Sales Revenue": "sum",
        "Profit": "sum",
        "Inventory Quantity": "mean",
    })
    monthly["Month_dt"] = pd.to_datetime(monthly["Month"], format="%Y-%m")
    monthly = monthly.sort_values("Month_dt")
    monthly["Revenue MoM %"] = monthly["Sales Revenue"].pct_change() * 100.0

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    color_map = {
        "qty": "#0d6efd",
        "revenue": "#198754",
        "profit": "#6f42c1",
        "inventory": "#fd7e14",
    }
    x = monthly["Month"]
    if "qty" in metrics_on:
        fig.add_trace(
            go.Scatter(
                x=x, y=monthly["Sales Quantity"], name=f"Quantity — {label}", mode="lines+markers",
                line=dict(color=color_map["qty"], width=2)
            ), secondary_y=False
        )
    if "revenue" in metrics_on:
        fig.add_trace(
            go.Scatter(
                x=x, y=monthly["Sales Revenue"], name=f"Revenue — {label}", mode="lines+markers",
                line=dict(color=color_map["revenue"], width=2)
            ), secondary_y=False
        )
    if "profit" in metrics_on:
        fig.add_trace(
            go.Scatter(
                x=x, y=monthly["Profit"], name=f"Profit — {label}", mode="lines+markers",
                line=dict(color=color_map["profit"], width=2)
            ), secondary_y=False
        )
    if "inventory" in metrics_on:
        fig.add_trace(
            go.Scatter(
                x=x, y=monthly["Inventory Quantity"], name=f"Inventory — {label}", mode="lines+markers",
                line=dict(color=color_map["inventory"], width=2)
            ), secondary_y=False
        )
    # MoM bars on secondary y
    fig.add_trace(
        go.Bar(x=x, y=monthly["Revenue MoM %"], name=f"Revenue MoM % — {label}", marker_color="#9CA3AF", opacity=0.6),
        secondary_y=True,
    )
    # Reference lines
    y_upper = [mom_range] * len(x)
    y_lower = [-mom_range] * len(x)
    fig.add_trace(go.Scatter(x=x, y=y_upper, mode='lines', name='Upper Range', line=dict(color='#9CA3AF', dash='dot'), showlegend=False), secondary_y=True)
    fig.add_trace(go.Scatter(x=x, y=y_lower, mode='lines', name='Lower Range', line=dict(color='#9CA3AF', dash='dot'), showlegend=False), secondary_y=True)

    y2_abs = monthly["Revenue MoM %"].abs().max()
    y2_abs = 0.0 if pd.isna(y2_abs) else float(y2_abs)
    y2_max = max(mom_range, y2_abs)
    y2_max = max(10, min(200, y2_max))

    fig.update_yaxes(title_text="Amounts", secondary_y=False)
    fig.update_yaxes(title_text="MoM %", range=[-y2_max, y2_max], secondary_y=True, zeroline=True, zerolinecolor="#9CA3AF")
    fig.update_layout(
        title=dict(text=f"Compact View — {label}", x=0.01, xanchor='left'),
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=40, b=0),
        hovermode="x unified",
    )
    return fig
