"""
Project: OptiManu long term capacity planning
File: 01_data_preparation.py
Purpose: Load and validate input datasets, clean types, and export clean copies if needed

Confidentiality notice:
The company name and all data used in this project are anonymized and
modified for educational and portfolio purposes only.
No real or proprietary company information is disclosed.

Author: Abdoulaye Diop
Date: 12 May 2024
"""

from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")


def load_business_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "Year" not in df.columns:
        raise ValueError("Business data must contain a Year column")

    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = df["Year"].astype(int)
    df = df.set_index("Year").sort_index()

    if df.index.has_duplicates:
        raise ValueError("Business data contains duplicate years")

    required_cols = [
        "Forecasted Demand",
        "Operational Cost (USD)",
        "Required Labor Hours",
        "Required Machinery Hours",
        "Average Wage (USD)",
        "Workforce Size",
        "Labor Market Tightness",
        "Expected Total Revenue (USD)",
        "Expected Raw Material Cost (USD)",
        "Expected Compliance Cost (USD)",
        "Expected Environmental Compliance Cost (USD)",
        "Expected Labor Law Changes Impact Cost (USD)",
        "Expected Technology Investment Cost (USD)",
        "Annual Budget (USD)",
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Business data missing columns: {missing}")

    return df


def load_expansion_costs(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "Proposed Expansion" not in df.columns:
        raise ValueError("Expansion costs must contain a Proposed Expansion column")

    df = df.dropna(how="any").copy()
    df = df.set_index("Proposed Expansion").sort_index()

    required_cols = [
        "Cost (USD)",
        "Time to Build (year)",
        "Additional Capacity (units)",
        "Efficiency Gain",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Expansion costs missing columns: {missing}")

    df["Time to Build (year)"] = df["Time to Build (year)"].astype(int)

    if (df["Time to Build (year)"] < 0).any():
        raise ValueError("Time to build must be non negative")

    return df


def main() -> None:
    business_path = DATA_DIR / "Business_Planning_Data_2014_2024.csv"
    expansion_path = DATA_DIR / "Expansion_Costs.csv"

    business = load_business_data(business_path)
    expansions = load_expansion_costs(expansion_path)

    print("Loaded business data shape:", business.shape)
    print("Loaded expansion costs shape:", expansions.shape)

    years = list(business.index)
    print("Planning years:", years[0], "to", years[-1])
    print("Expansion options:", len(expansions.index))


if __name__ == "__main__":
    main()
