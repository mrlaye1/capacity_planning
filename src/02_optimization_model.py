"""
Project: Long term capacity planning for OptiManu Inc

Project: OptiManu long term capacity planning
File: 02_optimization_model.py
Purpose: Define the capacity expansion optimization model using Pyomo

Confidentiality notice:
The company name and all data used in this project are anonymized and
modified for educational and portfolio purposes only.
No real or proprietary company information is disclosed.

Author: Abdoulaye Diop
Date: 12 May 2024
"""


from __future__ import annotations

from typing import Dict, Tuple
import pandas as pd
import pyomo.environ as pyo


def build_model(
    business: pd.DataFrame,
    expansions: pd.DataFrame,
    initial_capacity: int = 40000,
) -> pyo.ConcreteModel:
    m = pyo.ConcreteModel()

    years = list(business.index.astype(int))
    exp_names = list(expansions.index)

    m.Years = pyo.Set(initialize=years, ordered=True)
    m.Expansions = pyo.Set(initialize=exp_names, ordered=False)

    m.Select = pyo.Var(m.Years, m.Expansions, within=pyo.Binary)

    m.demand = pyo.Param(m.Years, initialize=business["Forecasted Demand"].to_dict())
    m.operational_cost = pyo.Param(m.Years, initialize=business["Operational Cost (USD)"].to_dict())
    m.req_labor_hours = pyo.Param(m.Years, initialize=business["Required Labor Hours"].to_dict())
    m.req_machine_hours = pyo.Param(m.Years, initialize=business["Required Machinery Hours"].to_dict())
    m.avg_wage = pyo.Param(m.Years, initialize=business["Average Wage (USD)"].to_dict())
    m.raw_material_cost = pyo.Param(m.Years, initialize=business["Expected Raw Material Cost (USD)"].to_dict())
    m.compliance_cost = pyo.Param(m.Years, initialize=business["Expected Compliance Cost (USD)"].to_dict())
    m.env_compliance_cost = pyo.Param(m.Years, initialize=business["Expected Environmental Compliance Cost (USD)"].to_dict())
    m.labor_law_cost = pyo.Param(m.Years, initialize=business["Expected Labor Law Changes Impact Cost (USD)"].to_dict())
    m.tech_invest_cost = pyo.Param(m.Years, initialize=business["Expected Technology Investment Cost (USD)"].to_dict())
    m.budget = pyo.Param(m.Years, initialize=business["Annual Budget (USD)"].to_dict())

    m.exp_cost = pyo.Param(m.Expansions, initialize=expansions["Cost (USD)"].to_dict())
    m.time_to_build = pyo.Param(m.Expansions, initialize=expansions["Time to Build (year)"].to_dict())
    m.add_capacity = pyo.Param(m.Expansions, initialize=expansions["Additional Capacity (units)"].to_dict())

    m.initial_capacity = pyo.Param(initialize=int(initial_capacity))

    def total_cost_rule(m: pyo.ConcreteModel) -> pyo.Expression:
        expansion_spend = sum(m.exp_cost[e] * m.Select[y, e] for y in m.Years for e in m.Expansions)

        labor_cost = sum(m.req_labor_hours[y] * m.avg_wage[y] for y in m.Years)
        machine_cost = sum(m.req_machine_hours[y] * m.avg_wage[y] for y in m.Years)

        other_annual = sum(
            m.operational_cost[y]
            + m.raw_material_cost[y]
            + m.compliance_cost[y]
            + m.env_compliance_cost[y]
            + m.labor_law_cost[y]
            + m.tech_invest_cost[y]
            for y in m.Years
        )

        return expansion_spend + labor_cost + machine_cost + other_annual

    m.TotalCost = pyo.Objective(rule=total_cost_rule, sense=pyo.minimize)

    def one_time_expansion_rule(m: pyo.ConcreteModel, e: str) -> pyo.Constraint:
        return sum(m.Select[y, e] for y in m.Years) <= 1

    m.OneTimeExpansion = pyo.Constraint(m.Expansions, rule=one_time_expansion_rule)

    def capacity_available(m: pyo.ConcreteModel, y: int) -> pyo.Expression:
        added = 0
        for e in m.Expansions:
            build_time = int(pyo.value(m.time_to_build[e]))
            for y0 in m.Years:
                if int(y0) + build_time <= int(y):
                    added += m.add_capacity[e] * m.Select[y0, e]
        return m.initial_capacity + added

    def demand_satisfaction_rule(m: pyo.ConcreteModel, y: int) -> pyo.Constraint:
        return capacity_available(m, y) >= m.demand[y]

    m.DemandSatisfaction = pyo.Constraint(m.Years, rule=demand_satisfaction_rule)

    def annual_budget_rule(m: pyo.ConcreteModel, y: int) -> pyo.Constraint:
        expansion_spend_y = sum(m.exp_cost[e] * m.Select[y, e] for e in m.Expansions)

        labor_cost_y = m.req_labor_hours[y] * m.avg_wage[y]
        machine_cost_y = m.req_machine_hours[y] * m.avg_wage[y]

        total_y = (
            expansion_spend_y
            + m.operational_cost[y]
            + labor_cost_y
            + machine_cost_y
            + m.raw_material_cost[y]
            + m.compliance_cost[y]
            + m.env_compliance_cost[y]
            + m.labor_law_cost[y]
            + m.tech_invest_cost[y]
        )

        return total_y <= m.budget[y]

    m.BudgetLimit = pyo.Constraint(m.Years, rule=annual_budget_rule)

    return m
