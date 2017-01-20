# encoding: UTF-8

from clustering import get_cluster_algorithm
from clustering import normalize
from loader import get_data
import numpy as np
import pandas as pd
from plot import init_plot
from plot import plot_clustering
from utils import get_df_at_time

PLOT = False

df = get_data(filtered=True)

xmin, xmax = min(df.latitude), max(df.latitude)
ymin, ymax = min(df.longitude), max(df.longitude)

cluster_algorithm = get_cluster_algorithm("db")

if PLOT:
    fig = init_plot(xmin, ymin, xmax, ymax)

clustering = pd.DataFrame()

time_range = range(0, max(df.created_at) / 100)
# time_range = [13311, 13312]

for time in time_range:

    sub_df = get_df_at_time(df, time)
    X = np.array(sub_df[['latitude', 'longitude', 'accuracy']])

    cluster_algorithm.fit(X)
    core_samples_mask = np.zeros_like(cluster_algorithm.labels_, dtype=bool)
    core_samples_mask[cluster_algorithm.core_sample_indices_] = True
    labels = cluster_algorithm.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print '%d - Estimated number of clusters: %d' % (time, n_clusters_)

    sub_df['clustering%s' % time] = labels

    try:
        del sub_df['clustering%s' % (time - 60)]
    except:
        pass

    clustering = pd.concat([clustering, sub_df.set_index('user_id')[['clustering%s' % time, 'latitude', 'longitude', 'accuracy']]], axis=1)
    # filtered_labels = filter_clustering(clustering)

    if time != time_range[0]:
        normalize(clustering, time)
        del clustering['latitude']
        del clustering['longitude']
        del clustering['accuracy']

    if PLOT:
        plot_clustering(X, time, labels, core_samples_mask, fig, save=True)

