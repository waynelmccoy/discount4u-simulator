# app.py (fixed: allow_duplicate on event-modal.style for confirm & cancel)
from dash import Dash, html, dcc, Input, Output, State, ALL, ctx
import os

import pandas as pd
from dash.exceptions import PreventUpdate
from data_generation import generate_data
from components import (
    opening_message, post_start_message, raw_data_table,
    kpi_cards, compact_amounts_and_changes, single_pie
)
from events_config import EVENTS
from events_engine import apply_transform
from dash import callback
import threading
GLOBAL_CONTROL = {"unlocked_weeks": {str(w): False for w in range(2,8)}}
GLOBAL_LOCK = threading.Lock()


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "Business Intelligence for Operational Management – Discount4U Simulation"

app.layout = html.Div([
    html.Header([
        html.H1("Business Intelligence for Operational Management Decision-Making", className="app-title"),
        html.H3("Discount 4U Clothing Store Simulation", className="app-subtitle")
    ], className="app-header"),

    html.Main([
        opening_message(),
        html.Div([
            html.Button("Display Data", id="start-btn", className="start-btn"),
            dcc.Store(id="data-store"),
            dcc.Store(id="sim-state", storage_type="local"),
            dcc.Store(id="instructor-control", storage_type="local"),
            dcc.Store(id="active-event"),
        dcc.Interval(id="poll-unlock", interval=4000, n_intervals=0),
            dcc.Download(id="download-raw"),
        ], className="start-row"),
        html.Div(id="post-start-msg"),
        html.Div(id="data-and-charts"),
        html.Hr(),
        html.Div(id="events-ui", children=[
            html.H3("Weekly Operational Events (Weeks 2–7)", className="section-title"),
            html.Div([
                html.Button(f"Week {w} Event", id={"type": "week-btn", "week": w}, n_clicks=0, disabled=True,
                            className="week-btn") for w in range(2, 8)
            ], className="controls-row"),
            html.Div(id="student-feedback", className="card", style={"display": "none"}),
            html.Details([
                html.Summary("Instructor Controls"),
                html.Div([
                    html.Div([
                        html.Label("Enter PIN"),
                        dcc.Input(id="instructor-pin", type="password", placeholder="PIN", debounce=True),
                        html.Button("Enter", id="enter-pin", n_clicks=0),
                        html.Div(id="role-status", className="highlight-text")
                    ], className="control"),
                    html.Div([
                        html.Label("Unlock Weeks"),
                        dcc.Checklist(
                            id="unlock-weeks",
                            options=[{"label": f"Week {w}", "value": str(w)} for w in range(2,8)],
                            value=[],
                            inline=True, className="checklist"
                        )
                    ], className="control"),
                    html.Div([
                        html.Label("Instructor notes for the last decision"),
                        dcc.Textarea(id="instructor-notes", style={"width": "100%", "height": "90px"}),
                        html.Button("Save notes", id="save-notes", n_clicks=0)
                    ], className="control")
                ], className="controls-col")
            ], open=False, className="card"),
        ], className="card"),
        html.Div(id="event-modal", style={"display": "none"}, className="modal",
                 children=html.Div(className="modal-content", children=[
                     html.H4(id="event-title"),
                     html.P(id="event-description"),
                     dcc.RadioItems(id="event-choice", options=[], value=None, className="radio"),
                     html.Div([
                         html.Button("Confirm selection", id="confirm-choice", n_clicks=0, className="primary"),
                         html.Button("Cancel", id="cancel-choice", n_clicks=0, className="secondary")
                     ], className="controls-row")
                 ])
        ),
    ], className="app-main"),

    html.Footer([
        html.Div("© 2025 Discount4U (Mock) – For instructional use.", className="footer-text")
    ], className="app-footer")
], className="app-container")

