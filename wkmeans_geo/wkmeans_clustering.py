import os
import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/src')))
#sys.path.append('src')

import pandas as pd
from wkmeans_geo.src import clusters as cl
from wkmeans_geo.src import initiation as init
from wkmeans_geo.src import optimization_model as ort


def calculate_clusters(input_locations,
                       number_of_clusters,
                       minimum_elements_in_a_cluster,
                       maximum_elements_in_a_cluster,
                       maximum_volume_in_a_cluster,
                       maximum_iteration,
                       objective_range,
                       enable_minimum_maximum_elements_in_a_cluster):
    '''
    Run WKmens clustering
    :param input_locations:
    :param number_of_clusters:
    :param minimum_elements_in_a_cluster:
    :param maximum_elements_in_a_cluster:
    :param maximum_volume_in_a_cluster:
    :param maximum_iteration:
    :param objective_range:
    :param enable_minimum_maximum_elements_in_a_cluster:
    :param previous_objective:
    :return:
    '''

    iteration = 0

    print('Running for iteration {}'.format(str(iteration)))

    all_clusters = []
    all_stores_with_clusters = []

    if 'CLUSTER' not in input_locations.columns:
        print('Randomly assigning clusters')
        locations_with_clusters = init.randomly_assign_clusters(number_of_clusters, input_locations)
    else:
        locations_with_clusters = input_locations.copy()
        input_locations.drop(['CLUSTER'], 1, inplace=True)

    prev_objective, prev_clusters, prev_locations_with_clusters = \
        init.initiate_algorithm(iteration, locations_with_clusters)

    all_clusters.append(prev_clusters)
    all_stores_with_clusters.append(prev_locations_with_clusters)

    solution_not_found = True
    while solution_not_found:

        print('Running iteration {}'.format(str(iteration)))

        print('Calculating distance matrix')
        location_cluster_distance_matrix = cl.calculate_distance_matrix(input_locations.copy(), prev_clusters)

        print('Preparing model inputs')
        location_list, cluster_list, distance, volume = ort.prepare_model_inputs(location_cluster_distance_matrix)

        print('Running the model')
        solution = ort.formulate_and_solve_ortools_model(location_list,
                                                         cluster_list,
                                                         distance,
                                                         volume,
                                                         minimum_elements_in_a_cluster,
                                                         maximum_elements_in_a_cluster,
                                                         maximum_volume_in_a_cluster,
                                                         enable_minimum_maximum_elements_in_a_cluster)

        if len(solution) > 0:

            iteration = iteration + 1
            solution['ITERATION'] = iteration
            objective = round(solution['WEIGHTED_DISTANCE'].sum(), 2)
            solution['OBJECTIVE'] = objective

            locations_with_clusters = input_locations.copy().merge(solution, how='left', on=['LOCATION_NAME'])

            #Clusters
            cluster_locations = cl.calculate_cluster_centers(locations_with_clusters)
            cluster_locations['ITERATION'] = iteration

            #Merging results with clusters
            locations_with_clusters = locations_with_clusters.merge(cluster_locations, how='left', on=['CLUSTER'])
            locations_with_clusters['ITERATION'] = iteration
            locations_with_clusters['SOLUTION'] = 0

            locations_with_clusters = locations_with_clusters[
                ['LOCATION_NAME', 'LATITUDE', 'LONGITUDE', 'WEIGHT', 'VOLUME',
                 'CLUSTER', 'CLUSTER_LATITUDE', 'CLUSTER_LONGITUDE',
                 'DISTANCE', 'WEIGHTED_DISTANCE', 'ITERATION',
                 'OBJECTIVE', 'SOLUTION']]

            print('Current objective {}'.format(str(objective)))
            print('Previous objective {}'.format(str(prev_objective)))

            if abs(objective - prev_objective) < objective_range:
                print('Solution found')
                solution_not_found = False
                prev_locations_with_clusters['SOLUTION'] = 1

            elif (prev_objective < objective) and iteration > maximum_iteration:
                print('Stopping since maximum iterations is reached')
                solution_not_found = False
                prev_locations_with_clusters['SOLUTION'] = 1

            else:
                prev_objective = objective
                prev_clusters = cluster_locations
                prev_locations_with_clusters = locations_with_clusters

                all_clusters.append(prev_clusters)
                all_stores_with_clusters.append(prev_locations_with_clusters)

        else:

            raise Exception('Optimal solution to the allocation model does not exist')

    all_clusters = pd.concat(all_clusters)
    all_clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters
    all_stores_with_clusters = pd.concat(all_stores_with_clusters)
    all_stores_with_clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters

    return all_clusters, all_stores_with_clusters
