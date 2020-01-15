from wkmeans_geo import wkmeans_clustering as wkc
import test_data

input_locations = test_data.locations_test
input_locations_with_clusters = test_data.locations_with_clusters_test
number_of_clusters = test_data.number_of_clusters
minimum_elements_in_a_cluster = test_data.minimum_elements_in_a_cluster
maximum_elements_in_a_cluster = test_data.maximum_elements_in_a_cluster
maximum_iteration = test_data.maximum_iteration
objective_range = 0.001
enable_minimum_maximum_elements_in_a_cluster=True

all_clusters, all_locations_with_clusters = wkc.calculate_clusters(input_locations,
                                                                   number_of_clusters,
                                                                   minimum_elements_in_a_cluster,
                                                                   maximum_elements_in_a_cluster,
                                                                   maximum_iteration,
                                                                   enable_minimum_maximum_elements_in_a_cluster,
                                                                   objective_range)