@callback(
    Output("data-store", "data"),
    Output("post-start-msg", "children"),
    Output("download-raw", "data"),
    Input("start-btn", "n_clicks"),
    prevent_initial_call=True,
)
def on_start(n):
    df = generate_data()
    return (
        df.to_dict("records"),
        post_start_message(),
        dcc.send_data_frame(pd.DataFrame(df).to_csv, "discount4u_raw_data.csv", index=False),
    )

@callback(
    Output("sim-state", "data"),
    Output("instructor-control", "data"),
    Input("data-store", "data"),
    prevent_initial_call=True
)
def init_sim_state(data_records):
    if not data_records:
        raise PreventUpdate
    return (
        {"week": 1, "data": data_records, "history": [], "completed_weeks": []},
        {"role": "student", "unlocked_weeks": {str(w): False for w in range(2,8)}}
    )

@callback(
    Output("data-and-charts", "children"),
    Input("data-store", "data"),
    prevent_initial_call=True,
)
def render_charts(data_records):
    if not data_records:
        raise PreventUpdate
    df = pd.DataFrame(data_records)
    months = sorted(df["Month"].unique().tolist())
    latest_month = months[-1]
    items = sorted(df["Item"].unique().tolist())

    kpi_controls = html.Div([
        html.Div([
            html.Label("KPI Scope"),
            dcc.RadioItems(
                id="kpi-scope",
                options=[{"label": "12 Months", "value": "12m"}, {"label": "Last Month", "value": "lm"}],
                value="12m",
                inline=True,
                className="radio",
            ),
        ], className="control"),
    ], className="controls-row")

    pie_controls = html.Div([
        html.Div([
            html.Label("Pie Metric"),
            dcc.RadioItems(
                id="pie-metric",
                options=[{"label": "Quantity", "value": "Sales Quantity"}, {"label": "Revenue", "value": "Sales Revenue"}],
                value="Sales Quantity",
                inline=True,
                className="radio",
            ),
        ], className="control"),
        html.Div([
            html.Label("Month"),
            dcc.Dropdown(id="pie-month", options=[{"label": m, "value": m} for m in months], value=latest_month, clearable=False),
        ], className="control"),
    ], className="controls-col")
    pie_section = html.Div([
        html.Div(pie_controls, className="section-controls"),
        html.Div(dcc.Graph(id="pie-graph", config={"displayModeBar": False}, responsive=True, style={"height": "380px"}), className="section-graph"),
    ], className="section-grid pie-section card")

    compact_controls = html.Div([
        html.Div([
            html.Label("Item (for Compact Chart)"),
            dcc.Dropdown(
                id="compact-item",
                options=[{"label": "All Items (Total)", "value": "ALL"}] + [{"label": it, "value": it} for it in items],
                value="ALL",
                clearable=False,
            ),
        ], className="control"),
        html.Div([
            html.Label("Compact Metrics"),
            dcc.Checklist(
                id="compact-metrics",
                options=[{"label": "Qty", "value": "qty"}, {"label": "Revenue", "value": "revenue"}, {"label": "Profit", "value": "profit"}, {"label": "Inventory", "value": "inventory"}],
                value=["qty", "revenue", "profit", "inventory"],
                inline=True,
                className="checklist",
            ),
        ], className="control"),
        html.Div([
            html.Label("MoM Range ±%"),
            dcc.Dropdown(id="mom-range", options=[{"label": str(v), "value": v} for v in [20, 40, 60]], value=60, clearable=False),
        ], className="control"),
    ], className="controls-col")
    compact_section = html.Div([
        html.Div(compact_controls, className="section-controls"),
        html.Div(dcc.Graph(id="compact-graph", responsive=True, style={"height": "460px"}), className="section-graph"),
    ], className="section-grid compact-section card")

    table_block = html.Div([
        html.H3("Raw Data (12 months × 7 items)", className="section-title"),
        raw_data_table(df)
    ], className="card table-card")

    return html.Div([
        html.Div([kpi_controls], className="card controls-card"),
        html.Div(id="kpi-cards", className="card kpis-card"),
        pie_section,
        compact_section,
        table_block,
    ], className="stack")

