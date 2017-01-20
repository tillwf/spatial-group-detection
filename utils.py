# encoding: UTF-8

import matplotlib.pyplot as plt
import pandas as pd


def tweak_min(x):
    try:
        return x[0]
    except:
        return 0


def tweak_max(x):
    try:
        return x[-1]
    except:
        return 0


def get_coordinates(user_id, df):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    x = df[df.user_id == user_id].latitude
    y = df[df.user_id == user_id].longitude
    s = df[df.user_id == user_id].accuracy
    c = colors[user_id % (len(colors) - 1)]
    return x, y, s, c


def get_df_at_time(df, time, max_allowed=60):
    # Take the last time of every user
    last_times = df[df.created_at <= time].groupby(["user_id"]).last()
    # Remove user where last time < time - 30
    user_alive = last_times[last_times.created_at >= time - max_allowed].index.tolist()
    last_times = last_times.reset_index()
    return last_times[last_times.user_id.apply(lambda x: x in user_alive)].reset_index()


def get_last_two(x):
    try:
        return x[:2]
    except:
        return get_last(x)


def get_last(x):
    try:
        return x[:1]
    except:
        return x.values[0]
