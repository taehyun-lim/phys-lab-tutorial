import math
import streamlit as st


st.set_page_config(page_title="02 – Snell's Law", page_icon="🔦", layout="wide")

st.title("Snell's Law with Uncertainty (Range Method)")
st.caption("Enter angles in degrees. This tool checks your results and shows how the calculations are done.")


def compute_refractive_indices(theta1_deg: float, theta2_deg: float, dtheta1_deg: float, dtheta2_deg: float):

	# Convert degrees to radians
	theta1_rad = math.radians(theta1_deg)
	theta2_rad = math.radians(theta2_deg)
	dtheta1_rad = math.radians(dtheta1_deg)
	dtheta2_rad = math.radians(dtheta2_deg)

	# Guard against invalid input leading to division by zero
	sin_theta1 = math.sin(theta1_rad)
	if abs(sin_theta1) < 1e-12:
		return {
			"ok": False,
			"error": "sin(θ1) is zero or too small; θ1 must not be 0°, 180°, etc.",
			"nominal": None,
			"high": None,
			"low": None,
			"half_range": None,
			"parts": {
				"theta1_rad": theta1_rad,
				"theta2_rad": theta2_rad,
				"dtheta1_rad": dtheta1_rad,
				"dtheta2_rad": dtheta2_rad,
			},
		}

	# Nominal using Snell's law: n2 = sin(theta2)/sin(theta1) (assuming n1 = 1)
	nominal = math.sin(theta2_rad) / sin_theta1

	# High and low using range method
	# High: theta2 + dtheta2, theta1 - dtheta1
	sin_theta1_low = math.sin(theta1_rad - dtheta1_rad)
	if abs(sin_theta1_low) < 1e-12:
		return {
			"ok": False,
			"error": "sin(θ1 − Δθ1) is zero or too small; adjust uncertainties.",
			"nominal": None,
			"high": None,
			"low": None,
			"half_range": None,
			"parts": {
				"theta1_rad": theta1_rad,
				"theta2_rad": theta2_rad,
				"dtheta1_rad": dtheta1_rad,
				"dtheta2_rad": dtheta2_rad,
			},
		}
	high = math.sin(theta2_rad + dtheta2_rad) / sin_theta1_low

	# Low: theta2 − dtheta2, theta1 + dtheta1
	sin_theta1_high = math.sin(theta1_rad + dtheta1_rad)
	if abs(sin_theta1_high) < 1e-12:
		return {
			"ok": False,
			"error": "sin(θ1 + Δθ1) is zero or too small; adjust uncertainties.",
			"nominal": None,
			"high": None,
			"low": None,
			"half_range": None,
			"parts": {
				"theta1_rad": theta1_rad,
				"theta2_rad": theta2_rad,
				"dtheta1_rad": dtheta1_rad,
				"dtheta2_rad": dtheta2_rad,
			},
		}
	low = math.sin(theta2_rad - dtheta2_rad) / sin_theta1_high

	half_range = (high - low) / 2

	return {
		"ok": True,
		"error": None,
		"nominal": nominal,
		"high": high,
		"low": low,
		"half_range": half_range,
		"parts": {
			"theta1_rad": theta1_rad,
			"theta2_rad": theta2_rad,
			"dtheta1_rad": dtheta1_rad,
			"dtheta2_rad": dtheta2_rad,
		},
	}


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


def format_number(x: float, digits: int = 6) -> str:
	if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
		return "—"
	return f"{x:.{digits}g}"


# =============================
# Phase 1 – Inputs and Checking
# =============================
st.subheader("Enter Inputs and Check Your Results")

with st.container():
	col_a, col_b = st.columns(2)
	with col_a:
		st.markdown("**Angle Inputs (degrees)**")
		theta1_deg = st.number_input("θ1 (solid) [deg]", min_value=-89.9, max_value=89.9, value=30.0, step=0.1, format="%.4f")
		dtheta1_deg = st.number_input("Uncertainty in θ1 [deg]", min_value=0.0, max_value=10.0, value=0.5, step=0.1, format="%.4f")
		theta2_deg = st.number_input("θ2 (air) [deg]", min_value=-89.9, max_value=89.9, value=51.0, step=0.1, format="%.4f")
		dtheta2_deg = st.number_input("Uncertainty in θ2 [deg]", min_value=0.0, max_value=10.0, value=0.5, step=0.1, format="%.4f")

	with col_b:
		st.markdown("**Your Results**")
		student_nominal = st.number_input("Nominal n (your value)", value=1.5543, step=0.0001, format="%.6f")
		student_high = st.number_input("High n (your value)", value=1.5893, step=0.0001, format="%.6f")
		student_low = st.number_input("Low n (your value)", value=1.5203, step=0.0001, format="%.6f")
		student_half_range = st.number_input("Half-range (your value)", value=0.03449, step=0.00001, format="%.6f")

	# Track input changes: reset check gate when inputs change
	current_sig = (theta1_deg, dtheta1_deg, theta2_deg, dtheta2_deg, student_nominal, student_high, student_low, student_half_range)
	if "prev_sig" not in st.session_state:
		st.session_state.prev_sig = current_sig
	if "show_results" not in st.session_state:
		st.session_state.show_results = False
	if current_sig != st.session_state.prev_sig:
		st.session_state.prev_sig = current_sig
		st.session_state.show_results = False

	# Check Results button
	if st.button("Check Results"):
		st.session_state.show_results = True

	# Compute expected values
	calc = compute_refractive_indices(theta1_deg, theta2_deg, dtheta1_deg, dtheta2_deg)

	# Only show correctness after button click
	if st.session_state.show_results:
		if not calc["ok"]:
			st.error(calc["error"]) 
		else:
			expected_nominal = calc["nominal"]
			expected_high = calc["high"]
			expected_low = calc["low"]
			expected_half_range = calc["half_range"]

			# Feedback cards (hide correct values unless that field is correct)
			c1, c2, c3, c4 = st.columns(4)
			any_incorrect = False
			with c1:
				if is_close(student_nominal, expected_nominal):
					st.success(f"Nominal n ✓\n\nExpected: {format_number(expected_nominal, 6)}")
				else:
					st.error("Nominal n ✗ — try again")
					any_incorrect = True
			with c2:
				if is_close(student_high, expected_high):
					st.success(f"High n ✓\n\nExpected: {format_number(expected_high, 6)}")
				else:
					st.error("High n ✗ — try again")
					any_incorrect = True
			with c3:
				if is_close(student_low, expected_low):
					st.success(f"Low n ✓\n\nExpected: {format_number(expected_low, 6)}")
				else:
					st.error("Low n ✗ — try again")
					any_incorrect = True
			with c4:
				if is_close(student_half_range, expected_half_range):
					st.success(f"Half-range ✓\n\nExpected: {format_number(expected_half_range, 6)}")
				else:
					st.error("Half-range ✗ — try again")
					any_incorrect = True

			if any_incorrect:
				st.info("One or more values are incorrect. Please try again.")
			else:
				st.caption("Checks allow small rounding differences (±0.002 abs, 0.1% rel).")


