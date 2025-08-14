import math
import streamlit as st


st.set_page_config(page_title="04 – Slip Correction", page_icon="💨", layout="wide")

st.title("04 – Slip Correction (Cunningham) with Iteration")
st.caption("Enter physical parameters and a measured terminal speed. This tool checks your results and shows the iterative slip-correction steps.")


def compute_radius_from_eta(eta: float, velocity: float, density_difference: float, gravity: float) -> float | None:
    """Radius from Stokes terminal velocity with constants arranged to match the workbook.

    r = sqrt( 6 * eta * v / ( (rho_oil - rho_air) * (4*g/3) ) )
    Equivalent to the classic r = sqrt( (9/2) * eta * v / (g * density_difference) ).
    Returns None if inputs lead to invalid domain.
    """
    denom = density_difference * (4.0 * gravity / 3.0)
    if denom <= 0 or eta <= 0 or velocity <= 0:
        return None
    val = 6.0 * eta * velocity / denom
    if val <= 0:
        return None
    return math.sqrt(val)


def compute_cunningham_correction(knudsen_number: float, a0: float, a1: float, a2: float) -> tuple[float, float]:
    """Return (A, C) where A = a0 + a1*exp(-a2/Kn), and C = 1 + A*Kn.

    This matches the workbook structure and corresponds to a common form of the
    Cunningham slip correction C ≈ 1 + Kn*(1.257 + 0.4*exp(-1.1/Kn)) when using
    defaults a0=1.257, a1=0.4, a2=1.1.
    """
    if knudsen_number <= 0:
        return (float("nan"), float("nan"))
    A_val = a0 + a1 * math.exp(-a2 / knudsen_number)
    C_val = 1.0 + A_val * knudsen_number
    return (A_val, C_val)


def iterate_slip_correction(
    rho_oil: float,
    rho_air: float,
    gravity: float,
    velocity: float,
    eta_base: float,
    mean_free_path_m: float,
    a0: float,
    a1: float,
    a2: float,
    iterations: int = 5,
):
    """Run the iteration sequence used in the workbook.

    At each stage i with viscosity eta_i, compute:
      r_i = radius(eta_i), Kn_i = λ / r_i, (A_i, C_i) from Kn_i, and eta_{i+1} = eta_base / C_i.

    Note: eta_base is the uncorrected viscosity used in each division by C_i, as in the sheet formula.
    """
    rho_diff = rho_oil - rho_air
    if rho_diff <= 0:
        return {
            "ok": False,
            "error": "density difference (oil − air) must be positive.",
            "stages": [],
        }

    stages = []
    eta_i = eta_base
    for i in range(iterations):
        r_i = compute_radius_from_eta(eta_i, velocity, rho_diff, gravity)
        if not r_i or r_i <= 0:
            return {"ok": False, "error": "invalid radius computed (check inputs).", "stages": stages}
        kn_i = mean_free_path_m / r_i if r_i > 0 else float("nan")
        A_i, C_i = compute_cunningham_correction(kn_i, a0, a1, a2)
        if not (C_i > 0):
            return {"ok": False, "error": "invalid Cunningham factor C (≤0).", "stages": stages}
        eta_next = eta_base / C_i
        stages.append({
            "index": i,
            "eta_in": eta_i,
            "radius": r_i,
            "kn": kn_i,
            "A": A_i,
            "C": C_i,
            "eta_out": eta_next,
        })
        eta_i = eta_next

    return {"ok": True, "error": None, "stages": stages}


def is_close(student_value: float, expected_value: float, abs_tol: float = 0.002, rel_tol: float = 0.001) -> bool:
    """Return True if student_value is within tolerance of expected_value.

    Tolerance policy: a value is marked correct if within max(abs_tol, rel_tol * |expected|).
    Defaults: abs_tol = 0.002, rel_tol = 0.001 (i.e., ±0.002 or ±0.1%, whichever is larger).
    Adjust abs_tol/rel_tol for stricter or looser checks.
    """
    try:
        return math.isclose(float(student_value), float(expected_value), rel_tol=rel_tol, abs_tol=abs_tol)
    except Exception:
        return False


def fmt(x: float, digits: int = 6) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    return f"{x:.{digits}g}"


# =============================
# Enter Inputs and Check Your Results
# =============================
st.subheader("Enter Inputs and Check Your Results")

