import pandas as pd


def worked_for_7_days(group):
    """
    Check if worked for 7 consecutive days.
    """
    sorted_dates = group['Time'].sort_values()
    return any((sorted_dates.iloc[i + 1] - sorted_dates.iloc[i]).days == 1 for i in range(len(sorted_dates) - 1))


def less_than_10_hours_between_shifts(group):
    """
    Check if less than 10 hours between shifts.
    """
    sorted_times = group['Time'].sort_values()
    time_diff = sorted_times.diff().fillna(pd.Timedelta(seconds=0))
    return any((1 < time_diff.iloc[i].seconds / 3600 < 10) for i in range(1, len(time_diff)))


def more_than_14_hours_in_a_shift(group):
    """
    Check if worked for more than 14 hours in a shift.
    """
    shift_duration = (group['Time Out'] - group['Time']).dt.total_seconds() / 3600
    return any(shift_duration > 14)


def convert_to_timedelta(value):
    """
    Convert time value to timedelta.
    """
    try:
        return pd.to_timedelta(value)
    except ValueError:
        try:
            return pd.to_timedelta(value + ':00')
        except ValueError:
            print(f"Unexpected value in 'Timecard Hours (as Time)': {value}")
            return pd.NaT