# =============================
# Phase 2 – Common Errors (toggle)
# =============================
st.subheader("Common Errors")

if "show_common_errors" not in st.session_state:
	st.session_state.show_common_errors = False

if st.button("Common Errors" + (" (hide)" if st.session_state.show_common_errors else " (show)")):
	st.session_state.show_common_errors = not st.session_state.show_common_errors

if st.session_state.show_common_errors:
	st.markdown(
		"""
		- **Inverted ratio**: using sin(θ1)/sin(θ2) instead of sin(θ2)/sin(θ1).
		- **Forgetting max/min**: varying only one angle or using the same sign for both angles.
		- **Both plus signs**: `sin(θ2+Δθ2)/sin(θ1+Δθ1)` is incorrect for the high case.
		- **Degrees in trig**: not converting degrees to radians before using `sin`.
		- **Extreme angles**: choosing θ1 near 0° so sin(θ1) ≈ 0, causing blow-ups.
		"""
	)


# =============================
# Phase 3 – Step-by-Step (toggle)
# =============================
st.subheader("Step-by-Step Calculation")

if "show_steps" not in st.session_state:
	st.session_state.show_steps = False

if st.button("Step-by-Step Calculation" + (" (hide)" if st.session_state.show_steps else " (show)")):
	st.session_state.show_steps = not st.session_state.show_steps

if st.session_state.show_steps:
	calc = compute_refractive_indices(theta1_deg, theta2_deg, dtheta1_deg, dtheta2_deg)
	if not calc["ok"]:
		st.error(calc["error"]) 
	else:
		parts = calc["parts"]
		st.markdown("**Convert to radians**")
		st.markdown(
			f"θ1 = {theta1_deg:.6f}° → {parts['theta1_rad']:.6f} rad  ")
		st.markdown(
			f"Δθ1 = {dtheta1_deg:.6f}° → {parts['dtheta1_rad']:.6f} rad  ")
		st.markdown(
			f"θ2 = {theta2_deg:.6f}° → {parts['theta2_rad']:.6f} rad  ")
		st.markdown(
			f"Δθ2 = {dtheta2_deg:.6f}° → {parts['dtheta2_rad']:.6f} rad")

		st.divider()
		st.markdown("**Nominal refractive index (assuming n₁ = 1)**")
		st.latex(r"n = \dfrac{\sin(\theta_2)}{\sin(\theta_1)}")
		st.markdown(f"n = sin({parts['theta2_rad']:.6f}) / sin({parts['theta1_rad']:.6f}) = {calc['nominal']:.6f}")

		st.divider()
		st.markdown("**Range method for uncertainty**")
		st.markdown("High case: θ2 ↗, θ1 ↘")
		st.latex(r"n_{\text{high}} = \dfrac{\sin(\theta_2 + \Delta\theta_2)}{\sin(\theta_1 - \Delta\theta_1)}")
		high = calc["high"]
		st.markdown(
			f"n_high = sin({parts['theta2_rad'] + parts['dtheta2_rad']:.6f}) / sin({parts['theta1_rad'] - parts['dtheta1_rad']:.6f}) = {high:.6f}"
		)

		st.markdown("Low case: θ2 ↘, θ1 ↗")
		st.latex(r"n_{\text{low}} = \dfrac{\sin(\theta_2 - \Delta\theta_2)}{\sin(\theta_1 + \Delta\theta_1)}")
		low = calc["low"]
		st.markdown(
			f"n_low = sin({parts['theta2_rad'] - parts['dtheta2_rad']:.6f}) / sin({parts['theta1_rad'] + parts['dtheta1_rad']:.6f}) = {low:.6f}"
		)

		st.markdown("Half-range (uncertainty in n)")
		st.latex(r"\Delta n = \dfrac{n_{\text{high}} - n_{\text{low}}}{2}")
		st.markdown(f"Δn = ({high:.6f} − {low:.6f}) / 2 = {calc['half_range']:.6f}")

		st.info("Values update dynamically as you edit the four inputs above.")