with st.container():
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Physical Inputs**")
        rho_oil = st.number_input("Density of oil [kg/m³]", value=838.0, step=1.0, format="%.6f")
        rho_air = st.number_input("Density of air [kg/m³]", value=1.204575411, step=0.001, format="%.9f")
        gravity = st.number_input("g [m/s²]", value=9.8, step=0.01, format="%.6f")
        velocity = st.number_input("Terminal speed v [m/s]", value=3.460207612456748e-05, step=1e-06, format="%.9e")
        eta_base = st.number_input("Base viscosity η (uncorrected) [kg/(m·s)]", value=1.82e-05, step=1e-06, format="%.9e")
        lambda_nm = st.number_input("Mean free path λ [nm]", value=68.4543, step=0.1, format="%.6f")
        a0 = st.number_input("Cunningham a₀", value=1.257, step=0.001, format="%.6f")
        a1 = st.number_input("Cunningham a₁", value=0.4, step=0.001, format="%.6f")
        a2 = st.number_input("Cunningham a₂", value=1.1, step=0.001, format="%.6f")
        iterations = st.number_input("Iterations", min_value=1, max_value=20, value=5, step=1)

    with col_b:
        st.markdown("**Your Results (first two stages and final)**")
        # Stage 0 outputs (computed from eta_base)
        student_r0 = st.number_input("Stage 0: r₀ [m]", value=0.0, step=0.0, format="%.9e")
        student_kn0 = st.number_input("Stage 0: Kn₀", value=0.0, step=0.0, format="%.9e")
        student_c0 = st.number_input("Stage 0: C₀", value=0.0, step=0.0, format="%.9f")
        student_eta1 = st.number_input("Stage 1: η₁ [kg/(m·s)]", value=0.0, step=0.0, format="%.9e")
        # Stage 1 outputs (computed from eta1)
        student_r1 = st.number_input("Stage 1: r₁ [m]", value=0.0, step=0.0, format="%.9e")
        student_kn1 = st.number_input("Stage 1: Kn₁", value=0.0, step=0.0, format="%.9e")
        student_c1 = st.number_input("Stage 1: C₁", value=0.0, step=0.0, format="%.9f")
        student_eta2 = st.number_input("Stage 2: η₂ [kg/(m·s)]", value=0.0, step=0.0, format="%.9e")
        # Final values after N iterations
        student_rN = st.number_input("Final: r_N [m]", value=0.0, step=0.0, format="%.9e")
        student_etaN = st.number_input("Final: η_N [kg/(m·s)]", value=0.0, step=0.0, format="%.9e")

    # Track input changes to reset the check gate
    signature = (
        rho_oil, rho_air, gravity, velocity, eta_base, lambda_nm, a0, a1, a2, iterations,
        student_r0, student_kn0, student_c0, student_eta1, student_r1, student_kn1, student_c1, student_eta2, student_rN, student_etaN,
    )
    if "prev_sig_slip" not in st.session_state:
        st.session_state.prev_sig_slip = signature
    if "show_results_slip" not in st.session_state:
        st.session_state.show_results_slip = False
    if signature != st.session_state.prev_sig_slip:
        st.session_state.prev_sig_slip = signature
        st.session_state.show_results_slip = False

    if st.button("Check Results"):
        st.session_state.show_results_slip = True

    # Compute expected sequence
    lambda_m = lambda_nm * 1e-9
    result = iterate_slip_correction(
        rho_oil=rho_oil,
        rho_air=rho_air,
        gravity=gravity,
        velocity=velocity,
        eta_base=eta_base,
        mean_free_path_m=lambda_m,
        a0=a0,
        a1=a1,
        a2=a2,
        iterations=int(iterations),
    )

    if st.session_state.show_results_slip:
        if not result["ok"]:
            st.error(result["error"]) 
        else:
            stages = result["stages"]
            # Extract key expected values
            s0 = stages[0]
            s1 = stages[1] if len(stages) > 1 else stages[0]
            sN = stages[-1]

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if is_close(student_r0, s0["radius"]):
                    st.success(f"r₀ ✓\n\nExpected: {fmt(s0['radius'], 6)} m")
                else:
                    st.error("r₀ ✗ — try again")
            with c2:
                if is_close(student_kn0, s0["kn"]):
                    st.success(f"Kn₀ ✓\n\nExpected: {fmt(s0['kn'], 6)}")
                else:
                    st.error("Kn₀ ✗ — try again")
            with c3:
                if is_close(student_c0, s0["C"]):
                    st.success(f"C₀ ✓\n\nExpected: {fmt(s0['C'], 6)}")
                else:
                    st.error("C₀ ✗ — try again")
            with c4:
                if is_close(student_eta1, s0["eta_out"]):
                    st.success(f"η₁ ✓\n\nExpected: {fmt(s0['eta_out'], 6)} kg/(m·s)")
                else:
                    st.error("η₁ ✗ — try again")
            with c5:
                if is_close(student_r1, s1["radius"]):
                    st.success(f"r₁ ✓\n\nExpected: {fmt(s1['radius'], 6)} m")
                else:
                    st.error("r₁ ✗ — try again")

            c6, c7, c8, c9, c10 = st.columns(5)
            with c6:
                if is_close(student_kn1, s1["kn"]):
                    st.success(f"Kn₁ ✓\n\nExpected: {fmt(s1['kn'], 6)}")
                else:
                    st.error("Kn₁ ✗ — try again")
            with c7:
                if is_close(student_c1, s1["C"]):
                    st.success(f"C₁ ✓\n\nExpected: {fmt(s1['C'], 6)}")
                else:
                    st.error("C₁ ✗ — try again")
            with c8:
                if is_close(student_eta2, s1["eta_out"]):
                    st.success(f"η₂ ✓\n\nExpected: {fmt(s1['eta_out'], 6)} kg/(m·s)")
                else:
                    st.error("η₂ ✗ — try again")
            with c9:
                if is_close(student_rN, sN["radius"]):
                    st.success(f"r_N ✓\n\nExpected: {fmt(sN['radius'], 6)} m")
                else:
                    st.error("r_N ✗ — try again")
            with c10:
                if is_close(student_etaN, sN["eta_out"]):
                    st.success(f"η_N ✓\n\nExpected: {fmt(sN['eta_out'], 6)} kg/(m·s)")
                else:
                    st.error("η_N ✗ — try again")


