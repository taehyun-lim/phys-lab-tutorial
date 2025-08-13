import streamlit as st

def render_standard_form_section():
    st.header("Standard Form")
    
    st.markdown(
        """
        In order to save time and effort, we will often make rather crude estimates of the uncertainty in a measurement. To indicate that our uncertainties are only estimates, we normally report the uncertainty to only 1 significant figure. (Even in very careful scientific work, uncertainties are almost never reported with more than 2 significant figures). This makes it easy for the reader to interpret the measurement as a range of believable values and is an important part of of clear communication of scientific research.

        When reporting the average of the measurements we should also be aware of how many significant figures we report. In the timing example above example, the calculated average of the 6 measurements is 0.47833333 s. However, we report the average to the same precision as the uncertainty. Thus, with an uncertainty of 0.01 s, the result, reported in **standard form** is

        t = (0.48 ± 0.01) s.

        or

        t = 0.48 ± 0.01 s.

        Notice that the last digit reported, the 8 in this example, is the digit that is uncertain. Both are reported to the tenths place.

        **Note**: Don't bother counting the number of significant figures for the value. This is a more sophisticated method of error analysis than significant figures.

        **Note**: Do not round too soon! Rounding is part of communication, not part of calculations. Keep the digits in your calculator.

        **Note** that standard form is not the same thing as scientific notation, but you can combine them if you want. If the result and uncertainty are written in scientific notation, then the uncertainty should be written with the same exponent as the result. For example, in the above case we would write the result as

        t = (4.8 ± 0.1) × 10^-1 s.    Both scientific notation and standard form.

        Standard form does require the formats to match, so this is NOT standard form:

        t = (4.8 × 10^-1) ± 0.1 s     [NOT standard form]

        because it makes it more difficult for the reader to interpret the measurement as a range of believable values.

        Usually we only use scientific notation when it makes the result more readable, and in scientific publications, metric prefixes are more common that scientific notation.

        **Summary instructions**:
        - Round the uncertainty to one significant figure.
        - Round the value to the same decimal place as the uncertainty. Match the format.
        - Write the value and uncertainty together as:    value  ± uncertainty unit
        """
    )

    st.subheader("Questions")
    
    # Q1: Significant figures question
    st.markdown("**Q1.** All but one of these has 1 significant figure. Which one is the odd one out with 2 significant figures?")
    q7_1 = st.radio(
        "Select one",
        ["2.1 m", "3000000 m", "600 m", "2 m", "0.8 m", "0.000006 m", "They all have 1 significant figure"],
        index=None,
        key="sf_q1",
    )
    if st.button("Check Q1", key="sf_q1_btn"):
        st.success("Correct! 2.1 m") if q7_1 == "2.1 m" else st.error("Try again")

    # Q2: Which is written in standard form
    st.markdown("**Q2.** Which one of these is written in standard form?")
    q7_2 = st.radio(
        "Select one",
        ["2362 ± 0.5 km", "2362.6 ± 4.6 km", "2362 ± 50 km", "2362.6 ± 5 km", "2362 ± 5 km", "2000 ± 0.5 km", "(2 × 10^3) ± 5 km", "(2.362 × 10^3) ± 5 km", "(2.362 × 10^6) ± 5000 m", "None of them"],
        index=None,
        key="sf_q2",
    )
    if st.button("Check Q2", key="sf_q2_btn"):
        st.success("Correct! 2362 ± 5 km") if q7_2 == "2362 ± 5 km" else st.error("Try again")

    # Q3: Write in standard form (large number)
    st.markdown("**Q3.** Write this in standard form: 284629 ± 342 V (you may copy-paste the ± character or use +/-)")
    q7_3 = st.text_input("Your answer", key="sf_q3")
    if st.button("Check Q3", key="sf_q3_btn"):
        # Normalize the input to handle various formats
        user_input = (q7_3 or "").strip().replace("+/-", "±").replace("+/-", "±")
        correct_answers = ["284629 ± 342 V", "284629±342 V", "284629 ±342 V", "284629± 342 V"]
        if any(user_input == ans for ans in correct_answers):
            st.success("Correct! 284629 ± 342 V")
        else:
            st.error("Try again. Round the uncertainty to 1 significant figure and the value to match.")

    # Q4: Write in standard form (small number)
    st.markdown("**Q4.** Write this in standard form: .048294 ± 0.0003 V")
    q7_4 = st.text_input("Your answer", key="sf_q4")
    if st.button("Check Q4", key="sf_q4_btn"):
        # Normalize the input to handle various formats
        user_input = (q7_4 or "").strip().replace("+/-", "±").replace("+/-", "±")
        correct_answers = ["0.048294 ± 0.0003 V", "0.048294±0.0003 V", "0.048294 ±0.0003 V", "0.048294± 0.0003 V"]
        if any(user_input == ans for ans in correct_answers):
            st.success("Correct! 0.048294 ± 0.0003 V")
        else:
            st.error("Try again. Round the uncertainty to 1 significant figure and the value to match.")
