'''
Test class for testing WKmens
'''

import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../wkmeans_geo')))
from wkmeans_geo import wkmeans_clustering as wkc
from wkmeans_geo.src import data as test_data
from wkmeans_geo import clusters_from_input as cf


class WKMeansTest(unittest.TestCase):

    def set_up(self):
        self.input_locations = test_data.locations_test
        self.input_locations_with_clusters = test_data.locations_with_clusters_test
        self.number_of_clusters = len(test_data.locations_with_clusters_test.CLUSTER.unique())
        self.minimum_elements_in_a_cluster = test_data.minimum_elements_in_a_cluster
        self.maximum_elements_in_a_cluster = test_data.maximum_elements_in_a_cluster
        self.maximum_volume_in_a_cluster = test_data.maximum_volume_in_a_cluster
        self.maximum_iteration = test_data.maximum_iteration
        self.objective_range = test_data.objective_range
        self.enable_minimum_maximum_elements_in_a_cluster = test_data.enable_minimum_maximum_elements_in_a_cluster

    def test_wkmeans_clustering(self):
        '''
        Test for WKmeans
        :return:
        '''

        self.set_up()

        all_clusters, all_locations_with_clusters = wkc.calculate_clusters(self.input_locations,
                                                                           self.number_of_clusters,
                                                                           self.minimum_elements_in_a_cluster,
                                                                           self.maximum_elements_in_a_cluster,
                                                                           self.maximum_volume_in_a_cluster,
                                                                           self.maximum_iteration,
                                                                           self.enable_minimum_maximum_elements_in_a_cluster,
                                                                           self.objective_range)

        self.assertTrue(len(all_locations_with_clusters) > 0)

    def test_create_initial_clusters_from_given_input(self):
        '''
        To test creating initial clusters from given solution input
        :return:
        '''
        self.set_up()

        initial_solution = cf.create_initial_clusters_from_given_input(self.number_of_clusters + 1,
                                                                       self.input_locations_with_clusters)

        self.assertTrue(len(initial_solution) > 0)

    def test_wkmeans_clustering_with_initial_solution(self):
        '''
        Test to create wkmeans clustering with given initial solution
        :return:
        '''

        self.set_up()

        all_clusters, all_locations_with_clusters = wkc.calculate_clusters(self.input_locations_with_clusters,
                                                                           self.number_of_clusters + 1,
                                                                           self.minimum_elements_in_a_cluster,
                                                                           self.maximum_elements_in_a_cluster,
                                                                           self.maximum_volume_in_a_cluster,
                                                                           self.maximum_iteration,
                                                                           self.enable_minimum_maximum_elements_in_a_cluster,
                                                                           self.objective_range)

        self.assertTrue(len(all_locations_with_clusters) > 0)


if __name__ == '__main__':
    unittest.main()
