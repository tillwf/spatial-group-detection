# encoding : UTF-8

import pandas as pd
from stats import get_elapsed_times
from utils import tweak_max

MAX_TIME_DELTA_ALLOWED = 60
MIN_ACCURACY_ALLOWED = 50


def get_data(filtered=False):
    df = pd.read_csv('data/dataset_groups_test.csv', header=0)
    if filtered:
        initial_length = len(df)
        df = filter_on_max_accuracy(df, MIN_ACCURACY_ALLOWED)
        df = filter_on_max_elapsed_time(df, MAX_TIME_DELTA_ALLOWED)

        percentage_kept = round(len(df) * 100.0 / initial_length, 2)

        print "{0:.0f}% of the db has been kept".format(percentage_kept)

    df = df.sort_values("created_at")
    return df.groupby(['user_id', 'created_at']).last().reset_index()


def filter_on_max_accuracy(df, max_allowed=MIN_ACCURACY_ALLOWED):
    return df[df.accuracy <= max_allowed]


def filter_on_max_elapsed_time(df, max_allowed=MAX_TIME_DELTA_ALLOWED):
    # Very drastic (ex: user_id=1)
    max_elapsed_time = get_elapsed_times(df).apply(tweak_max)
    filtered_user_ids = max_elapsed_time[max_elapsed_time <= max_allowed].index
    return df[df.user_id.apply(lambda x: x in filtered_user_ids)]
