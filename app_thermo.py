import streamlit as st
import numpy as np

st.title("Thermodynamic Process Calculator")

P1 = st.number_input("Initial Pressure (Pa)", value=101325.0)
V1 = st.number_input("Initial Volume (m^3)", value=1.0)
T1 = st.number_input("Initial Temp (K)", value=298.0)
gamma = st.number_input("Adiabatic Index (gamma)", value=1.4) # 1.4 for diatomic air

process = st.selectbox("Process Type", ["Isothermal (T=const)", "Adiabatic (Q=0)", "Isobaric (P=const)", "Isochoric (V=const)"])
target_var = st.selectbox("Target Constraint", ["Final Volume", "Final Pressure", "Final Temp"])
target_val = st.number_input("Target Value", value=0.5)

P2, V2, T2 = P1, V1, T1
Work = 0.0

if process == "Isothermal (T=const)":
    T2 = T1
    if target_var == "Final Volume":
        V2 = target_val
        P2 = P1 * V1 / V2
    elif target_var == "Final Pressure":
        P2 = target_val
        V2 = P1 * V1 / P2
    Work = P1 * V1 * np.log(V2 / V1)

elif process == "Adiabatic (Q=0)":
    # P1*V1^g = P2*V2^g
    if target_var == "Final Volume":
        V2 = target_val
        P2 = P1 * (V1 / V2)**gamma
        T2 = T1 * (V1 / V2)**(gamma - 1)
    elif target_var == "Final Pressure":
        P2 = target_val
        V2 = V1 * (P1 / P2)**(1/gamma)
        T2 = T1 * (P2 / P1)**((gamma-1)/gamma)

    Work = (P1 * V1 - P2 * V2) / (gamma - 1)

st.subheader("Results")
st.write(f"**Final State:** P={P2:.2f} Pa, V={V2:.4f} m^3, T={T2:.2f} K")
st.write(f"**Work Done (by gas):** {Work:.2f} J")
