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
                       objective_range):

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

            logging.info('Optimal solution is found')
            logging.info(solution)

            iteration = iteration + 1
            solution['ITERATION'] = iteration
            objective = round(solution['WEIGHTED_DISTANCE'].sum(), 2)
            solution['OBJECTIVE'] = objective

            stores_with_clusters = stores.copy().merge(solution, how='left', on=['STORE_NAME'])

            logging.info('Stores')
            logging.info(stores_with_clusters)

            logging.info('Clusters')
            logging.info(cluster_locations)

            cluster_locations = calculate_cluster_centers(stores_with_clusters, cluster_locations)
            cluster_locations['ITERATION'] = iteration

            logging.info('Merging results with clusters')
            stores_with_clusters = stores_with_clusters.merge(cluster_locations, how='left', on=['CLUSTER'])
            stores_with_clusters['ITERATION'] = iteration
            stores_with_clusters['SOLUTION'] = 0

            stores_with_clusters = stores_with_clusters[
                ['STORE_NAME', 'LATITUDE', 'LONGITUDE', 'DEMAND',
                 'CLUSTER', 'CLUSTER_NAME', 'CLUSTER_LATITUDE', 'CLUSTER_LONGITUDE',
                 'DISTANCE', 'WEIGHTED_DISTANCE', 'ITERATION',
                 'OBJECTIVE', 'SOLUTION']]

            logging.info('Current objective {}'.format(str(objective)))
            logging.info('Prev objective {}'.format(str(prev_objective)))

            if abs(objective - prev_objective) < objective_range:
                logging.info('Solution found')
                solution_not_found = False
                prev_stores_with_clusters['SOLUTION'] = 1

            elif (prev_objective < objective) and iteration > max_iteration:
                logging.info('Stopping')
                solution_not_found = False
                prev_stores_with_clusters['SOLUTION'] = 1

            else:
                prev_objective = objective
                prev_clusters = cluster_locations
                prev_stores_with_clusters = stores_with_clusters

                all_clusters.append(prev_clusters)
                all_stores_with_clusters.append(prev_stores_with_clusters)

        else:

            raise Exception('Optimal solution to the allocation model does not exist')

    return pd.concat(all_clusters), pd.concat(all_stores_with_clusters)