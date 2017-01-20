# encoding: UTF-8

from metrics import haversine_acc
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import pairwise_distances


def get_cluster_algorithm(algorithm):
    if algorithm == "db":
        """
        optimal eps values :
                "haversine": 0.05
                "haversine_acc": 0.05
        """
        return DBSCAN(
                    eps=0.05,
                    min_samples=2,
                    algorithm='brute',
                    metric=lambda X, Y: haversine_acc(X, Y)
                )


def normalize(clustering, time):
    from_minus1 = events_from_minus1(clustering, time)
    to_minus1 = events_to_minus1(clustering, time)

    return from_minus1 + to_minus1


def emit_event(clustering, time, previous_users, current_users, previous_cluster_id, current_cluster_id):
    event = {"date": time}

    if len(current_users) == 0:
        # Cluster deletion
        event.update({
            "type": "deletion",
            "cluster_id": previous_cluster_id,
            "people_out": previous_users
        })
    else:
        mean_lat = clustering.loc[list(current_users)].latitude
        mean_long = clustering.loc[list(current_users)].longitude
        event.update({
            "centroid": (np.mean(mean_lat), np.mean(mean_long)),
            "population": current_users,
            "cluster_id": current_cluster_id,
            "density": mean_distance_intra_centroid(clustering, current_users)
        })

        if not len(previous_users):
            # Creation
            event.update({"type": "creation"})
        elif len(previous_users) > len(current_users):
            event.update({
                "type": "decrease",
                "previous_cluster_id": previous_cluster_id,
                "people_out": previous_users.difference(current_users)
            })

        elif len(previous_users) < len(current_users):
            event.update({
                "type": "increase",
                "previous_cluster_id": previous_cluster_id,
                "people_in": current_users.difference(previous_users)
            })
        else:
            print "Error !"

    print event
    return event


def mean_distance_intra_centroid(clustering, users):
    X = np.array(clustering.loc[users, ['latitude', 'longitude', 'accuracy']])
    distances = pairwise_distances(X, metric=lambda X, Y: haversine_acc(X, Y))
    return np.mean(distances)


def events_from_minus1(clustering, time):

    prev_clus = clustering['clustering%s' % (time - 1)]
    current_clus = clustering['clustering%s' % time]

    # Handle previous non clustered points
    minus1 = pd.concat([prev_clus[prev_clus == -1], current_clus], axis=1, join='inner')
    new_groups = minus1[minus1['clustering%s' % time] != minus1['clustering%s' % (time - 1)]]

    events = []

    for cluster_id in set(new_groups['clustering%s' % time]):

        current_lines = clustering[clustering['clustering%s' % time] == cluster_id]
        current_users = set(current_lines.index.tolist())

        previous_lines = current_lines[current_lines['clustering%s' % (time - 1)] != -1].dropna()
        previous_users = set(previous_lines.index)

        previous_cluster_id = None
        if len(set(previous_lines.index)):
            # New users
            previous_cluster_id = list(set(current_lines['clustering%s' % (time - 1)].values) - set([-1]))[0]

        event = emit_event(clustering, time, previous_users, current_users, previous_cluster_id, cluster_id)
        events.append(event)

    return events


def events_to_minus1(clustering, time):

    prev_clus = clustering['clustering%s' % (time - 1)].dropna()
    current_clus = clustering['clustering%s' % time]

    # Handle previous non clustered points
    minus1 = pd.concat([prev_clus[current_clus == -1], current_clus], axis=1, join='inner')
    new_groups = minus1[minus1['clustering%s' % time] != minus1['clustering%s' % (time - 1)]]

    events = []

    for cluster_id in set(new_groups['clustering%s' % (time - 1)]):

        previous_lines = clustering[clustering['clustering%s' % (time - 1)] == cluster_id]
        previous_users = set(previous_lines.index.tolist())

        current_lines = new_groups[new_groups['clustering%s' % (time - 1)] == cluster_id]
        current_users = set(current_lines.index.tolist())

        kept_users = previous_users.difference(current_users)

        new_cluster_id = None

        if len(kept_users):
            # Cluster is alive
            users_in_cluster = current_clus.reset_index().groupby('clustering%s' % time).user_id.apply(set)
            new_cluster_id = users_in_cluster[users_in_cluster == kept_users].index.tolist()[0]

        event = emit_event(clustering, time, previous_users, kept_users, cluster_id, new_cluster_id)
        events.append(event)

    return events
