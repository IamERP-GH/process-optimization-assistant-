import numpy as np

def calculate_performance(T, Tmin=40, k=0.035):
    if T < Tmin:
        return 0
    return 100 * (1 - np.exp(-k * (T - Tmin)))

def calculate_energy(T, mass_flow_rate, Cp=0.0012, T_ambient=25, efficiency=0.75):
    delta_T = max(T - T_ambient, 0)
    return mass_flow_rate * Cp * delta_T / efficiency

def calculate_cost(energy_kwh, electricity_price):
    return energy_kwh * electricity_price

def calculate_emissions(energy_kwh, emission_factor):
    return energy_kwh * emission_factor

def evaluate_condition(T, mass_flow_rate, electricity_price, emission_factor):
    performance = calculate_performance(T)
    energy = calculate_energy(T, mass_flow_rate)
    cost = calculate_cost(energy, electricity_price)
    emissions = calculate_emissions(energy, emission_factor)

    return {
        "temperature": T,
        "performance": performance,
        "energy": energy,
        "cost": cost,
        "emissions": emissions
    }
