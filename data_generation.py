 
import pandas as pd 
import numpy as np 

def generate_data(seed: int = 42) -> pd.DataFrame:
    """
    Generate 12 months of store data for 7 items.
    Columns: Month, Item, Category, Sales Quantity, Sales Revenue, COGS, Profit, Inventory Quantity, Marketing Dollars
    """
    rng = np.random.default_rng(seed)
    items = [
        ("Jeans", "Bottoms", 55.0, 0.55),
        ("T-Shirts", "Tops", 18.0, 0.45),
        ("Jackets", "Outerwear", 90.0, 0.60),
        ("Shoes", "Footwear", 75.0, 0.58),
        ("Dresses", "Dresses", 70.0, 0.57),
        ("Accessories", "Accessories", 15.0, 0.40),
        ("Hoodies", "Tops", 48.0, 0.52),
    ]
    end = pd.Timestamp.today().normalize().to_period("M").to_timestamp()
    months = pd.period_range(end=end, periods=12, freq="M")
    rows = []
    seasonal = {m: 0.9 + 0.2 * np.sin(i / 12 * 2 * np.pi) for i, m in enumerate(months)}
    for m in months:
        monthly_marketing_pool = rng.uniform(800, 1600)
        marketing_allocations = rng.dirichlet(np.ones(len(items))) * monthly_marketing_pool
        for (item, cat, price, cost_ratio), mkt in zip(items, marketing_allocations):
            base_demand = rng.normal(300, 80)
            season_factor = seasonal[m]
            promo_factor = 1.0 + (mkt / monthly_marketing_pool) * 0.3 if monthly_marketing_pool > 0 else 1.0
            qty = max(0, int(base_demand * season_factor * promo_factor + rng.normal(0, 15)))
            revenue = qty * price
            cogs = qty * price * cost_ratio
            profit = revenue - cogs - mkt
            inv_qty = max(0, int(qty * rng.uniform(0.4, 0.9) + rng.normal(0, 20)))
            rows.append({
                "Month": m.strftime("%Y-%m"),
                "Item": item,
                "Category": cat,
                "Sales Quantity": qty,
                "Sales Revenue": round(revenue, 2),
                "COGS": round(cogs, 2),
                "Profit": round(profit, 2),
                "Inventory Quantity": inv_qty,
                "Marketing Dollars": round(mkt, 2),
            })
    df = pd.DataFrame(rows)
    return df
