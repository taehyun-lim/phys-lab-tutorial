import math
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Projectile Motion", page_icon="🏹")


def compute_projectile_trajectory(
    initial_speed_m_per_s: float,
    launch_angle_deg: float,
    initial_height_m: float,
    gravity_m_per_s2: float,
    num_points: int = 400,
) -> Tuple[np.ndarray, np.ndarray, float, float, float]:
    """
    Compute 2D projectile motion (no air resistance) from analytic solution.

    Returns x(t), y(t), t_flight, x_range, y_max.
    """
    theta = math.radians(launch_angle_deg)
    v0x = initial_speed_m_per_s * math.cos(theta)
    v0y = initial_speed_m_per_s * math.sin(theta)

    # Time of flight (for y=0 landing), allowing nonzero initial height
    disc = v0y ** 2 + 2.0 * gravity_m_per_s2 * max(initial_height_m, 0.0)
    t_flight = (v0y + math.sqrt(disc)) / gravity_m_per_s2 if gravity_m_per_s2 > 0 else 0.0
    t = np.linspace(0.0, t_flight, num=max(num_points, 2))

    x = v0x * t
    y = initial_height_m + v0y * t - 0.5 * gravity_m_per_s2 * t ** 2

    # Range and max height
    x_range = v0x * t_flight
    t_peak = v0y / gravity_m_per_s2 if gravity_m_per_s2 > 0 else 0.0
    y_max = initial_height_m + v0y * t_peak - 0.5 * gravity_m_per_s2 * t_peak ** 2
    return x, y, t_flight, x_range, y_max


st.title("Projectile Motion")

st.markdown(
    """
Adjust the parameters and observe how the trajectory, range, and flight time change.
    """
)

with st.sidebar:
    st.header("Parameters")
    v0 = st.slider("Initial speed v₀ (m/s)", min_value=1.0, max_value=60.0, value=20.0, step=0.5)
    angle = st.slider("Launch angle θ (degrees)", min_value=0.0, max_value=90.0, value=35.0, step=0.5)
    h0 = st.slider("Initial height h₀ (m)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    g = st.slider("Gravity g (m/s²)", min_value=1.0, max_value=20.0, value=9.81, step=0.01)

x, y, t_f, x_range, y_max = compute_projectile_trajectory(v0, angle, h0, g)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Trajectory"))
fig.add_hline(y=0.0, line_color="gray", line_dash="dot")
fig.update_layout(
    xaxis_title="x (m)", yaxis_title="y (m)",
    title="Projectile Trajectory",
    height=500,
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Time of flight", f"{t_f:.2f} s")
col2.metric("Horizontal range", f"{x_range:.2f} m")
col3.metric("Maximum height", f"{y_max:.2f} m")

# Mark completion
if st.button("Mark this module complete"):
    completed = st.session_state.get("completed_modules", set())
    completed.add("Projectile Motion")
    st.session_state["completed_modules"] = completed
    st.success("Marked as complete.")
