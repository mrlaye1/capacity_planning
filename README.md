# Long Term Capacity Planning
## Applied Capacity Expansion Optimization for Manufacturing Strategy

Project Date: 13 April 2024

---

## Confidentiality Notice

The original company name and all identifying information in the datasets have been changed to protect confidentiality.  
All data values, cost structures, and demand patterns have been anonymized or modified while remaining representative of a real world manufacturing capacity planning and Sales and Operations Planning scenario.  
No real company data, proprietary information, or confidential business records are disclosed.

---

## Overview

This project presents a long term capacity planning optimization model designed to support strategic manufacturing investment decisions.  
The model evaluates multiple capacity expansion options over a multi year planning horizon and determines the optimal timing of investments required to meet forecasted demand while respecting annual budget constraints and construction lead times.

The project is structured as a professional analytics case study suitable for public GitHub portfolios, technical interviews, and applied roles in operations analytics, supply chain planning, and decision optimization.

---

## Business Context

Manufacturing organizations must make capital intensive capacity decisions several years in advance. These decisions involve trade offs between demand growth, investment cost, operational feasibility, and financial constraints.

OptiManu Inc faces increasing demand volatility and must determine:
- When to invest in additional production capacity
- Which expansion options provide sufficient long term coverage
- Whether projected demand can be satisfied under annual budget limitations

---

## Objectives

The optimization model is designed to:
- Satisfy forecasted demand in every planning year
- Respect annual budget constraints
- Select each expansion option at most once
- Incorporate construction lead times before capacity becomes operational
- Minimize total cost across the full planning horizon

---

## Data Description

All datasets are anonymized and used strictly for demonstration and portfolio purposes.

### Business_Planning_Data_2014_2024.csv

| Year | Forecasted Demand | Operational Cost (USD) | Required Labor Hours | Required Machinery Hours | Average Wage (USD) | Workforce Size | Labor Market Tightness | Expected Total Revenue (USD) | Expected Raw Material Cost (USD) | Expected Compliance Cost (USD) | Expected Environmental Compliance Cost (USD) | Expected Labor Law Impact Cost (USD) | Expected Technology Investment Cost (USD) | Annual Budget (USD) |
|------|-------------------|------------------------|----------------------|--------------------------|--------------------|----------------|------------------------|-------------------------------|----------------------------------|--------------------------------|-----------------------------------------------|-----------------------------------|-------------------------------------------|-------------------|
| 2014 | 50000 | 50000 | 1000 | 800 | 20 | 50 | 0.05 | 7000000 | 2500000 | 2000 | 1000 | 500 | 10000 | 6986000 |
| 2015 | 52000 | 51500 | 1100 | 850 | 22 | 55 | 0.055 | 7252000 | 2652000 | 2200 | 1100 | 550 | 10500 | 7237496 |
| 2016 | 54080 | 53000 | 1200 | 900 | 24 | 60 | 0.06 | 7516160 | 2812160 | 2400 | 1200 | 600 | 11000 | 7501128 |
| 2017 | 56243 | 54500 | 1300 | 950 | 26 | 65 | 0.065 | 7793029 | 2980879 | 2600 | 1300 | 650 | 11500 | 7777443 |
| 2018 | 58495 | 56000 | 1400 | 1000 | 28 | 70 | 0.07 | 8083480 | 3158730 | 2800 | 1400 | 700 | 12000 | 8067313 |
| 2019 | 60840 | 57500 | 1500 | 1050 | 30 | 75 | 0.075 | 9388200 | 3346200 | 3000 | 1500 | 750 | 12500 | 9369424 |
| 2020 | 63282 | 59000 | 1600 | 1100 | 32 | 80 | 0.08 | 10707892 | 3543792 | 3200 | 1600 | 800 | 13000 | 10686476 |
| 2021 | 65825 | 60500 | 1700 | 1150 | 34 | 85 | 0.085 | 9043275 | 3752025 | 3400 | 1700 | 850 | 13500 | 9025188 |
| 2022 | 68476 | 62000 | 1800 | 1200 | 36 | 90 | 0.09 | 9395408 | 3971608 | 3600 | 1800 | 900 | 14000 | 9376617 |
| 2023 | 71240 | 63500 | 1900 | 1250 | 38 | 95 | 0.095 | 9765160 | 4203160 | 3800 | 1900 | 950 | 14500 | 9745630 |

---

### Expansion_Costs.csv

| Proposed Expansion | Cost (USD) | Time to Build (years) | Additional Capacity (units) | Efficiency Gain |
|-------------------|------------|------------------------|-----------------------------|-----------------|
| New Production Line | 3000000 | 0.5 | 20000 | 0.10 |
| Factory A (Small) | 5000000 | 1 | 30000 | 0.15 |
| Factory B (Medium) | 8000000 | 2 | 50000 | 0.25 |
| Factory C (Large) | 12000000 | 3 | 80000 | 0.40 |

---

## Methodology

Input data are validated for completeness, correct year indexing, and internal consistency prior to model execution.  
A mixed integer optimization model is formulated using Pyomo with binary expansion selection variables, demand satisfaction constraints, annual budget constraints, and capacity availability adjusted for construction lead times.  
The optimization model is defined in src/02_optimization_model.py and imported by the solver script.

---

## Project Structure

optimanu_capacity_planning  
├── README.md  
├── data  
│   ├── Business_Planning_Data_2014_2024.csv  
│   └── Expansion_Costs.csv  
├── src  
│   ├── 01_data_preparation.py  
│   ├── 02_optimization_model.py  
│   └── 03_solve_and_report.py  
├── results  
│   ├── expansion_plan.csv  
│   ├── annual_cost_breakdown.csv  
│   └── summary_metrics.txt  
└── figures  

---

## Reproducibility

`Environment requirements:
- Python 3.10 or later
- pandas
- pyomo
- GLPK solver (glpsol must be available in system PATH)

Execution logic:
- 01_data_preparation.py validates and prepares input data
- 02_optimization_model.py defines the optimization model
- 03_solve_and_report.py imports the model, solves it, and exports results

Execution order:
python src/01_data_preparation.py
python src/03_solve_and_report.py`

---

## Analytical Value

The outputs support strategic analysis of optimal capacity investment timing, trade offs between capital expenditure and demand coverage, and long term budget feasibility.

---

## Limitations

Demand and cost projections are treated as deterministic.  
Capacity is modeled at an annual aggregate level.  
Efficiency gains are not dynamically propagated across years.

---

## Author

ABDOULAYE DIOP

Applied Data Science and Analytics
