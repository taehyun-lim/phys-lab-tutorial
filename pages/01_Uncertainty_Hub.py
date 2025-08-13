import streamlit as st
import streamlit.components.v1 as components
import importlib.util
import os
import sys

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

# Initialize the trial tracker session state
trial_tracker.initialize_session_state()

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

st.set_page_config(page_title="Uncertainty – Tutorial Hub", page_icon="±", layout="wide", initial_sidebar_state="expanded")

# Global top-of-page anchor for reliable scrolling
st.markdown('<div id="page-top"></div>', unsafe_allow_html=True)

st.title("Uncertainty – Tutorial Hub")
st.caption("for Hamilton Physics 100 / 200 lab")

# Email collection (only show if not already collected)
current_email = trial_tracker.get_student_email()
if not current_email or current_email == "Not provided":
    st.info("📧 Please provide your Hamilton College email address to continue with the tutorial.")
    email = st.text_input("Email Address", placeholder="your.name@hamilton.edu", key="student_email")
    
    if st.button("Continue", key="email_continue"):
        if trial_tracker.set_student_email(email):
            st.success("Thank you! You can now proceed with the tutorial.")
            st.rerun()
        else:
            st.error("Please enter a valid Hamilton College email address (ending with @hamilton.edu).")

    # Don't show the rest of the tutorial until email is provided
    st.stop()

# Navigation sidebar with progress tracking
with st.sidebar:
    st.header("Progress")
    
    # Show progress
    progress = trial_tracker.get_progress_summary()
    st.metric("Progress", f"{progress['progress_percentage']}%")
    st.metric("Sections Completed", f"{progress['completed_sections']}/{progress['total_sections']}")
    
    if progress['next_section']:
        st.info(f"Next: {progress['next_section'].replace('_', ' ').title()}")
    
    # Export button for instructors (password protected)
    st.divider()
    st.header("Instructor Tools")
    
    # Password input for CSV download
    csv_password = st.text_input("Password", type="password", key="csv_password")
    
    if st.button("📥 Export Data to CSV"):
        if csv_password:
            csv_path, message = trial_tracker.export_to_csv(password=csv_password)
            if csv_path:
                st.success(f"Data exported successfully!")
                
                # Create a download link
                with open(csv_path, 'r') as f:
                    csv_content = f.read()
                st.download_button(
                    label="Download CSV",
                    data=csv_content,
                    file_name=os.path.basename(csv_path),
                    mime="text/csv"
                )
            else:
                st.error(f"Export failed: {message}")
        else:
            st.warning("Please enter the password to download CSV data.")

# Helper to normalize short free-text answers
def norm(s: str) -> str:
    return (s or "").strip().replace("+/-", "±").lower()

# Initialize active tab if not set
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# Function to handle tab switching
def switch_to_tab(tab_index):
    st.session_state.active_tab = tab_index
    st.rerun()

# Add scroll-to-top functionality when tabs change
if "previous_tab" not in st.session_state:
    st.session_state.previous_tab = st.session_state.active_tab

# Check if tab changed and scroll to top
if st.session_state.previous_tab != st.session_state.active_tab:
    # Simple scroll to top when tab changes
    st.markdown(
        """
        <script>
        // Simple scroll to top
        window.scrollTo(0, 0);
        </script>
        """,
        unsafe_allow_html=True
    )
    
    st.session_state.previous_tab = st.session_state.active_tab

# Create custom tab navigation that looks like tabs
tab_names = [
    "01 Intro to Error Analysis", 
    "02 Precision & Accuracy", 
    "03 Uncertainty as Range",
    "04 One Measurement", 
    "05 Range Method", 
    "06 Std Dev & Gaussian", 
    "07 Standard Form"
]

# Create tab buttons in a row with custom styling
cols = st.columns(len(tab_names))
for i, (col, name) in enumerate(zip(cols, tab_names)):
    with col:
        if i == st.session_state.active_tab:
            # Active tab - highlighted
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f2f6; 
                    border: 2px solid #0068c9; 
                    border-radius: 8px 8px 0px 0px; 
                    padding: 10px; 
                    text-align: center; 
                    font-weight: bold; 
                    color: #0068c9;
                    margin-bottom: 0px;
                ">
                    {name}
                </div>
                """,
                unsafe_allow_html=True
            )
        elif trial_tracker.can_access_section(trial_tracker.sections[i]):
            # Accessible tab - clickable
            if st.button(
                name, 
                key=f"tab_{i}",
                help=f"Click to go to {name}",
                use_container_width=True
            ):
                st.session_state.active_tab = i
                st.rerun()
        else:
            # Locked tab - disabled
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f2f6; 
                    border: 2px solid #cccccc; 
                    border-radius: 8px 8px 0px 0px; 
                    padding: 10px; 
                    text-align: center; 
                    color: #999999;
                    margin-bottom: 0px;
                ">
                    🔒 {name}
                </div>
                """,
                unsafe_allow_html=True
            )

# Add a separator line below the tabs
st.markdown(
    """
    <div style="
        border-top: 2px solid #0068c9; 
        margin-top: 0px; 
        margin-bottom: 20px;
    "></div>
    """,
    unsafe_allow_html=True
)

