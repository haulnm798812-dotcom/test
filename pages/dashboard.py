import pandas as pd
import streamlit as st
import os
st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Dashboard")
st.write("### Show your entries history")
working_file = "skibidi.csv"


def read_file(file_path):
    """
    Args:
        - Input file to check and make into a pd.dataframe

    Return:
        - 'pd.DataFrame' for user to make use if Valid, None for 'problem' to show.
        - None 'df' if Error, 'problem' to show."""
    try:
        df = pd.read_csv(file_path)
        return df, None
    except FileNotFoundError as e:
        return None, str(e)
    except pd.errors.EmptyDataError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)
# Func1 Checked [✓]


def check_digit_col(df):
    """
    Args:
        -pd.DataFrame
    Return:
        -which cols are digit cols/num cols, None(for problems)
        -None( No cols are digit/ Not 'int64' type), Problems(direct problems: ValueError, etc)"""
    try:
        digit_cols = list(df.select_dtypes(
            include=['int64', 'float64']).columns)
        if not digit_cols:
            return None, f"No digit columns found"
        return digit_cols, None
    except Exception as e:
        return None, f"{e}"


def make_stats_metrics(df, num_cols):
    """
    Args: Take columns from the 2nd function to make statistics about data

    Return:
    -statistics if succeeded, None for problem.
    -None stats if failed, problem: problem to fix. """
    try:
        stats = {}
        for col in num_cols:
            stats[col] = {
                f"mean": f"{df[col].mean():.2f}",
                f"sum": f"{df[col].sum():.2f}",
                f"max": f"{df[col].max():.1f}",
                f"min": f"{df[col].min():.1f}"}
        return stats, None
    except ValueError as e:
        return None, f"{e}"


main_df, load_error = read_file(working_file)
if load_error:
    st.error(load_error)
    st.stop()
digit_cols, col_error = check_digit_col(main_df)
statics, metric_error = make_stats_metrics(main_df, digit_cols)
if col_error:
    st.error(f"{col_error}")
    st.stop()
if metric_error:
    st.error(metric_error)
    st.stop()
if "counter" in st.session_state and st.session_state.counter > 0:
    st.success(f"Page 1 submission: {st.session_state.counter} times.")
st.dataframe(main_df, use_container_width=True)
st.write("## 📈 Statistics:")
st.write(f"Tracked {len(main_df)} days!")
cols = st.columns(len(digit_cols))
for idx, col_name in enumerate(digit_cols):
    with cols[idx]:
        st.metric(label=f"Average {col_name}",
                  value=(f"{statics[col_name]['mean']:.1f}"))
with st.expander(f"📊 Detailed Statistics"):
    for col_name in digit_cols:
        st.write(f"**{col_name}**")
        col1, col2, col3, col4 = st.columns(4, border=True)
        with col1:
            st.metric(
                "Average", statics[col_name]['mean'])
        with col2:
            st.metric('Total', statics[col_name]['sum'])
        with col3:
            st.metric('Most', statics[col_name]['max'])
        with col4:
            st.metric('Least', statics[col_name]['min'])
