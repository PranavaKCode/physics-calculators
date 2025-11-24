import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Projectile Optimization Solver")

v0 = st.number_input("Initial Velocity (m/s)", value=10.0)
g = st.number_input("Gravity (m/s^2)", value=9.81)
target_x = st.number_input("Target X distance (m)", value=8.0)
target_y = st.number_input("Target Y height (m)", value=2.0)

# Solve for required angle to hit (x,y)
# Equation: y = x*tan(theta) - (g*x^2)/(2*v0^2*cos^2(theta))
# Use identity 1/cos^2 = 1 + tan^2 to make it quadratic in tan(theta)

a = - (g * target_x**2) / (2 * v0**2)
b = target_x
c = a - target_y # Because we rewrite as a*tan^2 + b*tan + (a-y) = 0

discriminant = b**2 - 4*a*c

if discriminant < 0:
    st.error("Target is out of range!")
else:
    tan_theta1 = (-b + np.sqrt(discriminant)) / (2*a)
    tan_theta2 = (-b - np.sqrt(discriminant)) / (2*a)

    theta1 = np.degrees(np.arctan(tan_theta1))
    theta2 = np.degrees(np.arctan(tan_theta2))

    st.success(f"Two possible launch angles: {theta1:.2f}° and {theta2:.2f}°")

    # Optimization: Max range on flat ground
    max_range = v0**2 / g
    st.info(f"Max theoretical range on flat ground: {max_range:.2f} m")

# Slope Logic (for "Golf on a hill" type problems)
slope_deg = st.number_input("Slope of hill (degrees)", value=0.0)
if slope_deg != 0:
    # Range on slope formula
    alpha = np.radians(slope_deg)
    # This usually requires maximizing R(theta) relative to slope
    # R = (2*v0^2 * cos(theta) * sin(theta - alpha)) / (g * cos^2(alpha))
    # Optimal theta = (pi/2 + alpha) / 2
    opt_angle = (90 + slope_deg) / 2
    st.write(f"Optimal angle for max range on this slope: {opt_angle:.2f}°")
