import streamlit as st
import matplotlib.pyplot as plt

from model import evaluate_condition
from optimizer import generate_temperature_sweep, find_cost_optimal_condition
from recommender import generate_recommendation

st.set_page_config(page_title="Process Optimization Assistant", layout="wide")

st.title("Industrial Process Optimization Assistant Program")
st.title("GitHub@IamERP")

st.write(
    "This tool evaluates process performance, energy use, operating cost, "
    "and carbon emissions under different operating temperatures."
)

st.sidebar.header("Input Parameters")

temperature = st.sidebar.slider("Operating Temperature (°C)", 40, 160, 100)
mass_flow_rate = st.sidebar.number_input("Mass Flow Rate (kg/h)", value=1000.0)
electricity_price = st.sidebar.number_input("Electricity Price ($/kWh)", value=0.12)
emission_factor = st.sidebar.number_input("Emission Factor (kg CO₂/kWh)", value=0.40)
target_performance = st.sidebar.slider("Target Performance (%)", 50, 99, 90)

current = evaluate_condition(
    temperature,
    mass_flow_rate,
    electricity_price,
    emission_factor
)

df = generate_temperature_sweep(
    mass_flow_rate,
    electricity_price,
    emission_factor,
    target_performance
)

optimal = find_cost_optimal_condition(df)

st.header("Current Operating Condition")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Performance", f"{current['performance']:.1f}%")
col2.metric("Energy Use", f"{current['energy']:.1f} kWh")
col3.metric("Operating Cost", f"${current['cost']:.2f}")
col4.metric("Emissions", f"{current['emissions']:.1f} kg CO₂")

st.header("Optimization Results")

if optimal is not None:
    st.success(
        f"Cost-optimal feasible temperature: {optimal['temperature']:.0f}°C"
    )
else:
    st.error("No feasible condition found in the selected range.")

st.header("Process Analysis Charts")

colA, colB = st.columns(2)

with colA:
    fig, ax = plt.subplots()
    ax.plot(df["temperature"], df["performance"])
    ax.axhline(target_performance, linestyle="--")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Performance (%)")
    ax.set_title("Performance vs Temperature")
    st.pyplot(fig)

with colB:
    fig, ax = plt.subplots()
    ax.plot(df["temperature"], df["cost"])
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Cost ($)")
    ax.set_title("Cost vs Temperature")
    st.pyplot(fig)

colC, colD = st.columns(2)

with colC:
    fig, ax = plt.subplots()
    ax.plot(df["temperature"], df["emissions"])
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Emissions (kg CO₂)")
    ax.set_title("Emissions vs Temperature")
    st.pyplot(fig)

with colD:
    fig, ax = plt.subplots()
    ax.scatter(df["emissions"], df["cost"])
    ax.set_xlabel("Emissions (kg CO₂)")
    ax.set_ylabel("Cost ($)")
    ax.set_title("Cost vs Emissions")
    st.pyplot(fig)

st.header("Recommendations: ")

recommendations = generate_recommendation(
    current,
    optimal,
    target_performance
)

for rec in recommendations:
    st.write(f"- {rec}")