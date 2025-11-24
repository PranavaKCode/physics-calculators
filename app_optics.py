import streamlit as st
import numpy as np

st.title("Matrix Optics Solver")

st.write("Add optical elements in order from Object to Image.")

# Initial ray vector [y, theta]
y0 = st.number_input("Initial Height", value=1.0)
theta0 = st.number_input("Initial Angle (rad)", value=0.0)

# Chain matrices
# Identity matrix
M_total = np.identity(2)

num_elements = st.number_input("Number of Elements", min_value=1, max_value=10, step=1)

for i in range(int(num_elements)):
    etype = st.selectbox(f"Element {i+1} Type", ["Free Space propagation", "Thin Lens", "Refraction (Flat Interface)"], key=f"type_{i}")

    M_curr = np.identity(2)

    if etype == "Free Space propagation":
        d = st.number_input(f"Distance d_{i+1} (m)", value=0.1, key=f"d_{i}")
        M_curr = np.array([[1, d], [0, 1]])

    elif etype == "Thin Lens":
        f = st.number_input(f"Focal Length f_{i+1} (m)", value=0.05, key=f"f_{i}")
        M_curr = np.array([[1, 0], [-1/f, 1]])

    elif etype == "Refraction (Flat Interface)":
        n1 = st.number_input(f"n_in_{i+1}", value=1.0, key=f"n1_{i}")
        n2 = st.number_input(f"n_out_{i+1}", value=1.5, key=f"n2_{i}")
        M_curr = np.array([[1, 0], [0, n1/n2]])

    # Multiply matrices (New is multiplied on the LEFT)
    M_total = np.matmul(M_curr, M_total)

# Calculate output
# [y_out]   [A B] [y_in]
# [th_out]  [C D] [th_in]
in_vec = np.array([y0, theta0])
out_vec = np.matmul(M_total, in_vec)

st.subheader("Result")
st.write(f"Final Height: {out_vec[0]:.4f}")
st.write(f"Final Angle: {out_vec[1]:.4f} rad")
st.write(f"System Matrix ABCD: \n {M_total}")

if M_total[1,0] != 0:
    st.write(f"Effective Focal Length: {-1/M_total[1,0]:.4f} m")