# Helper to render a section with navigation buttons
def render_section_with_nav(section_index, render_callable):
    anchor_id = f"section-{section_index}-top"

    # Anchor at the top of the section content
    st.markdown(f'<div id="{anchor_id}"></div>', unsafe_allow_html=True)

    # Render the actual section content
    render_callable()

    # Navigation buttons at the end of the section
    left_col, right_col = st.columns(2)
    with left_col:
        if st.button("Back to Top", key=f"back_to_top_{section_index}"):
            st.session_state["scroll_to_element_id"] = "__PAGE_TOP__"
            st.rerun()
    with right_col:
        if section_index < len(tab_names) - 1:
            if st.button("Next Section", key=f"next_section_{section_index}"):
                # Only navigate if next section is accessible; otherwise, inform the user
                try:
                    next_section_key = trial_tracker.sections[section_index + 1]
                    if trial_tracker.can_access_section(next_section_key):
                        st.session_state.active_tab = section_index + 1
                        st.session_state["scroll_to_element_id"] = "__PAGE_TOP__"
                        st.rerun()
                    else:
                        st.warning("This section is locked. Complete the current section's final question to unlock the next section.")
                except Exception:
                    # Fallback: still attempt to navigate
                    st.session_state.active_tab = section_index + 1
                    st.session_state["scroll_to_element_id"] = "__PAGE_TOP__"
                    st.rerun()

# Render the active section content
if st.session_state.active_tab == 0:
    render_section_with_nav(0, intro_module.render_intro_section)
elif st.session_state.active_tab == 1:
    if trial_tracker.can_access_section("precision_accuracy"):
        render_section_with_nav(1, precision_accuracy_module.render_precision_accuracy_section)
    else:
        st.warning("🔒 This section is locked. Complete the Introduction section to unlock it.")
elif st.session_state.active_tab == 2:
    if trial_tracker.can_access_section("uncertainty_range"):
        render_section_with_nav(2, uncertainty_range_module.render_uncertainty_range_section)
    else:
        st.warning("🔒 This section is locked. Complete the Precision & Accuracy section to unlock it.")
elif st.session_state.active_tab == 3:
    if trial_tracker.can_access_section("one_measurement"):
        render_section_with_nav(3, one_measurement_module.render_one_measurement_section)
    else:
        st.warning("🔒 This section is locked. Complete the Uncertainty as Range section to unlock it.")
elif st.session_state.active_tab == 4:
    if trial_tracker.can_access_section("range_method"):
        render_section_with_nav(4, range_method_module.render_range_method_section)
    else:
        st.warning("🔒 This section is locked. Complete the One Measurement section to unlock it.")
elif st.session_state.active_tab == 5:
    if trial_tracker.can_access_section("std_dev_gaussian"):
        render_section_with_nav(5, std_dev_gaussian_module.render_std_dev_gaussian_section)
    else:
        st.warning("🔒 This section is locked. Complete the Range Method section to unlock it.")
elif st.session_state.active_tab == 6:
    if trial_tracker.can_access_section("standard_form"):
        render_section_with_nav(6, standard_form_module.render_standard_form_section)
    else:
        st.warning("🔒 This section is locked. Complete the Std Dev & Gaussian section to unlock it.")

# Mark session as complete when all accessible tabs are visited
trial_tracker.mark_session_complete()

# Perform any pending scroll action at the very end of the render
pending_anchor_id = st.session_state.get("scroll_to_element_id")
if pending_anchor_id:
    if pending_anchor_id == "__PAGE_TOP__":
        components.html(
            """
            <script>
            (function(){
              function scrollToTopRobust(){
                try {
                  var root = window.parent || window;
                  if (root && root.scrollTo) { root.scrollTo({ top: 0, left: 0, behavior: 'smooth' }); }
                  var pd = (window.parent && window.parent.document) ? window.parent.document : null;
                  var target = null;
                  if (pd) {
                    target = pd.getElementById('page-top') || pd.body || pd.documentElement;
                  }
                  if (!target) {
                    target = document.getElementById('page-top') || document.body || document.documentElement;
                  }
                  if (target && target.scrollIntoView) { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
                } catch (e) {}
              }
              scrollToTopRobust();
              setTimeout(scrollToTopRobust, 50);
              setTimeout(scrollToTopRobust, 150);
              setTimeout(scrollToTopRobust, 300);
              requestAnimationFrame(scrollToTopRobust);
            })();
            </script>
            """,
            height=0,
        )
    else:
        components.html(
            f"""
            <script>
            (function(){{
              function tryScrollToId(){{
                try {{
                  var rootDoc = (window.parent && window.parent.document) ? window.parent.document : document;
                  var el = rootDoc.getElementById("{pending_anchor_id}") || document.getElementById("{pending_anchor_id}");
                  if (el && el.scrollIntoView) {{
                    el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                  }} else {{
                    if (window.parent && window.parent.scrollTo) {{ window.parent.scrollTo({{ top: 0, left: 0, behavior: 'smooth' }}); }}
                    if (window.scrollTo) {{ window.scrollTo({{ top: 0, left: 0, behavior: 'smooth' }}); }}
                  }}
                }} catch (e) {{}}
              }}
              tryScrollToId();
              setTimeout(tryScrollToId, 50);
              setTimeout(tryScrollToId, 150);
              requestAnimationFrame(tryScrollToId);
            }})();
            </script>
            """,
            height=0,
        )
    st.session_state["scroll_to_element_id"] = None
