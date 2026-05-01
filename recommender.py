def generate_recommendation(current, optimal, target_performance):
    if optimal is None:
        return [
            "No feasible operating condition was found within the selected temperature range.",
            "Consider lowering the target performance or expanding the allowable operating range."
        ]

    recommendations = []

    current_T = current["temperature"]
    optimal_T = optimal["temperature"]

    if current["performance"] < target_performance:
        recommendations.append(
            "Current operating condition does not meet the target performance."
        )
        recommendations.append(
            f"Increasing temperature to approximately {optimal_T:.0f}°C can meet the target with minimum estimated cost."
        )

    elif current_T > optimal_T + 5:
        recommendations.append(
            "Current temperature is higher than necessary for the target performance."
        )
        recommendations.append(
            f"Lowering temperature to around {optimal_T:.0f}°C could reduce operating cost and carbon emissions while still meeting the target."
        )

    elif abs(current_T - optimal_T) <= 5:
        recommendations.append(
            "Current operating condition is close to the cost-optimal feasible point."
        )
        recommendations.append(
            "Only minor adjustments are recommended unless electricity price or emissions factor changes."
        )

    else:
        recommendations.append(
            "Current operating condition is feasible but not fully cost-optimized."
        )
        recommendations.append(
            f"The estimated cost-optimal temperature is approximately {optimal_T:.0f}°C."
        )

    recommendations.append(
        f"The optimal feasible condition gives an estimated cost of ${optimal['cost']:.2f} and emissions of {optimal['emissions']:.2f} kg CO₂."
    )

    return recommendations