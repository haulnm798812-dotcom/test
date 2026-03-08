import pandas as pd
import streamlit as st
import os
from datetime import date
import csv
# Rows: Records
# Columns: Attributes
st.set_page_config(page_title="Habit Tracker", page_icon="📊")
working_file = """Place your .csv file here"""
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.title("Daily Habit Tracker")
st.markdown("### Keep track on your Sleep, Work & Habit!")
st.header("Log today's habit")
file_form = st.form("habit tracker")

# Func1


def validate_data(habit, sleep_hrs, work_hrs):
    if habit.strip() == "" or habit.isdigit():
        return False, "Wrong type of Habit"
    if work_hrs + sleep_hrs > 24:
        return False, f"Work hours and Sleep hours must be <= 24"
    if work_hrs < 0 or sleep_hrs < 0:
        return False, "Work & Sleep hours must be > 0"
    return True, ""


# Func2


def check_headers(file_path, expected_headers):
    try:
        df = pd.read_csv(file_path, nrows=0)
        current_headers = list(df.columns)
        return current_headers == expected_headers
    except FileNotFoundError:
        return False
    except pd.errors.EmptyDataError:
        return False
    except Exception:
        return False

# Func3


def save_entry_data(new_data, file_path):
    new_data = new_data.values()
    has_valid_headers = check_headers(file_path, expected_headers)
    try:
        if has_valid_headers:
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
            return True, f"Data saved to {working_file}"
    except PermissionError as e:
        return False, "Permission denied"
    except Exception as e:
        return False, f"Unexpected error: {e}"


with file_form:
    todate = st.date_input("Date", value=date.today())
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
    st.write("---")
    st.session_state.counter += 1
    is_valid, advice = validate_data(
        hab_done, sleep_hrs, work_hrs)

    if not is_valid:
        st.error(f"{advice}")
        st.stop()

    new_entry = {
        "Date": todate,
        "Sleep hours": sleep_hrs,
        "Work hours": work_hrs,
        "Habit": hab_done.capitalize()
    }

    expected_headers = list(new_entry.keys())
    has_valid_headers = check_headers(working_file, expected_headers)
    insert_success, comment = save_entry_data(new_entry, working_file)
    if insert_success:
        st.success(comment)
        st.info(f"Submit count: {st.session_state.counter} times")

    else:
        st.error(comment)
        st.stop()
