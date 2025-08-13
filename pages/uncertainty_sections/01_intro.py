import streamlit as st

def render_intro_section():
    st.header("An Introduction to Error Analysis")
    
    st.subheader("Optional Questions")
    st.markdown("**What is your current understanding of uncertainty in measurements?**")
    q1_understanding = st.text_area(
        "Share your thoughts (optional)",
        placeholder="Describe what you currently know about uncertainty in measurements...",
        key="intro_understanding",
        height=100
    )
    
    st.markdown("**Which of the following topics are you most interested in learning about regarding uncertainty?**")
    q1_topics = st.multiselect(
        "Select topics (optional - choose multiple)",
        [
            "Definition of uncertainty",
            "Types of uncertainty (random vs. systematic)",
            "Estimating uncertainty for single measurements",
            "Standard deviation and standard error",
            "Reporting uncertainty in scientific contexts using standard form",
            "Graphing and uncertainty",
            "Propagation of uncertainty",
            "Judging whether two values are essentially the same or significantly different",
            "Other"
        ],
        key="intro_topics",
    )
    if q1_topics:
        st.info(f"You selected: {', '.join(q1_topics)}")
    
    st.markdown(
        """
        **"A man with a watch knows what time it is. A man with two watches is never sure."** (Segal's 'law')

        It is important to distinguish between the physics problems done in lecture and the situations that arise in this lab. In class, every problem is tailored to be as pristine as possible. Massless, frictionless, perfectly spherical objects often lead to one perfect solution to in class physics problems. The real world, however, is far messier than these problems would lead you to believe.

        **All measurements, no matter how good, involve some uncertainty in the result.**

        Error analysis is the study of that uncertainty. Knowledge of the uncertainty in a measurement is crucial for determining the reliability of a measurement.

        When reporting experimental results, physicists almost always include estimates of uncertainty, so that others can judge the quality of the results. Sometimes major advances in physics have depended on good error analysis.

        For example, it was known 150 years ago that the perihelion of Mercury, or point of closest approach to the sun, precessed very slowly about the sun at a rate of 1.555 degrees per century. Newton's theory of gravity predicted a precession of only 1.544 degrees. While these numbers were close, they did not agree to within the known uncertainties. A number of proposals were made to explain the discrepancy, but none were satisfactory. Finally, in 1915, Einstein showed that his General Theory of Relativity added 0.012 degrees to the prediction of Newton's theory, thus bringing theory into almost perfect agreement with experiment. This confirmation of Einstein's theory was critical for its acceptance by the scientific community as an improvement over Newton's theory.
        """
    )

    st.subheader("Quick Check")
    q1_3 = st.radio(
        "Do physicists care about estimating uncertainty for their measurements?",
        ["Yes", "No"],
        index=None,
        key="intro_q3",
    )
    if st.button("Check Answer", key="intro_q3_btn"):
        st.success("Correct! Physicists almost always include uncertainty estimates.") if q1_3 == "Yes" else st.error("Try again")
