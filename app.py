import streamlit as st

st.set_page_config(
    page_title="Viva PHYS Lab Tutorial",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Viva PHYS Lab Interactive Tutorial")

st.markdown(
    """
Welcome! Use the sidebar to navigate through lab modules.

This tutorial includes interactive simulations and short checks for understanding. Data is kept local in your browser session.

- Start with "Projectile Motion" for a kinematics refresher
- Continue with "Oscillations" to explore mass–spring motion

Tip: You can export figures from most plots by using the toolbar in the top-right of each plot.
    """
)

with st.sidebar:
    st.header("Navigation")
    st.markdown(
        """
Use the built-in page list below to jump between modules.
        """
    )

st.subheader("Session Progress (local only)")
completed_modules = st.session_state.get("completed_modules", set())
col1, col2 = st.columns(2)
with col1:
    st.write("Completed modules:")
    if completed_modules:
        for module_name in sorted(completed_modules):
            st.checkbox(module_name, value=True, disabled=True)
    else:
        st.caption("No modules marked complete yet.")

with col2:
    st.write("Mark modules complete from within each page.")

st.divider()

st.markdown(
    """
If you are an instructor, you can duplicate and customize modules by editing files in the `pages` directory.
    """
)
