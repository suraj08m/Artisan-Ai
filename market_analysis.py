import pandas as pd


def analyze_market(product):

    df = pd.read_csv("dataset.csv")

    df["product"] = df["product"].str.lower()

    product_data = df[df["product"].str.contains(product.lower(), na=False)]

    if product_data.empty:
        return {
            "best_platform": "Unknown",
            "suggested_price": 0,
            "estimated_profit": 0,
            "profit_margin": 0,
            "demand": "Unknown",
            "competition": "Unknown",
            "market_fit": 0
        }

    best_platform_row = product_data.sort_values(
        by="sales",
        ascending=False
    ).iloc[0]

    best_platform = best_platform_row["platform"]

    avg_price = product_data["price"].mean()

    estimated_cost = avg_price * 0.6
    estimated_profit = avg_price - estimated_cost
    profit_margin = (estimated_profit / avg_price) * 100

    avg_sales = product_data["sales"].mean()

    if avg_sales > 150:
        demand = "High"
    elif avg_sales > 80:
        demand = "Medium"
    else:
        demand = "Low"

    listings = len(product_data)

    if listings >= 4:
        competition = "High"
    elif listings >= 2:
        competition = "Medium"
    else:
        competition = "Low"

    # ---- Market Fit Score ----

    demand_score = {
        "High": 40,
        "Medium": 25,
        "Low": 10
    }.get(demand, 15)

    competition_score = {
        "Low": 25,
        "Medium": 15,
        "High": 5
    }.get(competition, 10)

    profit_score = min(25, profit_margin / 2)

    sales_score = min(10, avg_sales / 20)

    market_fit = round(
        demand_score +
        competition_score +
        profit_score +
        sales_score
    )

    market_fit = max(0, min(100, market_fit))

    return {
        "best_platform": best_platform,
        "suggested_price": round(avg_price, 2),
        "estimated_profit": round(estimated_profit, 2),
        "profit_margin": round(profit_margin, 2),
        "demand": demand,
        "competition": competition,
        "market_fit": market_fit
    }