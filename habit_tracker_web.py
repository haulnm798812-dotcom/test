import pandas as pd
import streamlit as st
import os
from datetime import date
import csv
# Rows: Records
# Columns: Attributes
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
    need_fix = False

    def need_changes(habit, sleep_hrs, work_hrs):
        try:
            if habit.strip() == "" or habit.isdigit():
                need_fix = True
            elif sleep_hrs + work_hrs >= 24:
                need_fix = True
        except ValueError:
            st.error("Incorrect type of value")
            need_fix = True
        except Exception:
            st.error("Can't run this command")
            need_fix = True
            if need_fix:
                advice = st.error("Change your values")
        return need_fix, advice
    new_entry = {
        "Date": todate,
        "Sleep hours": sleep_hrs,
        "Work hours": work_hrs,
        "Habit": hab_done.capitalize()
    }
    need_changes(new_entry['Habit'],
                 new_entry['Sleep hours'], new_entry['Work hours'])
    expected_headers = list(new_entry.keys())
    """Checks if current headers MATCHES with the expected headers --> return bool"""
    has_valid_headers = False

    def check_headers(file_path, expected_headers):
        try:
            df = pd.read_csv(file_path, nrows=0)
            current_headers = list(df.columns)
            has_valid_headers = (current_headers == expected_headers)
        except FileNotFoundError:
            has_valid_headers = False
        except pd.errors.EmptyDataError:
            has_valid_headers = False
        except Exception:
            has_valid_headers = False
        return has_valid_headers
    write_headers = False

    def save_entry_data(new_data, file_path):
        new_data = new_entry.keys()
        if check_headers(working_file, expected_headers):
            mode = 'a'
            write_headers = False
        else:
            mode = 'w'
            write_headers = True
        with open(file_path, mode, newline='') as f:
            csv_writer = csv.writer(f)
            if write_headers:
                csv_writer.writerow(expected_headers)
            csv_writer.writerow(new_data)
        return new_data, file_path
    inform_data = save_entry_data(new_entry, working_file)
    st.success(f"You successfully tracked Data into {working_file} today!")
    st.info(f"Submit count: {st.session_state.counter} times")
