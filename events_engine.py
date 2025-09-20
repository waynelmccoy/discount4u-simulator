# events_engine.py
import pandas as pd
import numpy as np
from typing import Dict, Any

def _latest_month(df: pd.DataFrame) -> str:
    months = pd.to_datetime(df["Month"], format="%Y-%m")
    return months.max().strftime("%Y-%m")

def _add_unit_cols(dff: pd.DataFrame) -> pd.DataFrame:
    dff = dff.copy()
    qty = dff["Sales Quantity"].replace(0, np.nan)
    dff["unit_price"] = dff["Sales Revenue"] / qty
    dff["unit_cost"]  = dff["COGS"] / qty
    dff["unit_price"] = dff["unit_price"].fillna(dff["unit_price"].median())
    dff["unit_cost"]  = dff["unit_cost"].fillna(dff["unit_cost"].median())
    return dff

def _recalc_financials(dff: pd.DataFrame) -> pd.DataFrame:
    dff = dff.copy()
    dff["Sales Revenue"] = (dff["Sales Quantity"] * dff["unit_price"]).round(2)
    dff["COGS"]          = (dff["Sales Quantity"] * dff["unit_cost"]).round(2)
    dff["Profit"]        = (dff["Sales Revenue"] - dff["COGS"] - dff["Marketing Dollars"]).round(2)
    return dff

def _delta_summary(before: pd.DataFrame, after: pd.DataFrame) -> Dict[str, Any]:
    keys = ["Sales Quantity", "Sales Revenue", "COGS", "Profit", "Inventory Quantity", "Marketing Dollars"]
    b = before[keys].sum(numeric_only=True)
    a = after[keys].sum(numeric_only=True)
    d = (a - b).to_dict()
    d["Revenue %"] = float(((a["Sales Revenue"] - b["Sales Revenue"]) / b["Sales Revenue"]) * 100.0) if b["Sales Revenue"] else 0.0
    d["Profit %"]  = float(((a["Profit"] - b["Profit"]) / b["Profit"]) * 100.0) if b["Profit"] else 0.0
    return {k: (round(v, 2) if isinstance(v, (int, float, np.floating)) else v) for k, v in d.items()}

def _apply_on_latest(df: pd.DataFrame, mask: pd.Series, *,
                     qty_mult: float = 1.0,
                     price_mult: float = 1.0,
                     cost_mult: float = 1.0,
                     inv_delta_pct: float = 0.0,
                     mkt_delta_mult: float = 1.0) -> pd.DataFrame:
    latest = _latest_month(df)
    dff = df.copy()
    latest_mask = dff["Month"].eq(latest) & mask
    dff = _add_unit_cols(dff)
    dff.loc[latest_mask, "Sales Quantity"] = (dff.loc[latest_mask, "Sales Quantity"] * qty_mult).round().astype(int)
    dff.loc[latest_mask, "unit_price"]     = dff.loc[latest_mask, "unit_price"] * price_mult
    dff.loc[latest_mask, "unit_cost"]      = dff.loc[latest_mask, "unit_cost"] * cost_mult
    dff.loc[latest_mask, "Marketing Dollars"] = (dff.loc[latest_mask, "Marketing Dollars"] * mkt_delta_mult).round(2)
    dff.loc[latest_mask, "Inventory Quantity"] = (
        dff.loc[latest_mask, "Inventory Quantity"] * (1.0 + inv_delta_pct)
    ).round().astype(int)
    dff = _recalc_financials(dff)
    return dff.drop(columns=["unit_price", "unit_cost"])  # cleanup

def _before_after(df):
    latest = _latest_month(df)
    return df[df["Month"].eq(latest)].copy(), latest

# Week 2

def w2_A_expedite_40(df: pd.DataFrame):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops")
    out = _apply_on_latest(df, tops, qty_mult=1.08, cost_mult=1.03, inv_delta_pct=0.05)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "You protected Tops availability via expedited freight, but incurred higher unit costs."

def w2_B_shift_demand_markdown(df: pd.DataFrame):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops"); non_tops = ~tops
    df2 = _apply_on_latest(df, tops, qty_mult=0.90)
    out = _apply_on_latest(df2, non_tops, qty_mult=1.06, price_mult=0.95, inv_delta_pct=-0.04)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "You shifted demand using markdowns; margin compression offset some volume gains."

def w2_C_partial_substitute(df: pd.DataFrame):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops")
    out = _apply_on_latest(df, tops, qty_mult=1.03, cost_mult=1.08, inv_delta_pct=-0.02)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Alternate supplier improved availability slightly at a higher cost; watch quality/returns."

# Week 3

def w3_A_boost_demand_ads(df):
    before, latest = _before_after(df); bottoms = df["Category"].eq("Bottoms")
    out = _apply_on_latest(df, bottoms, qty_mult=1.10, mkt_delta_mult=1.20, inv_delta_pct=-0.03)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Advertising captured the heat-wave demand for Shorts; higher marketing spend trimmed profit."

