# encoding: UTF-8

from nose.tools import *
import pandas as pd
from clustering import events_from_minus1
from clustering import events_to_minus1
from clustering import normalize
from StringIO import StringIO
import unittest
from unittest import TestCase


class TestStats(TestCase):

    def setUp(self):
        data = """
                user_id    clustering1    clustering2    latitude    longitude    accuracy
                      1             -1             -1           1            1           0
                      2             -1              2           1            1           0
                      3             -1              2           1            1           0
                      4              9              3           1            1           0
                      5              9              3           1            1           0
                      6              4              5           1            1           0
                      7              4              5           1            1           0
                      8              6             -1           1            1           0
                      9              6             -1           1            1           0
                     11             -1              3           1            1           0
                     14             -1              3           1            1           0
                     12              8              8           1            1           0
                     13              8              8           1            1           0
                     15             15             16           1            1           0
                     16             15             16           1            1           0
                     17             15             -1           1            1           0
        """

        self.clustering = pd.read_csv(StringIO(data), sep='\s+').set_index('user_id')
        self.event_new_group = {
            'type': 'creation',
            'date': 2,
            'centroid': (1.0, 1.0),
            'cluster_id': 2,
            'population': set([2, 3]),
            'density': 0.0
        }
        self.event_new_user = {
            'type': 'increase',
            'date': 2,
            'centroid': (1.0, 1.0),
            'people_in': set([11, 14]),
            'previous_cluster_id': 9,
            'cluster_id': 3,
            'population': set([11, 4, 5, 14]),
            'density': 0.0
        }
        self.event_user_left = {
            'type': 'decrease',
            'date': 2,
            'centroid': (1.0, 1.0),
            'people_out': set([17]),
            'previous_cluster_id': 15,
            'cluster_id': 16,
            'population': set([16, 15]),
            'density': 0.0
        }

        self.event_group_deleted = {
            'type': 'deletion',
            'date': 2,
            'people_out': set([8, 9]),
            'cluster_id': 6
        }

    def test_cluster_creation(self):
        data = self.clustering.loc[[1, 2, 3]]
        events = events_from_minus1(data, 2)
        self.assertEqual(events, [self.event_new_group])

    def test_cluster_increase(self):
        data = self.clustering.loc[[1, 4, 5, 11, 14]]
        events = events_from_minus1(data, 2)
        print events
        self.assertEqual(events, [self.event_new_user])

    def test_cluster_creation_and_increase(self):
        data = self.clustering.loc[[1, 2, 3, 4, 5, 11, 14]]
        events = events_from_minus1(data, 2)
        self.assertEqual(events, [
            self.event_new_group,
            self.event_new_user])

    def test_cluster_decrease(self):
        data = self.clustering.loc[[1, 15, 16, 17]]
        events = events_to_minus1(data, 2)
        self.assertEqual(events, [self.event_user_left])

    def test_cluster_deletion(self):
        data = self.clustering.loc[[1, 8, 9]]
        events = events_to_minus1(data, 2)
        self.assertEqual(events, [self.event_group_deleted ])

    def test_cluster_decrease_and_deletion(self):
        data = self.clustering.loc[[1, 8, 9, 15, 16, 17]]
        events = events_to_minus1(data, 2)
        self.assertEqual(events, [
            self.event_group_deleted,
            self.event_user_left])

    def test_full_normalize(self):
        data = self.clustering
        events = normalize(data, 2)
        self.assertEqual(events, [
            self.event_new_group,
            self.event_new_user,
            self.event_group_deleted,
            self.event_user_left,
        ])

    def test_new_cluster_with_new_point(self):
        pass