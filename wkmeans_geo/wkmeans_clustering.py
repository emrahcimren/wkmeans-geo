import pandas as pd
from src import clusters as cl
from src import initiation as init
from src import optimization_model as ort

input_locations = pd.read_csv('./test/data.csv')
#input_locations = pd.read_csv('./test/data_with_clusters.csv')
number_of_clusters = 100
minimum_elements_in_a_cluster = 0
maximum_elements_in_a_cluster = 50
maximum_iteration=100
objective_range=0.001
use_given_clusters=False
enable_minimum_maximum_elements_in_a_cluster=True


def calculate_clusters(input_locations,
                       number_of_clusters,
                       minimum_elements_in_a_cluster,
                       maximum_elements_in_a_cluster,
                       maximum_iteration,
                       objective_range,
                       previous_objective=None):

    iteration = 0
    all_clusters = []
    all_stores_with_clusters = []

    if 'CLUSTER' not in input_locations.columns:
        locations_with_clusters = init.randomly_assign_clusters(number_of_clusters, input_locations)
    else:
        locations_with_clusters = input_locations.copy()
        input_locations.drop(['CLUSTER'], 1, inplace=True)

    prev_objective, prev_clusters, prev_locations_with_clusters = \
        init.initiate_algorithm(iteration, locations_with_clusters)

    if previous_objective is not None:
        prev_objective = previous_objective

    all_clusters.append(prev_clusters)
    all_stores_with_clusters.append(prev_locations_with_clusters)

    solution_not_found = True
    while solution_not_found:
        print('Running iteration {}'.format(str(iteration)))

        location_cluster_distance_matrix = cl.calculate_distance_matrix(input_locations.copy(), prev_clusters)

        location_list, cluster_list, distance = ort.prepare_model_inputs(location_cluster_distance_matrix)
        solution = ort.formulate_and_solve_ortools_model(location_list, cluster_list, distance,
                                                         minimum_elements_in_a_cluster,
                                                         maximum_elements_in_a_cluster,
                                                         enable_minimum_maximum_elements_in_a_cluster)

        if len(solution) > 0:

            print('Optimal solution is found')
            print(solution)

            iteration = iteration + 1
            solution['ITERATION'] = iteration
            objective = round(solution['WEIGHTED_DISTANCE'].sum(), 2)
            solution['OBJECTIVE'] = objective

            locations_with_clusters = input_locations.copy().merge(solution, how='left', on=['LOCATION_NAME'])

            print('Stores')
            print(locations_with_clusters)

            print('Clusters')
            cluster_locations = cl.calculate_cluster_centers(locations_with_clusters)
            cluster_locations['ITERATION'] = iteration

            print('Merging results with clusters')
            locations_with_clusters = locations_with_clusters.merge(cluster_locations, how='left', on=['CLUSTER'])
            locations_with_clusters['ITERATION'] = iteration
            locations_with_clusters['SOLUTION'] = 0

            locations_with_clusters = locations_with_clusters[
                ['LOCATION_NAME', 'LATITUDE', 'LONGITUDE', 'WEIGHT',
                 'CLUSTER', 'CLUSTER_LATITUDE', 'CLUSTER_LONGITUDE',
                 'DISTANCE', 'WEIGHTED_DISTANCE', 'ITERATION',
                 'OBJECTIVE', 'SOLUTION']]

            print('Current objective {}'.format(str(objective)))
            print('Prev objective {}'.format(str(prev_objective)))

            if abs(objective - prev_objective) < objective_range:
                print('Solution found')
                solution_not_found = False
                prev_locations_with_clusters['SOLUTION'] = 1

            elif (prev_objective < objective) and iteration > maximum_iteration:
                print('Stopping')
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
