import math
import streamlit as st

st.set_page_config(page_title="Buoyancy & Fluids Toolkit", page_icon="🌊")

st.title(" Buoyancy & Fluids Toolkit")
st.caption("Quick checks for float/sink, submerged fraction, added mass, and composite objects.")


st.sidebar.header("Fluid & Gravity")

fluid_preset = st.sidebar.selectbox(
    "Fluid preset",
    ["Custom", "Fresh water (~1000 kg/m³)", "Sea water (~1025 kg/m³)", "Oil (~850 kg/m³)", "Ethanol (~790 kg/m³)"],
)

if fluid_preset == "Fresh water (~1000 kg/m³)":
    rho_fluid_default = 1000.0
elif fluid_preset == "Sea water (~1025 kg/m³)":
    rho_fluid_default = 1025.0
elif fluid_preset == "Oil (~850 kg/m³)":
    rho_fluid_default = 850.0
elif fluid_preset == "Ethanol (~790 kg/m³)":
    rho_fluid_default = 790.0
else:
    rho_fluid_default = 1000.0

rho_fluid = st.sidebar.number_input("Fluid density ρ (kg/m³)", value=rho_fluid_default, min_value=0.0)
g = st.sidebar.number_input("Gravitational acceleration g (m/s²)", value=9.81, min_value=0.0)

mode = st.sidebar.radio(
    "Calculator mode",
    ["Single object", "Object + added mass", "Composite object (2 materials)"],
)


def classify_buoyancy(rho_obj: float, rho_fluid: float) -> str:
    if rho_obj <= 0 or rho_fluid <= 0:
        return "invalid"
    if rho_obj < rho_fluid:
        return "floats (partially submerged)"
    elif math.isclose(rho_obj, rho_fluid, rel_tol=1e-6):
        return "neutrally buoyant (can stay at any depth)"
    else:
        return "sinks (fully submerged at equilibrium)"


def fraction_submerged(rho_obj: float, rho_fluid: float) -> float:
    """
    For an object that is floating at the surface in equilibrium:
    ρ_obj / ρ_fluid = V_sub / V_total
    """
    if rho_fluid <= 0:
        return float("nan")
    return rho_obj / rho_fluid


# --------------------------------------
# Mode 1: Single object
# --------------------------------------
if mode == "Single object":
    st.header("Single Object – Float or Sink?")

    st.markdown("Give the **mass** and **volume** of the object:")

    col1, col2 = st.columns(2)
    with col1:
        m_obj = st.number_input("Object mass m (kg)", value=10.0, min_value=0.0)
    with col2:
        V_obj = st.number_input("Object volume V (m³)", value=0.02, min_value=0.0)

    if V_obj <= 0 or m_obj <= 0:
        st.warning("Enter positive values for both mass and volume.")
    else:
        rho_obj = m_obj / V_obj
        W = m_obj * g  # weight
        Fb_full = rho_fluid * g * V_obj  # buoyant force if fully submerged

        st.subheader("Results")
        st.write(f"Object density ρₒ = **{rho_obj:.2f} kg/m³**")
        st.write(f"Weight W = **{W:.2f} N**")
        st.write(f"Buoyant force if fully submerged Fᵦ,full = **{Fb_full:.2f} N**")

        classification = classify_buoyancy(rho_obj, rho_fluid)
        if classification == "invalid":
            st.error("Check densities: one of them is non-positive.")
        else:
            st.info(f"Buoyancy verdict: **{classification}**")

            if classification.startswith("floats"):
                frac = fraction_submerged(rho_obj, rho_fluid)
                frac_percent = frac * 100
                st.write(
                    f"Fraction of volume submerged at equilibrium: "
                    f"**{frac:.3f}** (≈ **{frac_percent:.1f}%** of the object)"
                )

                V_sub = frac * V_obj
                Fb_eq = rho_fluid * g * V_sub
                st.write(f"Submerged volume V_sub ≈ **{V_sub:.4f} m³**, buoyant force at equilibrium ≈ **{Fb_eq:.2f} N**")

            elif classification.startswith("sinks"):
                st.write(
                    "Because the object is denser than the fluid, it cannot float at the surface. "
                    "At equilibrium it will be fully submerged (or rest on the bottom if there is one)."
                )
            else:
                st.write(
                    "The object is neutrally buoyant: its density matches the fluid's density, "
                    "so any submerged fraction is possible without net vertical force."
                )


# --------------------------------------
# Mode 2: Object + added mass
# --------------------------------------
elif mode == "Object + added mass":
    st.header("Object + Added Mass – When Does It Sink?")

    st.markdown(
        "You have a floating object (like a foam block or boat), and you add extra mass "
        "(stones, people, cargo). This helps for “how many people until it sinks?”-type problems."
    )

    col1, col2 = st.columns(2)
    with col1:
        m_obj = st.number_input("Base object mass m₀ (kg)", value=10.0, min_value=0.0)
    with col2:
        V_obj = st.number_input("Base object volume V (m³)", value=0.02, min_value=0.0)

    if V_obj <= 0 or m_obj <= 0:
        st.warning("Enter positive values for both base mass and volume.")
    else:
        rho_obj = m_obj / V_obj
        st.write(f"Base object density ρ₀ = **{rho_obj:.2f} kg/m³**")

        # mass needed for neutral buoyancy at the surface (just fully submerged)
