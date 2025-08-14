import math
import streamlit as st


st.set_page_config(page_title="03 – Optics Lab", page_icon="🔭", layout="wide")

st.title("03 – Optics Lab: Thin Lens with Range-Method Uncertainty")
st.caption("Enter positions in cm. This tool checks your results and shows how the calculations are done.")


def compute_optics(
	object_pos_cm: float,
	lens_pos_cm: float,
	unc_lens_pos_cm: float,
	smallest_focal_pos_cm: float,
	largest_focal_pos_cm: float,
	assumed_do_abs_unc_cm: float = 0.2,
):
	"""Replicate the workbook calculations for one measurement row.

	Derived quantities (columns from the sheet):
	- best_focal_pos E = average(D, F)
	- object distance G = B − A
	- image distance H = E − B
	- unc image pos J = (F − D)/2
	- unc image distance K = J + C
	- 1/di L = 1/H
	- 1/do M = 1/G
	- 1/di max N = 1/(H − K), 1/di min O = 1/(H + K), unc 1/di P = (N − O)/2
	- 1/do max Q = 1/(G − 0.2), 1/do min R = 1/(G + 0.2), unc 1/do S = (Q − R)/2

	The do absolute uncertainty uses the fixed ±0.2 cm as per the sheet.
	"""

	E_best = (smallest_focal_pos_cm + largest_focal_pos_cm) / 2.0
	G_do = lens_pos_cm - object_pos_cm
	H_di = E_best - lens_pos_cm
	J_unc_image_pos = (largest_focal_pos_cm - smallest_focal_pos_cm) / 2.0
	K_unc_image_dist = J_unc_image_pos + unc_lens_pos_cm

	def safe_inv(x: float):
		if x is None or abs(x) < 1e-12:
			return None
		return 1.0 / x

	L_inv_di = safe_inv(H_di)
	M_inv_do = safe_inv(G_do)

	N_inv_di_max = safe_inv(H_di - K_unc_image_dist)
	O_inv_di_min = safe_inv(H_di + K_unc_image_dist)
	P_unc_inv_di = None
	if N_inv_di_max is not None and O_inv_di_min is not None:
		P_unc_inv_di = (N_inv_di_max - O_inv_di_min) / 2.0

	Q_inv_do_max = safe_inv(G_do - assumed_do_abs_unc_cm)
	R_inv_do_min = safe_inv(G_do + assumed_do_abs_unc_cm)
	S_unc_inv_do = None
	if Q_inv_do_max is not None and R_inv_do_min is not None:
		S_unc_inv_do = (Q_inv_do_max - R_inv_do_min) / 2.0

	return {
		"ok": (L_inv_di is not None and M_inv_do is not None),
		"error": None if (L_inv_di is not None and M_inv_do is not None) else "Object or image distance led to division by zero.",
		"inputs": {
			"A_object_pos": object_pos_cm,
			"B_lens_pos": lens_pos_cm,
			"C_unc_lens_pos": unc_lens_pos_cm,
			"D_smallest_focal_pos": smallest_focal_pos_cm,
			"F_largest_focal_pos": largest_focal_pos_cm,
			"assumed_do_abs_unc_cm": assumed_do_abs_unc_cm,
		},
		"derived": {
			"E_best_focal_pos": E_best,
			"G_object_distance": G_do,
			"H_image_distance": H_di,
			"J_unc_image_pos": J_unc_image_pos,
			"K_unc_image_distance": K_unc_image_dist,
			"L_inv_di": L_inv_di,
			"M_inv_do": M_inv_do,
			"N_inv_di_max": N_inv_di_max,
			"O_inv_di_min": O_inv_di_min,
			"P_unc_inv_di": P_unc_inv_di,
			"Q_inv_do_max": Q_inv_do_max,
			"R_inv_do_min": R_inv_do_min,
			"S_unc_inv_do": S_unc_inv_do,
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
		st.markdown("**Position Inputs (cm)**")
		A_object_pos = st.number_input("Object position A [cm]", value=10.0, step=0.1, format="%.4f")
		B_lens_pos = st.number_input("Lens position B [cm]", value=20.0, step=0.1, format="%.4f")
		C_unc_lens_pos = st.number_input("Uncertainty in lens position C [cm]", value=0.1, step=0.01, min_value=0.0, format="%.4f")
		D_smallest_focal = st.number_input("Smallest focal position D [cm]", value=58.2, step=0.1, format="%.4f")
		F_largest_focal = st.number_input("Largest focal position F [cm]", value=78.1, step=0.1, format="%.4f")
		assumed_do_unc = st.number_input("Assumed |Δdo| for reciprocal step [cm]", value=0.2, step=0.01, min_value=0.0, format="%.4f")

	with col_b:
		st.markdown("**Your Results**")
		G_object_distance = st.number_input("Object distance do = B − A [cm]", value=10.0, step=0.01, format="%.6f")
		H_image_distance = st.number_input("Image distance di = E − B [cm]", value=38.4, step=0.01, format="%.6f")
		J_unc_image_pos = st.number_input("Uncertainty in image position J = (F − D)/2 [cm]", value=(78.1-58.2)/2, step=0.01, format="%.6f")
		K_unc_image_dist = st.number_input("Uncertainty in image distance K = J + C [cm]", value=((78.1-58.2)/2)+0.1, step=0.01, format="%.6f")
		L_inv_di = st.number_input("1/di [cm⁻¹]", value=1.0/38.4, step=0.0001, format="%.6f")
		M_inv_do = st.number_input("1/do [cm⁻¹]", value=1.0/10.0, step=0.0001, format="%.6f")
		N_inv_di_max = st.number_input("1/di max [cm⁻¹]", value=1.0/(38.4-((78.1-58.2)/2+0.1)), step=0.0001, format="%.6f")
		O_inv_di_min = st.number_input("1/di min [cm⁻¹]", value=1.0/(38.4+((78.1-58.2)/2+0.1)), step=0.0001, format="%.6f")
		P_unc_inv_di = st.number_input("unc 1/di [cm⁻¹]", value=(1.0/(38.4-((78.1-58.2)/2+0.1)) - 1.0/(38.4+((78.1-58.2)/2+0.1)))/2.0, step=0.0001, format="%.6f")
		Q_inv_do_max = st.number_input("1/do max [cm⁻¹]", value=1.0/(10.0-assumed_do_unc), step=0.0001, format="%.6f")
		R_inv_do_min = st.number_input("1/do min [cm⁻¹]", value=1.0/(10.0+assumed_do_unc), step=0.0001, format="%.6f")
		S_unc_inv_do = st.number_input("unc 1/do [cm⁻¹]", value=(1.0/(10.0-assumed_do_unc)-1.0/(10.0+assumed_do_unc))/2.0, step=0.0001, format="%.6f")

	# Track input changes: reset check gate when inputs change
	current_sig = (
		A_object_pos, B_lens_pos, C_unc_lens_pos, D_smallest_focal, F_largest_focal, assumed_do_unc,
		G_object_distance, H_image_distance, J_unc_image_pos, K_unc_image_dist, L_inv_di, M_inv_do,
		N_inv_di_max, O_inv_di_min, P_unc_inv_di, Q_inv_do_max, R_inv_do_min, S_unc_inv_do,
	)
	if "prev_sig_optics" not in st.session_state:
		st.session_state.prev_sig_optics = current_sig
	if "show_results_optics" not in st.session_state:
		st.session_state.show_results_optics = False
	if current_sig != st.session_state.prev_sig_optics:
		st.session_state.prev_sig_optics = current_sig
		st.session_state.show_results_optics = False

	# Check Results button
	if st.button("Check Results"):
		st.session_state.show_results_optics = True

	# Compute expected values
	calc = compute_optics(
		object_pos_cm=A_object_pos,
		lens_pos_cm=B_lens_pos,
		unc_lens_pos_cm=C_unc_lens_pos,
		smallest_focal_pos_cm=D_smallest_focal,
		largest_focal_pos_cm=F_largest_focal,
		assumed_do_abs_unc_cm=assumed_do_unc,
	)

	# Only show correctness after button click
	if st.session_state.show_results_optics:
		if not calc["ok"]:
			st.error(calc["error"]) 
		else:
			d = calc["derived"]
			c1, c2, c3 = st.columns(3)
			with c1:
				if is_close(G_object_distance, d["G_object_distance"]):
					st.success(f"do ✓\n\nExpected: {format_number(d['G_object_distance'], 6)} cm")
				else:
					st.error("do ✗ — try again")
			with c2:
				if is_close(H_image_distance, d["H_image_distance"]):
					st.success(f"di ✓\n\nExpected: {format_number(d['H_image_distance'], 6)} cm")
				else:
					st.error("di ✗ — try again")
			with c3:
				if is_close(J_unc_image_pos, d["J_unc_image_pos"]):
					st.success(f"unc image pos ✓\n\nExpected: {format_number(d['J_unc_image_pos'], 6)} cm")
				else:
					st.error("unc image pos ✗ — try again")

			c4, c5, c6 = st.columns(3)
			with c4:
				if is_close(K_unc_image_dist, d["K_unc_image_distance"]):
					st.success(f"unc image distance ✓\n\nExpected: {format_number(d['K_unc_image_distance'], 6)} cm")
				else:
					st.error("unc image distance ✗ — try again")
			with c5:
				if is_close(L_inv_di, d["L_inv_di"]):
					st.success(f"1/di ✓\n\nExpected: {format_number(d['L_inv_di'], 6)} cm⁻¹")
				else:
					st.error("1/di ✗ — try again")
			with c6:
				if is_close(M_inv_do, d["M_inv_do"]):
					st.success(f"1/do ✓\n\nExpected: {format_number(d['M_inv_do'], 6)} cm⁻¹")
				else:
					st.error("1/do ✗ — try again")

			c7, c8, c9 = st.columns(3)
			with c7:
				if is_close(N_inv_di_max, d["N_inv_di_max"]):
					st.success(f"1/di max ✓\n\nExpected: {format_number(d['N_inv_di_max'], 6)} cm⁻¹")
				else:
					st.error("1/di max ✗ — try again")
			with c8:
				if is_close(O_inv_di_min, d["O_inv_di_min"]):
					st.success(f"1/di min ✓\n\nExpected: {format_number(d['O_inv_di_min'], 6)} cm⁻¹")
				else:
					st.error("1/di min ✗ — try again")
			with c9:
				if is_close(P_unc_inv_di, d["P_unc_inv_di"]):
					st.success(f"unc 1/di ✓\n\nExpected: {format_number(d['P_unc_inv_di'], 6)} cm⁻¹")
				else:
					st.error("unc 1/di ✗ — try again")

			c10, c11, c12 = st.columns(3)
			with c10:
				if is_close(Q_inv_do_max, d["Q_inv_do_max"]):
					st.success(f"1/do max ✓\n\nExpected: {format_number(d['Q_inv_do_max'], 6)} cm⁻¹")
				else:
					st.error("1/do max ✗ — try again")
			with c11:
				if is_close(R_inv_do_min, d["R_inv_do_min"]):
					st.success(f"1/do min ✓\n\nExpected: {format_number(d['R_inv_do_min'], 6)} cm⁻¹")
				else:
					st.error("1/do min ✗ — try again")
			with c12:
				if is_close(S_unc_inv_do, d["S_unc_inv_do"]):
					st.success(f"unc 1/do ✓\n\nExpected: {format_number(d['S_unc_inv_do'], 6)} cm⁻¹")
				else:
					st.error("unc 1/do ✗ — try again")


# =============================
# Phase 2 – Step-by-Step (toggle)
# =============================
st.subheader("Step-by-Step Calculation")

if "show_steps_optics" not in st.session_state:
	st.session_state.show_steps_optics = False

if st.button("Step-by-Step Calculation" + (" (hide)" if st.session_state.show_steps_optics else " (show)")):
	st.session_state.show_steps_optics = not st.session_state.show_steps_optics

if st.session_state.show_steps_optics:
	calc = compute_optics(
		object_pos_cm=A_object_pos,
		lens_pos_cm=B_lens_pos,
		unc_lens_pos_cm=C_unc_lens_pos,
		smallest_focal_pos_cm=D_smallest_focal,
		largest_focal_pos_cm=F_largest_focal,
		assumed_do_abs_unc_cm=assumed_do_unc,
	)
	if not calc["ok"]:
		st.error(calc["error"]) 
	else:
		d = calc["derived"]
		st.markdown("**Best focal position**")
		st.markdown(f"E = average(D, F) = ({D_smallest_focal:.6f} + {F_largest_focal:.6f})/2 = {d['E_best_focal_pos']:.6f} cm")

		st.divider()
		st.markdown("**Distances**")
		st.markdown(f"do = B − A = {B_lens_pos:.6f} − {A_object_pos:.6f} = {d['G_object_distance']:.6f} cm")
		st.markdown(f"di = E − B = {d['E_best_focal_pos']:.6f} − {B_lens_pos:.6f} = {d['H_image_distance']:.6f} cm")

		st.divider()
		st.markdown("**Uncertainties (range method)**")
		st.markdown(f"J = (F − D)/2 = ({F_largest_focal:.6f} − {D_smallest_focal:.6f})/2 = {d['J_unc_image_pos']:.6f} cm")
		st.markdown(f"K = J + C = {d['J_unc_image_pos']:.6f} + {C_unc_lens_pos:.6f} = {d['K_unc_image_distance']:.6f} cm")

		st.divider()
		st.markdown("**Reciprocals**")
		st.markdown(f"1/di = 1/({d['H_image_distance']:.6f}) = {format_number(d['L_inv_di'], 6)} cm⁻¹")
		st.markdown(f"1/do = 1/({d['G_object_distance']:.6f}) = {format_number(d['M_inv_do'], 6)} cm⁻¹")

		st.divider()
		st.markdown("**Reciprocal uncertainty (image)**")
		st.markdown(f"1/di_max = 1/(di − K) = 1/({d['H_image_distance']:.6f} − {d['K_unc_image_distance']:.6f}) = {format_number(d['N_inv_di_max'], 6)} cm⁻¹")
		st.markdown(f"1/di_min = 1/(di + K) = 1/({d['H_image_distance']:.6f} + {d['K_unc_image_distance']:.6f}) = {format_number(d['O_inv_di_min'], 6)} cm⁻¹")
		st.markdown(f"unc 1/di = (max − min)/2 = ({format_number(d['N_inv_di_max'], 6)} − {format_number(d['O_inv_di_min'], 6)})/2 = {format_number(d['P_unc_inv_di'], 6)} cm⁻¹")

		st.divider()
		st.markdown("**Reciprocal uncertainty (object)**")
		st.markdown(f"Using |Δdo| = {assumed_do_unc:.6f} cm")
		st.markdown(f"1/do_max = 1/(do − |Δdo|) = 1/({d['G_object_distance']:.6f} − {assumed_do_unc:.6f}) = {format_number(d['Q_inv_do_max'], 6)} cm⁻¹")
		st.markdown(f"1/do_min = 1/(do + |Δdo|) = 1/({d['G_object_distance']:.6f} + {assumed_do_unc:.6f}) = {format_number(d['R_inv_do_min'], 6)} cm⁻¹")
		st.markdown(f"unc 1/do = (max − min)/2 = ({format_number(d['Q_inv_do_max'], 6)} − {format_number(d['R_inv_do_min'], 6)})/2 = {format_number(d['S_unc_inv_do'], 6)} cm⁻¹")