# =============================
# Step-by-Step Calculation
# =============================
st.subheader("Step-by-Step Calculation")

if "show_steps_slip" not in st.session_state:
    st.session_state.show_steps_slip = False

if st.button("Step-by-Step Calculation" + (" (hide)" if st.session_state.show_steps_slip else " (show)")):
    st.session_state.show_steps_slip = not st.session_state.show_steps_slip

if st.session_state.show_steps_slip:
    lambda_m = (st.session_state.get("lambda_nm", 68.4543) if False else lambda_nm) * 1e-9
    result_preview = iterate_slip_correction(
        rho_oil=rho_oil,
        rho_air=rho_air,
        gravity=gravity,
        velocity=velocity,
        eta_base=eta_base,
        mean_free_path_m=lambda_m,
        a0=a0,
        a1=a1,
        a2=a2,
        iterations=int(iterations),
    )
    if not result_preview["ok"]:
        st.error(result_preview["error"]) 
    else:
        stages = result_preview["stages"]
        # Show first two stages in detail, then final summary
        if stages:
            s0 = stages[0]
            st.markdown("**Stage 0** (using η₀ = base η)")
            st.markdown(f"r₀ = sqrt( 6 η₀ v / ((ρ_oil−ρ_air)·(4g/3)) ) = sqrt( 6·{eta_base:.6g}·{velocity:.6g} / (({rho_oil:.6g}−{rho_air:.6g})·({4*gravity/3:.6g})) ) = {s0['radius']:.6g} m")
            st.markdown(f"Kn₀ = λ / r₀ = {lambda_m:.6g} / {s0['radius']:.6g} = {s0['kn']:.6g}")
            st.markdown(f"A₀ = a₀ + a₁ e^(−a₂/Kn₀) = {a0:.6g} + {a1:.6g}·exp(−{a2:.6g}/{s0['kn']:.6g}) = {s0['A']:.6g}")
            st.markdown(f"C₀ = 1 + A₀·Kn₀ = 1 + {s0['A']:.6g}·{s0['kn']:.6g} = {s0['C']:.6g}")
            st.markdown(f"η₁ = η_base / C₀ = {eta_base:.6g} / {s0['C']:.6g} = {s0['eta_out']:.6g} kg/(m·s)")
            st.divider()

        if len(stages) > 1:
            s1 = stages[1]
            st.markdown("**Stage 1** (using η₁)")
            st.markdown(f"r₁ = sqrt( 6 η₁ v / ((ρ_oil−ρ_air)·(4g/3)) ) = sqrt( 6·{s0['eta_out']:.6g}·{velocity:.6g} / (({rho_oil:.6g}−{rho_air:.6g})·({4*gravity/3:.6g})) ) = {s1['radius']:.6g} m")
            st.markdown(f"Kn₁ = λ / r₁ = {lambda_m:.6g} / {s1['radius']:.6g} = {s1['kn']:.6g}")
            st.markdown(f"A₁ = a₀ + a₁ e^(−a₂/Kn₁) = {a0:.6g} + {a1:.6g}·exp(−{a2:.6g}/{s1['kn']:.6g}) = {s1['A']:.6g}")
            st.markdown(f"C₁ = 1 + A₁·Kn₁ = 1 + {s1['A']:.6g}·{s1['kn']:.6g} = {s1['C']:.6g}")
            st.markdown(f"η₂ = η_base / C₁ = {eta_base:.6g} / {s1['C']:.6g} = {s1['eta_out']:.6g} kg/(m·s)")
            st.divider()

        sN = stages[-1]
        st.markdown("**Final (after N iterations)**")
        st.markdown(f"r_N = {sN['radius']:.6g} m,  η_N = {sN['eta_out']:.6g} kg/(m·s),  Kn_N = {sN['kn']:.6g},  C_N = {sN['C']:.6g}")


