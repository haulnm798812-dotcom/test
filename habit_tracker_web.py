import pandas as pd
import streamlit as st
import os
from datetime import date
import csv
st.set_page_config(page_title="Habit Tracker", page_icon=":DDD")
working_file = "skibidi.csv"
st.title("Daily Habit Tracker")
st.markdown("### Keep track on your Sleep, Work & Habit!")
st.header("Log today's habit")
file_form = st.form("habit tracker")
if "counter" not in st.session_state:
    st.session_state.counter = 0
with file_form:
    todate = st.date_input("Date", value=date.today())
    sleep_hrs = st.number_input("Sleep hours",
                                min_value=0,
                                max_value=24,
                                help="Put in today's sleep hours")
    work_hrs = st.number_input("Work hours",
                               min_value=0,
                               max_value=24 - sleep_hrs,
                               help="Put in today's work hours")
    hab_done = st.text_input("Main Habit?",
                             placeholder="for ex: Gym, Reading, Gaming, Cooking, etc",
                             help="What you did in free time")
    submitted = st.form_submit_button("Submit here")

if submitted:
    st.write("---")
    st.session_state.counter += 1
    if hab_done.strip() == "" or hab_done.isdigit():
        st.error("Incorrect Habit")
        st.stop()
    new_entry = {
        "Date": todate,
        "Sleep hours": sleep_hrs,
        "Work hours": work_hrs,
        "Habit": hab_done.capitalize()
    }
    expected_headers = list(new_entry.keys())
    has_valid_headers = False
    try:
        df = pd.read_csv(working_file, nrows=0)
        actual_headers = list(df.columns)
        has_valid_headers = (actual_headers == expected_headers)
    except pd.errors.EmptyDataError:
        has_valid_headers = False
    except Exception as e:
        has_valid_headers = False
    if has_valid_headers:
        mode = 'a'
        write_headers = False
    else:
        mode = 'w'
        write_headers = True
    try:
        with open(working_file, mode, newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            if write_headers:
                csv_writer.writerow(expected_headers)
            csv_writer.writerow(new_entry.values())
        st.success(f"You successfully tracked Data into {working_file} today!")
        st.info(f"Submit count: {st.session_state.counter} times")
    except PermissionError:
        st.error("Can't write to file, Permission denied")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
