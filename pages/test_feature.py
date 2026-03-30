import streamlit as st
import pandas as pd
import os
from datetime import datetime
st.title("📊 Dashboard")
st.write("### Show your entries history")
working_file = "skibidi.csv"

st.set_page_config(page_title="Habit Tracker", page_icon="📊")
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.title("Daily Habit Tracker")
st.markdown("### Keep track on your Sleep, Work & Habit!")
st.header("Log today's habit")
file_form = st.form("habit tracker")


#Func1: Check data values
def validate_data(habit, sleep_hrs, work_hrs):
    if float(habit.strip()):
        return False, "Wrong type of Habit"
    if work_hrs + sleep_hrs > 24:
        return False, f"Work hours and Sleep hours must be <= 24"
    if work_hrs < 0 or sleep_hrs < 0:
        return False, "Work & Sleep hours must be > 0"
    return True, None




with file_form:
    todate = st.date_input("Date", value=datetime.today())
    sleep_hrs = st.number_input("Sleep hours",
                                min_value=0,
                                max_value=24,
                                help="Put in today's sleep hours")
    work_hrs = st.number_input("Work hours",
                               min_value=0,
                               max_value=24,
                               help="Put in today's work hours")
    hab_done = st.text_input("Main Habit?",
                             placeholder="for ex: Gym, Reading, Gaming, Cooking, etc",
                             help="What you did in free time")
    submitted = st.form_submit_button("Submit here")
if submitted:
    success, comment = validate_data(hab_done, sleep_hrs, work_hrs)
    st.info(comment)