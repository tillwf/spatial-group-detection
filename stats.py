import pandas as pd
import numpy as np
from utils import tweak_max, tweak_min


################
#   ACCURACY   #
################

def get_accuracies(df):
    return df.sort_values('created_at').groupby('user_id').accuracy.apply(list)


def get_max_accuracy_distribution(df):
    max_acc = get_accuracies(df).apply(tweak_max)
    max_acc = max_acc.reset_index().groupby("accuracy").size().cumsum()
    max_acc.index = max_acc.index.map(int)
    return pd.DataFrame(max_acc * 100 / max(max_acc))

################
# ELAPSED TIME #
################


def get_ordered_time_list(df):
    time_gb = df.sort_values('created_at').groupby('user_id')
    return time_gb.created_at.apply(list)


def get_elapsed_times(df):
    return get_ordered_time_list(df).apply(lambda a: [t - s for s, t in zip(a, a[1:])])


def get_max_elapsed_time_distribution(df):
    elapsed_times = get_elapsed_times(df)
    elapsed_times = elapsed_times.apply(tweak_max).reset_index().groupby("created_at").size().cumsum()
    return pd.DataFrame(elapsed_times * 100 / max(elapsed_times))


def get_max_elapsed_time_quantiles(df):
    elapsed_times = get_elapsed_times(df)
    return [round(sum(elapsed_times <= i)*100.0/len(elapsed_times)) for i in sorted(list(set(elapsed_times)))]
