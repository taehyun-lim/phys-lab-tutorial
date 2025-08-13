import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_uncertainty_range_section():
    # Ensure trial tracker is initialized
    trial_tracker.initialize_session_state()
    
    st.header("Uncertainty as a range of believable values")
    
    st.markdown(
        """
        - "Tomorrow the highs will be in the 70s."
        - "It's about 4 and a half hours to New York City."
        - "We'll be ready in 5 to 7 business days."

        Each of the above uncertain predictions can be communicated as range or as a best value and an uncertainty.

        In physics, we prefer to give the best value and uncertainty using the plus or minus (±) symbol.

        **For example:** "55 ± 4 m" means the best value is 55 meters and the believable range is 51 to 59 meters.

        You will almost always use uncertainty as a measure of the random error, not the systematic error, though it can be used for both.
        """
    )

    #st.subheader("Quiz")
    st.markdown("**Q1.** What is the lowest believable value that corresponds to 6 ± 1 days?")
    q3_1 = st.radio("Select one", ["3 days", "4 days", "5 days", "6 days"], index=None, key="uncertainty_q1")
    
    question_id = "uncertainty_q1"
    
    if st.button("Check", key="uncertainty_q1_btn"):
        is_correct = q3_1 == "5 days"
        trial_tracker.record_attempt(question_id, is_correct, q3_1, "uncertainty_range")
        
        if is_correct:
            st.success("Correct! 5 days")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("uncertainty_range", "uncertainty_q2"):
        st.markdown("**Q2.** \"Tomorrow the highs will be in the 70s.\" Please pick the best way to interpret this temperature.")
        q3_2 = st.radio(
            "Select one",
            ["75 ± 5 ºF", "75 ± 5 ºC", "70 ± 10 ºF", "70 ± 10 ºC", "80 ± 10 ºF"],
            index=None,
            key="uncertainty_q2",
        )
        
        question_id = "uncertainty_q2"
        
        if st.button("Check", key="uncertainty_q2_btn"):
            is_correct = q3_2 == "75 ± 5 ºF"
            trial_tracker.record_attempt(question_id, is_correct, q3_2, "uncertainty_range")
            
            if is_correct:
                st.success("Correct! 75 ± 5 ºF")
            else:
                st.error("Try again")

        # Q3 - only visible after Q2 is completed correctly
        if trial_tracker.can_access_question("uncertainty_range", "uncertainty_q3"):
            st.markdown("**Q3.** What is the highest believable value that corresponds to 385000 ± 1000 km? (The distance to the moon!)")
            st.caption("Please use km as your units and include the units in your answer.")
            q3_3 = st.text_input("Your answer", key="uncertainty_q3")
            
            question_id = "uncertainty_q3"
            
            if st.button("Check", key="uncertainty_q3_btn"):
                ok = q3_3.strip().lower() in {"386000 km", "386000km", "386000 kilometers", "386000kilometers"}
                trial_tracker.record_attempt(question_id, ok, q3_3, "uncertainty_range")
                
                if ok:
                    st.success("Accepted! 386000 km")
                else:
                    st.error("Expected 386000 km")

            # Q4 - only visible after Q3 is completed correctly
            if trial_tracker.can_access_question("uncertainty_range", "uncertainty_q4"):
                st.markdown("**Q4.** A student measures the voltage of a battery 10 times using a digital multimeter and obtains the following results:")
                st.markdown(
                    "1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V<br>1.5 V",
                    unsafe_allow_html=True
                )
                st.markdown("What is the best way to communicate this set of measurements?")
                q3_4 = st.radio(
                    "Select one",
                    ["1.5 V", "1.5 ± 0.0 V", "1.50 ± 0.05 V"],
                    index=None,
                    key="uncertainty_q4",
                )
                
                question_id = "uncertainty_q4"
                
                if st.button("Check", key="uncertainty_q4_btn"):
                    is_correct = q3_4 == "1.50 ± 0.05 V"
                    trial_tracker.record_attempt(question_id, is_correct, q3_4, "uncertainty_range")
                    
                    if is_correct:
                        st.success("Correct! 1.50 ± 0.05 V")
                    else:
                        st.error("Try again")
            else:
                st.info("🔒 Complete Question 3 correctly to unlock Question 4.")
        else:
            st.info("🔒 Complete Question 2 correctly to unlock Question 3.")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
