# encoding: UTF-8

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from utils import get_coordinates
from utils import get_df_at_time


def plot_at_time(df, time, max_allowed=60):
    # Plot scatter
    sub_df = get_df_at_time(df, time, max_allowed)
    sub_df = sub_df.groupby('user_id').last().reset_index()
    for user_id in list(set(sub_df.user_id)):
        x, y, s, c = get_coordinates(user_id, sub_df)
        plt.scatter(x, y, s, color=c, alpha=0.2)


def plot_to_time(df, time):
    # Plot line and last scatter
    # for every user
    pass


def plot_user_to_time(df, time):
    # Plot line and last scatter
    pass


def init_plot(xmin, ymin, xmax, ymax):
    fig = plt.figure()
    plt.plot(xmin, ymin)
    plt.plot(xmax, ymax)
    return fig


def plot_clustering(X, time, labels, core_samples_mask, fig, save=False):
    fig.clf()
    ax = fig.add_subplot()

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=8)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    if save:
        plt.savefig("images/res%08d.png" % time)
    else:
        plt.show()