@callback(
    Output("kpi-cards", "children"),
    Input("sim-state", "data"),
    Input("kpi-scope", "value"),
    Input("pie-month", "value"),
    Input("data-and-charts", "children"),
)
def update_kpis(sim_state, scope, month, _children):
    if not sim_state or not sim_state.get("data"):
        raise PreventUpdate
    df = pd.DataFrame(sim_state["data"])
    dff = df[df["Month"] == month] if scope == "lm" else df
    revenue_total = dff["Sales Revenue"].sum()
    profit_total = dff["Profit"].sum()
    rev = dff["Sales Revenue"].sum()
    gm = 0.0 if rev == 0 else (rev - dff["COGS"].sum()) / rev * 100.0
    avg_inv = dff["Inventory Quantity"].mean()
    marketing_total = dff["Marketing Dollars"].sum()
    return kpi_cards(revenue_total, profit_total, gm, avg_inv, marketing_total)

@callback(
    Output("pie-graph", "figure"),
    Input("sim-state", "data"),
    Input("pie-month", "value"),
    Input("pie-metric", "value"),
    Input("data-and-charts", "children"),
)
def update_pie(sim_state, month, metric, _children):
    if not sim_state or not sim_state.get("data"):
        raise PreventUpdate
    df = pd.DataFrame(sim_state["data"])
    return single_pie(df, month, metric)

@callback(
    Output("compact-graph", "figure"),
    Input("sim-state", "data"),
    Input("compact-metrics", "value"),
    Input("mom-range", "value"),
    Input("compact-item", "value"),
    Input("data-and-charts", "children"),
)
def update_compact(sim_state, metrics_on, mom_range, item_scope, _children):
    if not sim_state or not sim_state.get("data"):
        raise PreventUpdate
    df = pd.DataFrame(sim_state["data"])
    label = "All Items (Total)"
    if item_scope and item_scope != "ALL":
        df = df[df["Item"] == item_scope]
        label = item_scope
    return compact_amounts_and_changes(df, metrics_on=metrics_on, mom_range=mom_range, label=label)

PIN = os.environ.get("INSTRUCTOR_PIN", "D4U2025")

@callback(
    Output("instructor-control", "data", allow_duplicate=True),
    Output("role-status", "children"),
    Input("enter-pin", "n_clicks"),
    State("instructor-pin", "value"),
    State("instructor-control", "data"),
    prevent_initial_call=True
)
def set_instructor_role(n, pin, icontrol):
    if not icontrol:
        raise PreventUpdate
    role = "instructor" if pin == PIN else "student"
    icontrol["role"] = role
    status = "Role: INSTRUCTOR" if role == "instructor" else "Role: STUDENT (invalid PIN)"
    return icontrol, status

@callback(
    Output("instructor-control", "data", allow_duplicate=True),
    Input("unlock-weeks", "value"),
    State("instructor-control", "data"),
    prevent_initial_call=True
)
def update_unlock_weeks(selected, icontrol):
    if not icontrol or icontrol.get("role") != "instructor":
        raise PreventUpdate
    allowed = {str(w): (str(w) in set(selected or [])) for w in range(2,8)}
    icontrol["unlocked_weeks"] = allowed
    with GLOBAL_LOCK:
        GLOBAL_CONTROL["unlocked_weeks"] = allowed
    return icontrol

@callback(
    Output({"type": "week-btn", "week": ALL}, "disabled"),
    Input("sim-state", "data"),
    Input("instructor-control", "data"),
    prevent_initial_call=True
)


def control_week_buttons(sim_state, icontrol, _n):
    if not sim_state:
        return [True] * 6
    with GLOBAL_LOCK:
        unlocked = GLOBAL_CONTROL.get("unlocked_weeks", {})
    completed = set(sim_state.get("completed_weeks", []))
    return [ (not unlocked.get(str(w), False)) or (w in completed) for w in range(2,8) ]


