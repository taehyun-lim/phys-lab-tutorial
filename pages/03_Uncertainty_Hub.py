import streamlit as st
import importlib.util
import os

# Function to import module from file path
def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get the current directory (pages folder)
current_dir = os.path.dirname(__file__)

# Import all section modules
intro_module = import_module_from_path("intro", os.path.join(current_dir, "uncertainty_sections", "01_intro.py"))
precision_accuracy_module = import_module_from_path("precision_accuracy", os.path.join(current_dir, "uncertainty_sections", "02_precision_accuracy.py"))
uncertainty_range_module = import_module_from_path("uncertainty_range", os.path.join(current_dir, "uncertainty_sections", "03_uncertainty_range.py"))
one_measurement_module = import_module_from_path("one_measurement", os.path.join(current_dir, "uncertainty_sections", "04_one_measurement.py"))
range_method_module = import_module_from_path("range_method", os.path.join(current_dir, "uncertainty_sections", "05_range_method.py"))
std_dev_gaussian_module = import_module_from_path("std_dev_gaussian", os.path.join(current_dir, "uncertainty_sections", "06_std_dev_gaussian.py"))
standard_form_module = import_module_from_path("standard_form", os.path.join(current_dir, "uncertainty_sections", "07_standard_form.py"))

st.set_page_config(page_title="Uncertainty – Tutorial Hub", page_icon="±", layout="wide")

st.title("Uncertainty – Tutorial Hub")
st.caption("for Hamilton Physics 100 / 200 lab")

# Helper to normalize short free-text answers
def norm(s: str) -> str:
    return (s or "").strip().replace("+/-", "±").lower()

tabs = st.tabs(
    [
        "01 Intro to Error Analysis",
        "02 Precision & Accuracy", 
        "03 Uncertainty as Range",
        "04 One Measurement",
        "05 Range Method",
        "06 Std Dev & Gaussian",
        "07 Standard Form",
    ]
)

# Render each section using the modular functions
with tabs[0]:
    intro_module.render_intro_section()

with tabs[1]:
    precision_accuracy_module.render_precision_accuracy_section()

with tabs[2]:
    uncertainty_range_module.render_uncertainty_range_section()

with tabs[3]:
    one_measurement_module.render_one_measurement_section()

with tabs[4]:
    range_method_module.render_range_method_section()

with tabs[5]:
    std_dev_gaussian_module.render_std_dev_gaussian_section()

with tabs[6]:
    standard_form_module.render_standard_form_section()
