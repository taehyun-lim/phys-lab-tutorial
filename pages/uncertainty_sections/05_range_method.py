import streamlit as st
import sys
import os

# Add the lib directory to the path so we can import our trial tracker
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Import our trial tracker
from trial_tracker import trial_tracker

def render_range_method_section():
    # Ensure trial tracker is initialized
    trial_tracker.initialize_session_state()
    
    st.header("Range Method")
    
    # First text block
    st.markdown(
        """
        In many cases, we obtain an estimate of the uncertainty in a measurement, by repeating the experiment a number of times and examining the variation in the data. For example, suppose that the time for a marble to fall a distance of 1.00 m is measured 6 times with a digital stopwatch that reads to the nearest 0.01 s, and the results are 0.44 s, 0.51 s, 0.45 s, 0.52 s, 0.46 s, and 0.49 s. To obtain the **best estimate** for the time we take the **average** or **arithmetic mean** of the six measurements and get 0.48 s. To estimate the **uncertainty**, we might use the **range method** (though perhaps 6 measurements is too many for the range method!). We note that the actual value is unlikely to be more than the highest value, 0.52 s, or less than the lowest value, 0.44s. We write the result as 
        
        t = (0.48 ± 0.04) s

        or

        t = 0.48 ± 0.04 s. [Note that the unit applies to both numbers.]

        This statement is read "time t equals 0.48 plus or minus 0.04 seconds," and it is just a shorthand way of saying that the best estimate is 0.48 s and we believe that the actual value is likely to be between 0.52 and 0.44 s. In this situation, the difference between the highest value and the mean was the same as the difference between the mean and the lowest value. It is also acceptable to take an average to obtain one value for uncertainty when that is not the case.

        The range method for estimating error can be very useful when you have only a few data points and are trying to obtain a rough estimate of your uncertainty. As you take more and more data however, it becomes increasingly likely that you will record numbers that are further and further away from the mean of the data. When using this method, more data often means a greater uncertainty. For this reason, when **6 or more** data points are collected it becomes important to analyze your data using a more mathematical approach, as described in the next section.
        """
    )

    # First question
    #st.subheader("Question 1")
    st.markdown("**Q1.** Should you use the range method in your physics lab if you have 10 trials?")
    q5_1 = st.radio(
        "Select one",
        ["Sure!", "No, use a different method."],
        index=None,
        key="range_q1",
    )
    
    question_id = "range_q1"
    
    if st.button("Check", key="range_q1_btn"):
        is_correct = q5_1 == "No, use a different method."
        trial_tracker.record_attempt(question_id, is_correct, q5_1, "range_method")
        
        if is_correct:
            st.success("Correct! With 10 trials, you should use a different method.")
        else:
            st.error("Try again")

    # Q2 - only visible after Q1 is completed correctly
    if trial_tracker.can_access_question("range_method", "range_q2"):
        # Second text block with detailed example
        st.subheader("Range Method Example")
        st.markdown(
            """
            Here are measurements from 5 trials:
            - 578 g
            - 543 g  
            - 564 g
            - 585 g
            - 503 g

            **Using the range method, what is the best value with uncertainty?**

            **Solution:** The average is the sum, 2773 g, divided by 5 trials, which is: **554.6 g**, and we assume this is the best value.

            There are two equivalent ways to do the next calculation:

            **a)** The high value was 585 g - 554.6 g = 30.4 g above the average. The low value was 503 g, which was 51.6 g below the average. So we take the average of those differences to estimate the one uncertainty we will use: (30.4 + 51.6)/2 = 41 g.

            **or**

            **b)** The highest trial obtained 585 g and the lowest 503 g. So the total range was 585 g - 503 g = 82 g. Since it's plus or minus, we use half of the range, 41 g, as the uncertainty. (This way has less arithmetic and you can prove with algebra that you will get the same result.)

            So the answer is: **554.6 g ± 41 g**

            That means the believable range is 554.6 g - 41 g = **513.6 g to 595.6 g**.

            Since the tens place could vary all the way from 1 to 9, we don't really know ones place, so when we report the measurement in **standard form**, we round to the tens place and write: **550 ± 40 g**, which implies that the believable range is 510 to 590 g.

            (You may note that we measured a trial that was below that range, but we approximate our range to be symmetric about the best value.)
            """
        )

        # Second question
        #st.subheader("Question 2")
        st.markdown("**Q2.** Here are measurements from 5 trials:")
        st.markdown("7.80 V, 8.65 V, 8.40 V, 7.86 V, 7.65 V")
        st.markdown("**Using the range method, which is the average with uncertainty?**")
        q5_2 = st.radio(
            "Select one",
            ["7.9 ± 0.4 V", "8.3 ± 0.6 V", "9.00 ± 0.04 V", "8.1 ± 0.5 V"],
            index=None,
            key="range_q2",
        )
        
        question_id = "range_q2"
        
        if st.button("Check", key="range_q2_btn"):
            is_correct = q5_2 == "8.1 ± 0.5 V"
            trial_tracker.record_attempt(question_id, is_correct, q5_2, "range_method")
            
            if is_correct:
                st.success("Correct! 8.1 ± 0.5 V")
            else:
                st.error("Try again")
    else:
        st.info("🔒 Complete Question 1 correctly to unlock Question 2.")
