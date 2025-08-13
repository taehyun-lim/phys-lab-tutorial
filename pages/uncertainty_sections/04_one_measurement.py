import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_one_measurement_section():
    # Ensure trial tracker is initialized
    trial_tracker.initialize_session_state()
    
    st.header("Estimating uncertainty for one measurement")
    
    st.markdown(
        """
        Sometimes the best you can do is take one measurement. It may be tempting to think that one measurement is exact, but **even the best measurements in physics have an uncertainty associated with them**. You can determine the uncertainty in your measurement by **estimating the smallest and largest measurement you would believe**. This uncertainty will vary depending on the circumstances surrounding the measurement and is usually larger than the capabilities of your measuring device. The process may feel uncomfortable, but finding the believable extent of your measurement is a perfectly valid way of estimating your uncertainty when you only have one measurement.

        As an example, consider timing a friend in a crowded five-mile race. A stopwatch can measure time to 0.01 seconds, however you likely wouldn't feel comfortable with quoting your uncertainty to 0.01 seconds. It is much more reasonable that your ability to hit the stopwatch button consistently would vary by as much as 0.2 seconds. In this case the uncertainty in the measurement is not determined by the precision of the stopwatch, but the circumstances surrounding the measurement. Be aware that in this course we will often see that the uncertainty is larger than what one would expect based simply on the precision and accuracy of the measuring instrument.

        **Summary:** uncertainty shows what numbers you would believe. We use the plus or minus (±) symbol to indicate uncertainty.
        """
    )

    #st.subheader("Questions")
    st.markdown("**Q1.** Which is a reasonable measurement with uncertainty for the paperclip?")
    st.image(
        "uncertainty_google_forms/Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files/unnamed.png",
        #caption="Hitting a target requires both high precision and high accuracy",
        width=500
    )
    q4_1 = st.radio(
        "Select one",
        ["3.75 cm", "3.75", "3.75 ± 0.05 cm", "0.05 cm", "3.75 ± 0.2 cm"],
        index=None,
        key="om_q1",
    )
    
    question_id = "om_q1"
    
    if st.button("Check", key="om_q1_btn"):
        is_correct = q4_1 == "3.75 ± 0.05 cm"
        trial_tracker.record_attempt(question_id, is_correct, q4_1, "one_measurement")
        
        if is_correct:
            st.success("Correct! 3.75 ± 0.05 cm")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("one_measurement", "om_q2"):
        st.markdown("**Q2.** Which is a reasonable measurement with uncertainty for the pencil length?")
        st.image(
            "uncertainty_google_forms/Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files/unnamed(3).png",
            #caption="Hitting a target requires both high precision and high accuracy",
            width=500
        )
        q4_2 = st.radio(
            "Select one",
            ["4.5 ± 0.5 cm", "4 ± 1 cm", "4.10 ± 0.07 cm", "4.1 ± 0.0001 cm"],
            index=None,
            key="om_q2",
        )
        
        question_id = "om_q2"
        
        if st.button("Check", key="om_q2_btn"):
            is_correct = q4_2 == "4.10 ± 0.07 cm"
            trial_tracker.record_attempt(question_id, is_correct, q4_2, "one_measurement")
            
            if is_correct:
                st.success("Correct! 4.10 ± 0.07 cm")
            else:
                st.error("Try again")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
