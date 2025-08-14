import math
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Oscillations", page_icon="🪗")


def compute_damped_oscillation(
    mass_kg: float,
    spring_constant_n_per_m: float,
    damping_coefficient_kg_per_s: float,
    amplitude_m: float,
    phase_rad: float,
    duration_s: float,
    num_points: int = 1200,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute x(t) for a damped mass–spring system with analytic solution.

    x(t) = A e^{-γ t} cos(ω_d t + φ),
      γ = c / (2m),  ω_0 = sqrt(k/m),  ω_d = sqrt(ω_0^2 - γ^2) for underdamped.

    If overdamped/critical, falls back to a numerically stable envelope using real ω_d = 0.
    """
    gamma = damping_coefficient_kg_per_s / (2.0 * max(mass_kg, 1e-9))
    omega0 = math.sqrt(max(spring_constant_n_per_m, 0.0) / max(mass_kg, 1e-9))
    under = omega0 ** 2 - gamma ** 2
    omega_d = math.sqrt(under) if under > 0 else 0.0

    t = np.linspace(0.0, max(duration_s, 0.01), num=max(num_points, 2))
    envelope = np.exp(-gamma * t)

    if omega_d > 0:
        x = amplitude_m * envelope * np.cos(omega_d * t + phase_rad)
    else:
        # Critically damped or overdamped: show non-oscillatory decay using cosine term frozen at phase
        x = amplitude_m * envelope * np.cos(phase_rad)
    return t, x


st.title("Oscillations (Mass–Spring–Damper)")

st.markdown(
    """
Explore how mass m, spring constant k, and damping c affect a mass–spring system.
    """
)

with st.sidebar:
    st.header("Parameters")
    m = st.slider("Mass m (kg)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    k = st.slider("Spring constant k (N/m)", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
    c = st.slider("Damping c (kg/s)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
    A = st.slider("Amplitude A (m)", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
    phi = st.slider("Phase φ (deg)", min_value=0.0, max_value=360.0, value=0.0, step=1.0)
    T = st.slider("Duration (s)", min_value=1.0, max_value=30.0, value=10.0, step=0.5)

phi_rad = math.radians(phi)

t, x = compute_damped_oscillation(m, k, c, A, phi_rad, T)

omega0 = math.sqrt(k / m)
gamma = c / (2.0 * m)
under = omega0 ** 2 - gamma ** 2
omega_d = math.sqrt(under) if under > 0 else 0.0

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=x, mode="lines", name="x(t)"))
fig.update_layout(
    xaxis_title="t (s)", yaxis_title="x (m)",
    title="Damped Oscillation",
    height=500,
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("ω₀ (rad/s)", f"{omega0:.2f}")
col2.metric("γ (1/s)", f"{gamma:.2f}")
col3.metric("ω_d (rad/s)", f"{omega_d:.2f}")

# Quick prompts
st.divider()
with st.expander("Checks for understanding"):
    st.markdown(
        "- How does increasing damping c affect ω_d and the envelope?\n"
        "- What happens as c approaches the critical value 2√(km)?\n"
        "- How do m and k change ω₀ and the period?"
    )

# Mark completion
if st.button("Mark this module complete"):
    completed = st.session_state.get("completed_modules", set())
    completed.add("Oscillations")
    st.session_state["completed_modules"] = completed
    st.success("Marked as complete.")