@callback(
    Output("event-modal", "style"),
    Output("event-title", "children"),
    Output("event-description", "children"),
    Output("event-choice", "options"),
    Output("event-choice", "value"),
    Output("active-event", "data"),
    Input({"type": "week-btn", "week": ALL}, "n_clicks"),
    State("instructor-control", "data"),
    State("sim-state", "data"),
    prevent_initial_call=True
)


def open_event(week_clicks, icontrol, sim_state):
    if not sim_state:
        raise PreventUpdate
    trigger = ctx.triggered_id
    if not isinstance(trigger, dict):
        raise PreventUpdate
    w = int(trigger.get("week"))
    with GLOBAL_LOCK:
        is_unlocked = GLOBAL_CONTROL.get("unlocked_weeks", {}).get(str(w), False)
    if (not is_unlocked) or (w in set(sim_state.get("completed_weeks", []))):
        raise PreventUpdate

    ev = EVENTS.get(str(w))
    if not ev:
        raise PreventUpdate
    options = [{"label": c["label"], "value": c["id"]} for c in ev["choices"]]
    return {"display": "block"}, ev["title"], ev["description"], options, None, {"week": w, "event_id": ev["id"]}

@callback(
    Output("sim-state", "data", allow_duplicate=True),
    Output("student-feedback", "children"),
    Output("student-feedback", "style"),
    Output("event-modal", "style", allow_duplicate=True),  # allow duplicate here
    Input("confirm-choice", "n_clicks"),
    State("event-choice", "value"),
    State("active-event", "data"),
    State("sim-state", "data"),
    prevent_initial_call=True
)
def confirm_choice(n, choice_id, active, sim_state):
    if not n or not choice_id or not active or not sim_state:
        raise PreventUpdate
    week = active["week"]
    ev = EVENTS[str(week)]
    choice = next(c for c in ev["choices"] if c["id"] == choice_id)
    df = pd.DataFrame(sim_state["data"])
    new_df, delta, auto_feedback = apply_transform(df, choice["transform"])

    feedback_html = html.Div([
        html.H4(f"Week {week}: Decision Outcome"),
        html.P(ev["description"]),
        html.H5("Your selection:"), html.P(choice["label"]),
        html.H5("Impact (latest month):"),
        html.Ul([html.Li(f"{k}: {v}") for k, v in delta.items()]),
        html.H5("Feedback:"),
        html.Ul([html.Li(x) for x in choice["student_feedback"]]),
        html.P(auto_feedback, className="highlight-text")
    ])

    history = sim_state.get("history", [])
    history.append({
        "week": week,
        "event_id": ev["id"],
        "choice": choice_id,
        "delta_summary": delta,
        "student_feedback": choice["student_feedback"],
        "instructor_notes": ""
    })
    completed = set(sim_state.get("completed_weeks", []))
    completed.add(week)
    new_state = {
        **sim_state,
        "week": max(sim_state.get("week", 1), week),
        "data": new_df.to_dict("records"),
        "history": history,
        "completed_weeks": sorted(list(completed))
    }
    return new_state, feedback_html, {"display": "block"}, {"display": "none"}

@callback(
    Output("event-modal", "style", allow_duplicate=True),  # allow duplicate here
    Input("cancel-choice", "n_clicks"),
    prevent_initial_call=True
)
def cancel_modal(n):
    if not n:
        raise PreventUpdate
    return {"display": "none"}

@callback(
    Output("sim-state", "data", allow_duplicate=True),
    Input("save-notes", "n_clicks"),
    State("instructor-notes", "value"),
    State("sim-state", "data"),
    prevent_initial_call=True
)
def save_notes(n, notes, sim_state):
    if not n or not sim_state:
        raise PreventUpdate
    hist = sim_state.get("history", [])
    if hist:
        hist[-1]["instructor_notes"] = notes or ""
    sim_state["history"] = hist
    return sim_state

if __name__ == "__main__":
    app.run(debug=True)

