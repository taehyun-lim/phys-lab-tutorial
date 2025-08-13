import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_precision_accuracy_section():
    """Render the precision and accuracy section"""
    # Initialize the trial tracker session state
    trial_tracker.initialize_session_state()
    
    st.header("Precision and Accuracy")
    
    # Add the target image
    st.markdown("**Hitting a target requires both high precision and high accuracy**")
    st.image(
        "uncertainty_google_forms/Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files/unnamed(1).jpg",
        #caption="Hitting a target requires both high precision and high accuracy",
        width=500
    )
    
    st.markdown(
        """
        A lack of accuracy provides evidence of systematic error. Systematic error occurs when the real world doesn't match an expected model, for example, when measurement tools aren't calibrated correctly.

        A lack of precision is called random error. We can measure random error by seeing the variation from one trial to another.
        """
    )

    #st.subheader("Questions")
    st.markdown("**Q1.** \"Random error\" refers to")
    q2_1 = st.radio(
        "Select one",
        [
            "a lack of precision", 
            "a lack of accuracy"
        ],
        index=None,
        key="pa_q1",
    )
    
    question_id = "pa_q1"
    
    if st.button("Check Q1", key="pa_q1_btn"):
        is_correct = q2_1 == "a lack of precision"
        trial_tracker.record_attempt(question_id, is_correct, q2_1, "precision_accuracy")
        
        if is_correct:
            st.success("Correct! Random error refers to a lack of precision.")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("precision_accuracy", "pa_q2"):
        st.markdown("**Q2.** \"Systematic error\" refers to")
        q2_2 = st.radio(
            "Select one",
            [
                "a lack of precision",
                "a lack of accuracy"
            ],
            index=None,
            key="pa_q2",
        )
        
        question_id = "pa_q2"
        
        if st.button("Check Q2", key="pa_q2_btn"):
            is_correct = q2_2 == "a lack of accuracy"
            trial_tracker.record_attempt(question_id, is_correct, q2_2, "precision_accuracy")
            
            if is_correct:
                st.success("Correct! Systematic error refers to a lack of accuracy.")
            else:
                st.error("Try again")

        # Q3 - only visible after Q2 is completed correctly
        if trial_tracker.can_access_question("precision_accuracy", "pa_q3"):
            # Text content that appears after Q2 is completed correctly
            st.markdown(
                """
                **Unless you are counting an integer, there is ALWAYS systematic error and ALWAYS random error in a measurement. We try to make both small.**

                **Precision** refers to the degree of reproducibility of the measurement. For example, a mercury thermometer marked in 1º increments can probably be read reliably to the nearest 0.2º. Thus two people using the same thermometer might disagree on the temperature of a liquid, but they probably would not disagree by more than 0.2º. In this case, any disagreement is due to randomness in judging the exact position of the mercury. In general, precision refers to the size of the **random errors** that affect the result of a measurement.

                **Accuracy** refers to how close the result is to the actual (true) value. For example, the temperature shown on a mercury thermometer might be different from the actual temperature (inaccurate) because of an imperfect calibration of the thermometer. In this case the disagreement is due to a problem with the system used to make the measurement. In general, accuracy refers to the size of the **systematic errors** that affect the result of a measurement.

                As an example, suppose that you ride your bicycle to the Clinton Hannaford a number of times and your bike odometer reads 1.7 miles, 1.8 miles, 1.8 miles, and 1.7 miles. The tenth of a mile variation indicates the precision of the measurement, and the variation might be due to random wiggles in your riding. On the other hand suppose you drive the same distance and you find that your car odometer reads 2.0 miles. The difference indicates a systematic error; one, or both, of the odometers must be measuring the distance incorrectly.

                When we repeat an experiment a number of times and examine the variation in the data, we are obtaining information about the random errors in the experiment but we learn nothing about the systematic errors. This is because **systematic errors affect all measurements in the same way**. Suppose a stopwatch is designed for operation between 50ºF and 80ºF and when the temperature is above 80º F it runs too fast. If the measurements were made when the temperature was 90ºF, then all of the time readings would be too large. We have no way of knowing about this effect from examining the variation in the data.

                **Note: We don't use the term "human error". Usually the correct term is "systematic error".**
                """
            )

            st.markdown("**Q3.** Random error is most likely caused by:")
            q2_3 = st.radio(
                "Select one",
                [
                    "A measuring device that hasn't been calibrated",
                    "A consistent mistake in the design of the apparatus", 
                    "Fluctuations that vary unpredictably from trial to trial",
                    "Using a faulty method to analyze results"
                ],
                index=None,
                key="pa_q3",
            )
            
            question_id = "pa_q3"
            
            if st.button("Check Q3", key="pa_q3_btn"):
                is_correct = q2_3 == "Fluctuations that vary unpredictably from trial to trial"
                trial_tracker.record_attempt(question_id, is_correct, q2_3, "precision_accuracy")
                
                if is_correct:
                    st.success("Correct! Random error is caused by fluctuations that vary unpredictably from trial to trial.")
                else:
                    st.error("Try again")

            # Q4 - only visible after Q3 is completed correctly
            if trial_tracker.can_access_question("precision_accuracy", "pa_q4"):
                st.markdown("**Q4.** Systematic errors can possibly be reduced by:")
                q2_4 = st.radio(
                    "Select one",
                    [
                        "Averaging the results from many trials using the same technique and instruments",
                        "Comparing to a known, more reliable measurement",
                        "Recording more digits from the measurement tool",
                        "Rounding your measurements to the nearest whole number"
                    ],
                    index=None,
                    key="pa_q4",
                )
                
                question_id = "pa_q4"
                
                if st.button("Check Q4", key="pa_q4_btn"):
                    is_correct = q2_4 == "Comparing to a known, more reliable measurement"
                    trial_tracker.record_attempt(question_id, is_correct, q2_4, "precision_accuracy")
                    
                    if is_correct:
                        st.success("Correct! Systematic errors can be reduced by comparing to a known, more reliable measurement.")
                    else:
                        st.error("Try again")

                # Q5 - only visible after Q4 is completed correctly
                if trial_tracker.can_access_question("precision_accuracy", "pa_q5"):
                    st.markdown("**Q5.** Which type of error is this?")
                    st.markdown("A student measures the temperature of a solid object using a thermometer, but the thermometer is not in good thermal contact with the object. The student and their lab partner independently take the measurement of the thermometer and obtain similar results, but neither one notices the thermal contact problem.")
                    q2_5 = st.radio(
                        "Select one",
                        ["random error", "systematic error"],
                        index=None,
                        key="pa_q5",
                    )
                    
                    question_id = "pa_q5"
                    
                    if st.button("Check Q5", key="pa_q5_btn"):
                        is_correct = q2_5 == "systematic error"
                        trial_tracker.record_attempt(question_id, is_correct, q2_5, "precision_accuracy")
                        
                        if is_correct:
                            st.success("Correct! This is a systematic error - the same problem affects all measurements.")
                        else:
                            st.error("Try again")

                    # Q6 - only visible after Q5 is completed correctly
                    if trial_tracker.can_access_question("precision_accuracy", "pa_q6"):
                        st.markdown("**Q6.** Which type of error is this?")
                        st.markdown("A student is measuring voltage using a voltmeter, but the voltmeter is fluctuating up and down. There is electronic noise in the circuit. The student records a variety of different numbers while conducting repeated trials of the same experiment.")
                        q2_6 = st.radio(
                            "Select one",
                            ["random error", "systematic error"],
                            index=None,
                            key="pa_q6",
                        )
                        
                        question_id = "pa_q6"
                        
                        if st.button("Check Q6", key="pa_q6_btn"):
                            is_correct = q2_6 == "random error"
                            trial_tracker.record_attempt(question_id, is_correct, q2_6, "precision_accuracy")
                            
                            if is_correct:
                                st.success("Correct! This is a random error - the fluctuations vary unpredictably from trial to trial.")
                            else:
                                st.error("Try again")

                        # Q7 - only visible after Q6 is completed correctly
                        if trial_tracker.can_access_question("precision_accuracy", "pa_q7"):
                            st.markdown("**Q7.** Which type of error is this?")
                            st.markdown("A physicist makes a mathematical approximation assuming that a certain angle is small (the small-angle approximation), but in fact the angle is rather large, so the calculation doesn't match the situation.")
                            q2_7 = st.radio(
                                "Select one",
                                ["random error", "systematic error"],
                                index=None,
                                key="pa_q7",
                            )
                            
                            question_id = "pa_q7"
                            
                            if st.button("Check Q7", key="pa_q7_btn"):
                                is_correct = q2_7 == "systematic error"
                                trial_tracker.record_attempt(question_id, is_correct, q2_7, "precision_accuracy")
                                
                                if is_correct:
                                    st.success("Correct! This is a systematic error - the same approximation error affects all calculations.")
                                else:
                                    st.error("Try again")

                            # Q8 - only visible after Q7 is completed correctly
                            if trial_tracker.can_access_question("precision_accuracy", "pa_q8"):
                                st.markdown("**Q8.** Suppose you conduct N trials of an experiment and take the average of all your measurements to find a good value. As N increases, your value will get better. Why?")
                                q2_8 = st.radio(
                                    "Select one",
                                    [
                                        "Increasing the number of trials will lower the random error.",
                                        "Increasing the number of trials will lower the systematic error.",
                                        "Increasing the number of trials will lower both random and systematic error."
                                    ],
                                    index=None,
                                    key="pa_q8",
                                )
                                
                                question_id = "pa_q8"
                                
                                if st.button("Check Q8", key="pa_q8_btn"):
                                    is_correct = q2_8 == "Increasing the number of trials will lower the random error."
                                    trial_tracker.record_attempt(question_id, is_correct, q2_8, "precision_accuracy")
                                    
                                    if is_correct:
                                        st.success("Correct! Increasing trials reduces random error, not systematic error.")
                                    else:
                                        st.error("Try again")
                            else:
                                st.info("🔒 Complete Question 7 correctly to unlock Question 8.")
                        else:
                            st.info("🔒 Complete Question 6 correctly to unlock Question 7.")
                    else:
                        st.info("🔒 Complete Question 5 correctly to unlock Question 6.")
                else:
                    st.info("🔒 Complete Question 4 correctly to unlock Question 5.")
            else:
                st.info("🔒 Complete Question 3 correctly to unlock Question 4.")
        else:
            st.info("🔒 Complete Question 2 correctly to unlock Question 3.")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
