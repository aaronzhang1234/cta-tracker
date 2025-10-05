import pandas as pd
import logging

def pandas_fun(df):
    average_stats = {}

    for column in df:
        df[column] = pd.to_datetime(df[column], format="ISO8601")

    average_stats["full_route_stats"] = get_full_route_stats(df)
    #Return dict of key {stopid-stopid} and value {mean_between_station}
    average_stats["time_between_stats"] = get_times_between(df)
    return average_stats

def get_full_route_stats(df):
    full_route_stats = {}
    total_time_series = df[df.columns[-1]] - df[df.columns[0]]

    full_route_stats["avg_total_time"] = timedelta_to_string(total_time_series.mean())

    full_route_stats["slowest_train"] = {}
    full_route_stats["slowest_train"]["total_time"] = timedelta_to_string(total_time_series.max())
    max_time_index = total_time_series.argmax()
    full_route_stats["slowest_train"]["total_time_uuid"] = total_time_series.index[max_time_index]

    full_route_stats["fastest_train"] = {}
    full_route_stats["fastest_train"]["total_time"] = timedelta_to_string(total_time_series.min())
    min_time_index = total_time_series.argmin()
    full_route_stats["fastest_train"]["total_time_uuid"] = total_time_series.index[min_time_index]
    return full_route_stats

def get_times_between(df):
    times_between = pd.DataFrame()
    columns = df.columns.values
    for idx in range(len(columns) - 1):
        times_between_stops = df[columns[idx + 1]] - df[columns[idx]]
        column_name = f"{columns[idx]}-{columns[idx + 1]}"
        times_between[column_name] = times_between_stops
    return get_time_between_dict(times_between)

def get_time_between_dict(times_between):
    route_dict_times = {}
    times_between_columns = times_between.columns.values
    for column_name in times_between_columns:
        between_dict ={}
        times_between_column = times_between[column_name]
        between_dict["max_time"] = timedelta_to_string(times_between_column.max())
        max_time_index = times_between_column.argmax()
        between_dict["max_time_uuid"] = times_between.iloc[max_time_index].name
        between_dict["mean_time"] = timedelta_to_string(times_between_column.mean())
        route_dict_times[column_name] = between_dict
    return route_dict_times


def timedelta_to_string(td):
    total_time = int(td.total_seconds())
    hours, remainder = divmod(total_time, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
