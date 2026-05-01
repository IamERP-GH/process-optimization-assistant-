import pandas as pd
from model import evaluate_condition

def generate_temperature_sweep(
    mass_flow_rate,
    electricity_price,
    emission_factor,
    target_performance,
    T_min=40,
    T_max=160
):
    results = []

    for T in range(T_min, T_max + 1):
        result = evaluate_condition(
            T,
            mass_flow_rate,
            electricity_price,
            emission_factor
        )
        result["feasible"] = result["performance"] >= target_performance
        results.append(result)

    return pd.DataFrame(results)

def find_cost_optimal_condition(df):
    feasible_df = df[df["feasible"] == True]

    if feasible_df.empty:
        return None

    return feasible_df.loc[feasible_df["cost"].idxmin()]