import streamlit as st
import math

st.title("Relativity & Collider Solver")

mode = st.radio("Mode", ["Collider Energy", "Relativistic Doppler"])

c = 299792458

if mode == "Collider Energy":
    st.write("Calculate available energy (center of mass) for particle creation.")
    m0 = st.number_input("Rest Mass of Particle (GeV/c^2)", value=0.000511) # Electron
    E_beam = st.number_input("Beam Energy (GeV)", value=209.0)
    setup = st.selectbox("Setup", ["Fixed Target (Beam -> Stationary)", "Collider (Beam -> Beam)"])

    if setup == "Collider (Beam -> Beam)":
        E_cm = 2 * E_beam
        st.success(f"Center of Mass Energy: {E_cm} GeV")
    else:
        # E_cm = sqrt(2 * m * E_beam + m^2 + m^2) roughly
        # Precise formula: s = m1^2 + m2^2 + 2E1*m2
        s = m0**2 + m0**2 + 2 * E_beam * m0
        E_cm = math.sqrt(s)
        st.success(f"Center of Mass Energy: {E_cm:.4f} GeV")
        st.info("Note how much energy is 'wasted' on momentum in fixed target setups!")

elif mode == "Relativistic Doppler":
    lambda_0 = st.number_input("Emitted Wavelength (nm)", value=600.0)
    lambda_obs = st.number_input("Observed Wavelength (nm)", value=670.0)

    # Formula: lambda_obs = lambda_0 * sqrt((1+beta)/(1-beta))
    z = lambda_obs / lambda_0
    # z^2 = (1+b)/(1-b) -> z^2 - z^2b = 1 + b -> b(1+z^2) = z^2 - 1
    beta = (z**2 - 1) / (z**2 + 1)
    v = beta * c

    st.success(f"Recession Velocity (v): {v:.4e} m/s")
    st.write(f"Beta (v/c): {beta:.4f}")
