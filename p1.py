import math
import streamlit as st

st.set_page_config(page_title="Mowing Spiral Pole Radius Calculator", page_icon="🌱")

st.title("Mowing Spiral Pole Radius Calculator 🌱")
st.write(
    """
    This app computes the required radius of the central pole so that a lawnmower
    attached by a rope winds around it in a spiral and the cut strips **just touch**
    (no overlaps, no gaps).

    Mathematically, the mower follows (approximately) an involute of a circle.
    The distance between neighboring turns of this spiral equals the pole's
    circumference, \(2\\pi R\). To cover the lawn perfectly, that distance must
    equal the mower’s cutting width \(w\).
    """
)

st.latex(r"w = 2\pi R \quad \Rightarrow \quad R = \frac{w}{2\pi}")

st.subheader("Input")

cut_width_m = st.number_input(
    "Mower cutting width w (in meters)",
    min_value=0.01,
    value=0.75,
    step=0.01,
    format="%.2f",
    help="For this problem, w = 0.75 m."
)

# Compute radius
radius_m = cut_width_m / (2 * math.pi)
radius_cm = radius_m * 100.0

# Format with 2 significant digits (for the cm answer)
radius_cm_2sf = float(f"{radius_cm:.2g}")

st.subheader("Result")

st.write("Using the formula:")
st.latex(r"R = \dfrac{w}{2\pi}")

st.write(
    f"""
    - Pole radius in **meters**: `{radius_m:.5f} m`  
    - Pole radius in **centimeters**: `{radius_cm:.5f} cm`  
    - Pole radius in **centimeters (2 significant digits)**: **{radius_cm_2sf:.2f} cm**
    """
)

st.info(
    f"For the given mower width of {cut_width_m:.2f} m, "
    f"the pole radius should be approximately **{radius_cm_2sf:.2f} cm** "
    f"to make the cut strips perfectly align."
)

st.caption("Neglecting rope thickness, as stated in the problem.")