def w3_B_limit_per_customer(df):
    before, latest = _before_after(df); bottoms = df["Category"].eq("Bottoms")
    out = _apply_on_latest(df, bottoms, qty_mult=0.95, inv_delta_pct=0.04)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Purchase limits protected availability but reduced overall units sold slightly."

def w3_C_crossdock(df):
    before, latest = _before_after(df); bottoms = df["Category"].eq("Bottoms")
    out = _apply_on_latest(df, bottoms, qty_mult=1.06, cost_mult=1.01, inv_delta_pct=-0.05)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Cross-docking matched supply to demand; minor cost, improved sell-through."

# Week 4

def w4_A_rework_quality(df):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops")
    out = _apply_on_latest(df, tops, cost_mult=1.02, inv_delta_pct=-0.02)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Quality rework contained the issue and protected brand equity with minor cost impact."

def w4_B_clearance(df):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops")
    out = _apply_on_latest(df, tops, price_mult=0.80, qty_mult=1.12, inv_delta_pct=-0.12)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Clearance moved affected inventory quickly but at a steep margin cost."

def w4_C_credit_pause(df):
    before, latest = _before_after(df); tops = df["Category"].eq("Tops")
    out = _apply_on_latest(df, tops, cost_mult=0.95, qty_mult=0.94, inv_delta_pct=-0.06)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "You recovered some costs via supplier credit but reduced available assortment temporarily."

# Week 5

def w5_A_hedge(df):
    before, latest = _before_after(df); mask = df["Category"].isin(["Tops","Bottoms"])
    out = _apply_on_latest(df, mask, cost_mult=1.06, mkt_delta_mult=1.05)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Hedging reduced cost volatility with a modest fee; profit impact is buffered."

def w5_B_price_up(df):
    before, latest = _before_after(df); mask = df["Category"].isin(["Tops","Bottoms"])
    out = _apply_on_latest(df, mask, price_mult=1.028, qty_mult=0.97, inv_delta_pct=0.02)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Pricing action protected GM$ with a small demand contraction."

def w5_C_blend_substitute(df):
    before, latest = _before_after(df); mask = df["Category"].isin(["Tops","Bottoms"])
    out = _apply_on_latest(df, mask, cost_mult=1.03, qty_mult=0.99, inv_delta_pct=-0.01)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Material substitution contained costs with minimal demand impact."

# Week 6

def w6_A_temp_staff(df):
    before, latest = _before_after(df); mask = df["Month"].eq(latest)
    out = _apply_on_latest(df, mask, qty_mult=1.02, mkt_delta_mult=1.04, inv_delta_pct=-0.02)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Temporary staffing improved service levels at a modest cost."

def w6_B_prioritize_top(df):
    before, latest = _before_after(df); last = df[df["Month"].eq(latest)].copy()
    top_items = last.groupby("Item")["Sales Quantity"].sum().nlargest(3).index.tolist()
    high = df["Item"].isin(top_items); low = ~high
    df2 = _apply_on_latest(df, high, qty_mult=1.05, inv_delta_pct=-0.03)
    out = _apply_on_latest(df2, low, qty_mult=0.97, inv_delta_pct=0.02)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "You focused capacity on top items; tail performance softened slightly."

def w6_C_dropship(df):
    before, latest = _before_after(df); mask = df["Month"].eq(latest)
    out = _apply_on_latest(df, mask, qty_mult=1.02, cost_mult=1.015)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Drop-ship reduced DC load and improved speed for a subset, with slightly higher cost."

# Week 7

def w7_A_counter_promo(df):
    before, latest = _before_after(df); mask = df["Category"].isin(["Tops","Bottoms","Accessories"])
    out = _apply_on_latest(df, mask, price_mult=0.95, qty_mult=1.08, inv_delta_pct=-0.05, mkt_delta_mult=1.05)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Counter-promo defended share with a trade-off in margin percentage."

def w7_B_differentiate(df):
    before, latest = _before_after(df); premium = df["Category"].isin(["Outerwear","Footwear","Dresses"]); tail = df["Category"].isin(["Accessories"])
    df2 = _apply_on_latest(df, premium, price_mult=1.06, qty_mult=0.98)
    out = _apply_on_latest(df2, tail, inv_delta_pct=-0.10, qty_mult=0.98)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Assortment focused on premium; GM$ stabilized despite softer units."

def w7_C_experience_led(df):
    before, latest = _before_after(df); mask = df["Month"].eq(latest)
    out = _apply_on_latest(df, mask, qty_mult=1.04, mkt_delta_mult=1.08, inv_delta_pct=-0.03)
    return out, _delta_summary(before, out[out["Month"].eq(latest)]), "Experience strategy grew traffic with limited discounting; benefits may compound over time."

FUNCTIONS = {name: obj for name, obj in globals().items() if callable(obj) and name.startswith("w")}

def apply_transform(df: pd.DataFrame, transform_name: str):
    fn = FUNCTIONS.get(transform_name)
    if not fn:
        raise ValueError(f"Unknown transform: {transform_name}")
    return fn(df)
