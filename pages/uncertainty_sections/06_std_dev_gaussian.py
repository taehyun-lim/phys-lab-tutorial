import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_std_dev_gaussian_section():
    # Ensure trial tracker is initialized
    trial_tracker.initialize_session_state()
    
    st.header("Standard Deviation and the Gaussian Distribution")
    
    # First text block
    st.markdown(
        """
        When a measurement is repeated a large number of times, instead of considering the largest and smallest values to quantify the uncertainty, we calculate the **standard deviation** (sigma σ). The standard deviation describes the **spread of the data** from the mean. If all the measurements are the same, then σ = 0. The more variation in the data, the larger σ will be.

        The definition is a square root (sqrt) average of the square deviations from the mean. The formula is below but in your physics lab you may always use a calculator function. For example, in Excel, the function is =STDEV(A1\:A10).

        (If you know more about this, note that we use the sample standard deviation, not the population standard deviation, because in physics it is always possible to take additional data by conducting another trial.)
        """
    )

    # Standard deviation formula
    st.subheader("Standard Deviation Formula")
    st.image(
        "uncertainty_google_forms/Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files/unnamed(4).png",
        #caption="Hitting a target requires both high precision and high accuracy",
        width=500
    )

    # Gaussian distribution explanation
    st.subheader("The Gaussian Distribution / Bell Curve / Normal Distribution and Standard Deviation σ")
    st.image(
        "uncertainty_google_forms/Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files/unnamed(5).png",
        #caption="(image credit: https://www.simplypsychology.org/normal-distribution.html)",
        width=500
    )
    
    # Clickable link below the image
    st.markdown(
        "image credit: [https://www.simplypsychology.org/normal-distribution.html](https://www.simplypsychology.org/normal-distribution.html)",
        unsafe_allow_html=True
    )

    # Standard deviation as uncertainty
    st.subheader("Standard deviation as uncertainty that shows the spread between trials")
    st.markdown(
        """
        Recall the timing measurements example: 0.44 s, 0.51 s, 0.45 s, 0.52 s, 0.46 s, and 0.49 s

        For the six timing measurements discussed above, the standard deviation is σ = 0.0331s. Notice that this value is smaller than the uncertainty value obtained using the previous method (0.4 s). In general, **standard deviation is a more precise method of estimating the spread in a data set and is less susceptible to extremes within the data** compared to the range method. As you add more and more data to your data set, ideally the standard deviation will not change.

        Using the standard deviation as the uncertainty gives us a 68% confidence interval for any single trial:
        0.48 ± 0.03 s,
        meaning that any single trial is 68% likely to land in the range of 0.45 to 0.51 seconds and 32% likely to be outside that range.

        [Note for students of statistics: In other classes, like Psych Stats, you may use a confidence interval of 95%, which is called an alpha of 5%. In Physics we do not privilege the null hypothesis that two numbers are the same, so we choose a smaller confidence interval. That means: in Psychology research, it's important to assume that two quantities are equal -- the null hypothesis -- unless there is <5% chance that they are not equal. Rejecting the null hypothesis in Psychology requires a greater burden. In Physics lab, we usually assume that two quantities are equal if there is <32% chance that they are different: our alpha is usually around 32%.]

        When most measurements are repeated a very large number of times we expect that half of the data will be ≥ the average and half will be ≤ the average. We also expect that most of the results will be fairly close to the average and a smaller number of results will be further from the average (see Fig. 1). The particular distribution of data shown in Fig. 1 is called a **_normal_** or **_Gaussian distribution_**. If the data is indeed distributed normally (as we shall usually assume), then it can be shown that 68% (about 2/3) of the measurements fall within ± σ of the average, about 95% of the data fall within ± 2 σ of the average, and more than 99% of the data fall within ± 3 σ of the average.
        """
    )

    st.subheader("Standard error as an uncertainty that shows the spread between averages")
    st.markdown(
        """
        Often, we repeat an experiment a number of times and then find the average. Intuitively we know that the more times we repeat the experiment, the more confidence we have in the average value obtained. In other words, the more times we repeat the experiment, the smaller the uncertainty in the average. However, repeating the experiment more times does not significantly affect the standard deviation, because the variation of the data is determined by the precision of the measurement, and repeating a measurement does not change its precision.

        To quantify the uncertainty of the average that comes with an increased number of measurements, scientists use the **_standard error_** (SE). It is defined by the equation
        SE =  σ /√N,
        where σ is the standard deviation and N is the number of times the measurement is repeated.

        While the standard deviation indicates the amount of variation of the data about the mean, the standard error indicates how much the average of N measurements would be expected to vary if the entire N measurements were repeated again.

        In the timing example used previously, the standard error is (0.0331 s)/√6 = 0.0135 s ≈ 0.01 s.
        0.48 ± 0.01 s.
        This standard error indicates that if 6 more time measurements are made, it is quite likely that the **average** of the 6 new measurements will be within 0.01 s of the previous **average** of 0.48 s. The standard deviation of the 6 new measurements would still be expected to be about 0.03s.

        When reporting the result of a measurement, it is important to justify your uncertainty. Always specify how you obtained your uncertainty and report if it is an estimate, from the range method, the standard deviation, or the standard error.
        """
    )
    # Five questions
    #st.subheader("Questions")
    
    # Q1: Standard error calculation
    st.markdown("**Q1.** On Monday, a pair of students measure the voltage of a circuit five times, and they find that the average is 1.5452 V and the standard deviation is 0.0533 V. What is the standard error? (Round your answer to 1 significant figure.)")
    q6_1 = st.radio(
        "Select one",
        ["0.01 V", "0.02 V", "0.03 V", "0.04 V", "0.05 V", "0.06 V", "0.1 V"],
        index=None,
        key="sd_q1",
    )
    
    question_id = "sd_q1"
    
    if st.button("Check", key="sd_q1_btn"):
        is_correct = q6_1 == "0.02 V"
        trial_tracker.record_attempt(question_id, is_correct, q6_1, "std_dev_gaussian")
        
        if is_correct:
            st.success("Correct! 0.02 V")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("std_dev_gaussian", "sd_q2"):
        # Q2: Which uncertainty for next measurement
        st.markdown("**Q2.** Which uncertainty should the students use to estimate the range of values they might get on their next voltage measurement?")
        q6_2 = st.radio(
            "Select one",
            ["standard deviation", "standard error"],
            index=None,
            key="sd_q2",
        )
        
        question_id = "sd_q2"
        
        if st.button("Check", key="sd_q2_btn"):
            is_correct = q6_2 == "standard deviation"
            trial_tracker.record_attempt(question_id, is_correct, q6_2, "std_dev_gaussian")
            
            if is_correct:
                st.success("Correct! standard deviation")
            else:
                st.error("Try again")

        # Q3 - only visible after Q2 is completed correctly
        if trial_tracker.can_access_question("std_dev_gaussian", "sd_q3"):
            # Q3: Which uncertainty for Tuesday lab students' average
            st.markdown("**Q3.** Which uncertainty should the Monday students use to estimate the range of values they expect for the AVERAGE the Tuesday lab students will get when they conduct voltage measurements of the **same circuit**?")
            q6_3 = st.radio(
                "Select one",
                ["standard deviation", "standard error"],
                index=None,
                key="sd_q3",
            )
            
            question_id = "sd_q3"
            
            if st.button("Check", key="sd_q3_btn"):
                is_correct = q6_3 == "standard error"
                trial_tracker.record_attempt(question_id, is_correct, q6_3, "std_dev_gaussian")
                
                if is_correct:
                    st.success("Correct! standard error")
                else:
                    st.error("Try again")

            # Q4 - only visible after Q3 is completed correctly
            if trial_tracker.can_access_question("std_dev_gaussian", "sd_q4"):
                # Q4: Does standard deviation measure random or systematic error
                st.markdown("**Q4.** Does standard deviation measure random error or systematic error?")
                q6_4 = st.radio(
                    "Select one",
                    ["random error", "systematic error", "both random and systematic error", "neither"],
                    index=None,
                    key="sd_q4",
                )
                
                question_id = "sd_q4"
                
                if st.button("Check", key="sd_q4_btn"):
                    is_correct = q6_4 == "random error"
                    trial_tracker.record_attempt(question_id, is_correct, q6_4, "std_dev_gaussian")
                    
                    if is_correct:
                        st.success("Correct! random error")
                    else:
                        st.error("Try again")

                # Q5 - only visible after Q4 is completed correctly
                if trial_tracker.can_access_question("std_dev_gaussian", "sd_q5"):
                    # Q5: Why does standard error decrease with more measurements
                    st.markdown("**Q5.** Does standard error measure random error or systematic error?")
                    q6_5 = st.radio(
                        "Select one",
                        [
                            "random error",
                            "systematic error",
                            "both random and systematic error",
                            "neither"
                        ],
                        index=None,
                        key="sd_q5",
                    )
                    
                    question_id = "sd_q5"
                    
                    if st.button("Check", key="sd_q5_btn"):
                        is_correct = q6_5 == "random error"
                        trial_tracker.record_attempt(question_id, is_correct, q6_5, "std_dev_gaussian")
                        
                        if is_correct:
                            st.success("Correct! random error")
                        else:
                            st.error("Try again")
                else:
                    st.info("🔒 Complete Question 4 correctly to unlock Question 5.")
            else:
                st.info("🔒 Complete Question 3 correctly to unlock Question 4.")
        else:
            st.info("🔒 Complete Question 2 correctly to unlock Question 3.")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
