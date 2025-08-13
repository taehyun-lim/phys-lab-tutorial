import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_standard_form_section():
    # Ensure trial tracker is initialized
    trial_tracker.initialize_session_state()
    
    st.header("Standard Form")
    
    st.markdown(
        """
        In order to save time and effort, we will often make rather crude estimates of the uncertainty in a measurement. To indicate that our uncertainties are only estimates, we normally report the uncertainty to only 1 significant figure. (Even in very careful scientific work, uncertainties are rarely reported to more than 2 significant figures.)

        For example, suppose that the time for a marble to fall a distance of 1.00 m is measured 6 times and the average is 0.48 s. The standard error is (0.0331 s)/√6 = 0.0135 s ≈ 0.01 s. The result, reported in **standard form** is

        t = (0.48 ± 0.01) s.
        or
        t = 0.48 ± 0.01 s.

        Notice that the last digit reported, the 8 in this example, is the digit that is uncertain. Both are reported to the tenths place.

        **Note**: Don't bother counting the number of significant figures for the value. This is a more sophisticated method of error analysis than significant figures.

        **Note**: Do not round too soon! Round only at the very end, after all calculations are complete. Use your calculator.

        **Note** that standard form is not the same thing as scientific notation, but you can combine them if you want. If the result and uncertainty are written in scientific notation, then the uncertainty should be written in scientific notation as well. For example:

        t = (4.8 × 10^-1) ± (1 × 10^-2) s. Both scientific notation and standard form.

        Standard form does require the formats to match, so this is NOT standard form:

        t = (4.8 × 10^-1) ± 0.1 s     [NOT standard form]

        because it makes it more difficult for the reader to interpret the measurement as a range of believable values.

        Usually we only use scientific notation when it makes the result more readable, and in scientific publications, metric prefixes are more common than scientific notation.

        **Summary instructions**:
        - Round the uncertainty to 1 significant figure.
        - Round the value to the same decimal place as the uncertainty. Match the format.
        - Write the value and uncertainty together as:    value  ± uncertainty unit
        """
    )

    # Q1: Which has 2 significant figures (the odd one out)
    st.markdown("**Q1.** All but one of these has 1 significant figure. Which one is the odd one out with 2 significant figures?")
    q7_1 = st.radio(
        "Select one",
        ["2.1 m", "3000000 m", "600 m", "2 m", "0.8 m", "0.000006 m", "They all have 1 significant figure"],
        index=None,
        key="sf_q1",
    )
    
    question_id = "sf_q1"
    
    if st.button("Check", key="sf_q1_btn"):
        is_correct = q7_1 == "2.1 m"
        trial_tracker.record_attempt(question_id, is_correct, q7_1, "standard_form")
        
        if is_correct:
            st.success("Correct! 2.1 m has 2 significant figures in the uncertainty.")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("standard_form", "sf_q2"):
        # Q2: Which is written in standard form
        st.markdown("**Q2.** Which one of these is written in standard form?")
        q7_2 = st.radio(
            "Select one",
            ["2362 ± 0.5 km", "2362.6 ± 4.6 km", "2362 ± 50 km", "2362.6 ± 5 km", "2362 ± 5 km", "2000 ± 0.5 km", "(2 × 10^3) ± 5 km", "(2.362 × 10^3) ± 5 km", "(2.362 × 10^6) ± 5000 m", "None of them"],
            index=None,
            key="sf_q2",
        )
        
        question_id = "sf_q2"
        
        if st.button("Check", key="sf_q2_btn"):
            is_correct = q7_2 == "2362 ± 5 km"
            trial_tracker.record_attempt(question_id, is_correct, q7_2, "standard_form")
            
            if is_correct:
                st.success("Correct! 2362 ± 5 km")
            else:
                st.error("Try again")

        # Q3 - only visible after Q2 is completed correctly
        if trial_tracker.can_access_question("standard_form", "sf_q3"):
            # Q3: Write in standard form (large number)
            st.markdown("**Q3.** Write this in standard form: 284629 ± 342 V (you may copy-paste the ± character or use +/-)")
            q7_3 = st.text_input("Your answer", key="sf_q3")
            
            question_id = "sf_q3"
            
            if st.button("Check", key="sf_q3_btn"):
                # Normalize the input to handle various formats
                user_input = (q7_3 or "").strip().replace("+/-", "±").replace("+/-", "±")
                correct_answers = ["284629 ± 342 V", "284629±342 V", "284629 ±342 V", "284629± 342 V"]
                is_correct = any(user_input == ans for ans in correct_answers)
                
                trial_tracker.record_attempt(question_id, is_correct, q7_3, "standard_form")
                
                if is_correct:
                    st.success("Correct! 284629 ± 342 V")
                else:
                    st.error("Try again. Round the uncertainty to 1 significant figure and the value to match.")

            # Q4 - only visible after Q3 is completed correctly
            if trial_tracker.can_access_question("standard_form", "sf_q4"):
                # Q4: Write in standard form (small number)
                st.markdown("**Q4.** Write this in standard form: .048294 ± 0.0003 V")
                q7_4 = st.text_input("Your answer", key="sf_q4")
                
                question_id = "sf_q4"
                
                if st.button("Check", key="sf_q4_btn"):
                    # Normalize the input to handle various formats
                    user_input = (q7_4 or "").strip().replace("+/-", "±").replace("+/-", "±")
                    correct_answers = ["0.048294 ± 0.0003 V", "0.048294±0.0003 V", "0.048294 ±0.0003 V", "0.048294± 0.0003 V"]
                    is_correct = any(user_input == ans for ans in correct_answers)
                    
                    trial_tracker.record_attempt(question_id, is_correct, q7_4, "standard_form")
                    
                    if is_correct:
                        st.success("Correct! 0.048294 ± 0.0003 V")
                    else:
                        st.error("Try again. Round the uncertainty to 1 significant figure and the value to match.")
            else:
                st.info("🔒 Complete Question 3 correctly to unlock Question 4.")
        else:
            st.info("🔒 Complete Question 2 correctly to unlock Question 3.")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
