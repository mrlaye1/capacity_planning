"""
Project: OptiManu long term capacity planning
File: 03_solve_and_report.py
Purpose: Solve the optimization model and export summary results

Confidentiality notice:
The company name and all data used in this project are anonymized and
modified for educational and portfolio purposes only.
No real or proprietary company information is disclosed.

Author: Abdoulaye Diop
Date: 12 May 2024
"""

from pathlib import Path
import pandas as pd
import pyomo.environ as pyo

from src_02_optimization_model import build_model


DATA_DIR = Path("data")
RESULTS_DIR = Path("results")


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    business = pd.read_csv(DATA_DIR / "Business_Planning_Data_2014_2024.csv")
    business["Year"] = business["Year"].astype(int)
    business = business.set_index("Year").sort_index()

    expansions = pd.read_csv(DATA_DIR / "Expansion_Costs.csv")
    expansions = expansions.set_index("Proposed Expansion").sort_index()

    return business, expansions


def solve_model(model: pyo.ConcreteModel) -> pyo.SolverResults:
    solver = pyo.SolverFactory("glpk")

    if solver is None or not solver.available():
        raise RuntimeError(
            "GLPK not available. Install glpk and ensure glpsol is on your system PATH."
        )

    results = solver.solve(model, tee=True)

    term = str(results.solver.termination_condition)
    if term.lower() not in {"optimal", "locallyoptimal"}:
        raise RuntimeError(f"Solver did not reach an optimal solution. Termination: {term}")

    return results


def export_results(model: pyo.ConcreteModel, business: pd.DataFrame) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    plan_rows = []
    cost_rows = []

    for y in sorted(list(model.Years)):
        selected = []
        expansion_spend_y = 0.0

        for e in model.Expansions:
            if pyo.value(model.Select[y, e]) > 0.5:
                cost_e = float(pyo.value(model.exp_cost[e]))
                expansion_spend_y += cost_e
                selected.append(str(e))

        labor_cost_y = float(pyo.value(model.req_labor_hours[y] * model.avg_wage[y]))
        machine_cost_y = float(pyo.value(model.req_machine_hours[y] * model.avg_wage[y]))

        operational = float(pyo.value(model.operational_cost[y]))
        raw_mat = float(pyo.value(model.raw_material_cost[y]))
        compliance = float(pyo.value(model.compliance_cost[y]))
        env = float(pyo.value(model.env_compliance_cost[y]))
        labor_law = float(pyo.value(model.labor_law_cost[y]))
        tech = float(pyo.value(model.tech_invest_cost[y]))

        total_y = (
            expansion_spend_y
            + operational
            + labor_cost_y
            + machine_cost_y
            + raw_mat
            + compliance
            + env
            + labor_law
            + tech
        )

        budget_y = float(pyo.value(model.budget[y]))
        savings_y = budget_y - total_y

        plan_rows.append(
            {
                "Year": int(y),
                "Selected_Expansions": ", ".join(selected) if selected else "None",
                "Annual_Budget": budget_y,
                "Annual_Total_Cost": total_y,
                "Annual_Budget_Savings": savings_y,
            }
        )

        cost_rows.append(
            {
                "Year": int(y),
                "Expansion_Spend": expansion_spend_y,
                "Operational_Cost": operational,
                "Labor_Cost": labor_cost_y,
                "Machinery_Cost": machine_cost_y,
                "Raw_Material_Cost": raw_mat,
                "Compliance_Cost": compliance,
                "Environmental_Compliance_Cost": env,
                "Labor_Law_Impact_Cost": labor_law,
                "Technology_Investment_Cost": tech,
                "Total_Cost": total_y,
            }
        )

    plan_df = pd.DataFrame(plan_rows).sort_values("Year")
    costs_df = pd.DataFrame(cost_rows).sort_values("Year")

    plan_df.to_csv(RESULTS_DIR / "expansion_plan.csv", index=False)
    costs_df.to_csv(RESULTS_DIR / "annual_cost_breakdown.csv", index=False)

    total_revenue = float(business["Expected Total Revenue (USD)"].sum())
    total_budget = float(business["Annual Budget (USD)"].sum())
    total_cost = float(costs_df["Total_Cost"].sum())
    total_savings = float(plan_df["Annual_Budget_Savings"].sum())

    summary_text = "\n".join(
        [
            "OptiManu capacity planning summary",
            f"Total revenue: {total_revenue:,.0f}",
            f"Total budget: {total_budget:,.0f}",
            f"Total cost: {total_cost:,.0f}",
            f"Total budget savings: {total_savings:,.0f}",
        ]
    )

    (RESULTS_DIR / "summary_metrics.txt").write_text(summary_text, encoding="utf8")

    print(summary_text)
    print("Saved results to results folder")


def main() -> None:
    business, expansions = load_inputs()
    model = build_model(business=business, expansions=expansions, initial_capacity=40000)
    solve_model(model)
    export_results(model, business)


if __name__ == "__main__":
    main()
