import pandas as pd
main_df = pd.read_csv('habittracker.csv')


def get_common_habit(df, exclude_values=None):
    import logging
    logger = logging.getLogger(__name__)
    if "Habit" not in df.columns:
        raise ValueError("Missing 'Habit' column")
    if len(df) == 0:
        raise ValueError("Dataframe is empty")
    exclude_values = [exclude_values] or ["Not sure", ""]
    filtered_df = df[~df['Habit'].isin(exclude_values)]
    if len(filtered_df) == 0:
        logger.warning("New Dataframe contains no value")
        return None, 0, 0.0
    habit_counts = filtered_df['Habit'].value_counts()
    fav_habit = habit_counts.idxmax()
    most_time_done = habit_counts.max()
    percentage = (most_time_done/len(df))*100
    logger.info(
        f"Most common habit: {fav_habit} with {most_time_done} times and accounts for: {percentage:.1f}%")
    return fav_habit, most_time_done, percentage


try:
    habit, count, pct = get_common_habit(main_df, exclude_values="Not sure")
    print(
        f"Most common habit: {habit}, appears:{count}, takes up to: {pct:.1f}%")
except ValueError as e:
    print(f"Error: {e}")


def calculate_habit_statistics(df, metric_cols, exclude_zeros=True):
    import logging
    logger = logging.getLogger(__name__)
    missing = [col for col in ["Habit", metric_cols] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    filtered_df = df.copy()
    if exclude_zeros:
        before = len(df)
        filtered_df = filtered_df[filtered_df[metric_cols] > 0]
        removed = before - len(filtered_df)
        logger.info(f"Excluded {removed} rows with zeros {metric_cols}")
    if len(filtered_df) == 0:
        logger.warning(f"No data left after filtering {metric_cols}.")
        return pd.DataFrame()
    stats = filtered_df.groupby("Habit").agg(
        avg=(metric_cols, "mean"),
        total=(metric_cols, "sum"),
        count=(metric_cols, "count"),
        min=(metric_cols, "min"),
        max=(metric_cols, "max"))
    stats = round(stats, 2)
    stats.columns = [f"{metric_cols}_{stat}" for stat in [
        'avg', 'sum', 'count', 'min', 'max']]
    return stats


print(f"Sleep statistics by habit:")
sleep_stats = calculate_habit_statistics(main_df, "Sleep hours")
print(sleep_stats)
print("Work statistics by habit")
work_stats = calculate_habit_statistics(main_df, "Work hours")
print(work_stats)


def find_top_habit_by_metric(stats_df, metric_col, top_n=1):
    import logging
    logger = logging.getLogger(__name__)
    if metric_col not in stats_df.columns:
        raise ValueError(f"Not found {metric_col} in {stats_df.columns}")
    if len(stats_df) == 0:
        logger.warning("Empty Dataframe")
        return pd.DataFrame
    top_bits = stats_df.nlargest(top_n, metric_col)
    logger.info(f"Top {top_n} Habit by {metric_col}:")
    for i, row in top_bits.iterrows():
        logger.info(f"Num{i}: {row[metric_col]:.2f}.")
        return top_bits


print("\n===Top 3 Most productive habit===")
top_work_habit = find_top_habit_by_metric(
    work_stats, "Work hours_avg", top_n=3)
print(top_work_habit)
top_sleep_habit = find_top_habit_by_metric(
    sleep_stats, "Sleep hours_avg", top_n=3)
print(f"{top_sleep_habit[0]}")
