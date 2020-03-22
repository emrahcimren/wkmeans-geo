'''
Formulate and solve depot-store allocation model
'''

import pandas as pd
import collections
from ortools.linear_solver import pywraplp


def prepare_model_inputs(location_cluster_distance_matrix):
    '''
    Run the optimization model
    :param location_cluster_distance_matrix:
    :return:
    '''

    DistanceInputs = collections.namedtuple('DistanceInputs', ['DISTANCE', 'WEIGHTED_DISTANCE'])
    distance = {}
    for row in location_cluster_distance_matrix.itertuples():
        distance[row.CLUSTER, row.LOCATION_NAME] = (DistanceInputs(
            DISTANCE=row.DISTANCE,
            WEIGHTED_DISTANCE=row.WEIGHTED_DISTANCE))

    location_list = []
    cluster_list = []
    for cluster, store in distance.keys():
        cluster_list.append(cluster)
        location_list.append(store)
    location_list = list(dict.fromkeys(location_list))
    cluster_list = list(dict.fromkeys(cluster_list))

    volume_input = location_cluster_distance_matrix[['LOCATION_NAME', 'VOLUME']].drop_duplicates()
    volume = {}
    for _, row in volume_input.iterrows():
        volume[row.LOCATION_NAME] = row.VOLUME

    return location_list, cluster_list, distance, volume


def formulate_and_solve_ortools_model(store_list,
                                      cluster_list,
                                      distance,
                                      volume,
                                      minimum_elements_in_a_cluster,
                                      maximum_elements_in_a_cluster,
                                      maximum_volume_in_a_cluster,
                                      enable_minimum_maximum_elements_in_a_cluster):
    '''
    Formulate the model
    :param store_list:
    :param cluster_list:
    :param distance:
    :param volume:
    :param minimum_elements_in_a_cluster:
    :param maximum_elements_in_a_cluster:
    :param maximum_volume_in_a_cluster:
    :param enable_minimum_maximum_elements_in_a_cluster:
    :return:
    '''

    # formulate model
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # create variables #
    y = {}
    for cluster, store in distance.keys():
        y[cluster, store] = solver.BoolVar('y[cluster = {}, {}]'.format(str(cluster), store))

    # Add constraints
    # each store is assigned to one cluster
    for store in store_list:
        solver.Add(solver.Sum([y[cluster, store] for cluster in cluster_list]) == 1)

    if enable_minimum_maximum_elements_in_a_cluster:
        # minimum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, store] for store in store_list]) >= minimum_elements_in_a_cluster)

        # maximum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, store] for store in store_list]) <= maximum_elements_in_a_cluster)
    else:

        # minimum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, store] for store in store_list]) >= 1)

    if maximum_volume_in_a_cluster is not None:
        for cluster in cluster_list:
            solver.Add(
                solver.Sum([volume[store] * y[cluster, store] for store in store_list]) <= maximum_volume_in_a_cluster)

    # add objective
    solver.Minimize(solver.Sum(
        [distance[cluster, store].WEIGHTED_DISTANCE * y[cluster, store] for cluster, store in
         distance.keys()]))

    # solver.Minimize(1)
    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(pywraplp.MPSolverParameters.RELATIVE_MIP_GAP, 0.01)
    # solver.SetTimeLimit(self.solver_time_limit)

    solver.EnableOutput()

    solution = solver.Solve()

    # get solution
    if solution == pywraplp.Solver.OPTIMAL:

        print('Optimal solution is found')
        print('Problem solved in {} milliseconds'.format(str(solver.WallTime())))
        print('Problem solved in {} iterations'.format(str(solver.Iterations())))

        solution_final = []
        for cluster, store in distance.keys():
            solution_final.append({'CLUSTER': cluster,
                                   'LOCATION_NAME': store,
                                   'VALUE': y[cluster, store].solution_value(),
                                   'DISTANCE': distance[cluster, store].DISTANCE,
                                   'WEIGHTED_DISTANCE': distance[cluster, store].WEIGHTED_DISTANCE,
                                   'VOLUME': volume[store]})

        solution = pd.DataFrame(solution_final)

        solution = solution[solution['VALUE'] == 1]
        solution = solution[['CLUSTER', 'LOCATION_NAME', 'DISTANCE', 'WEIGHTED_DISTANCE']]

    else:
        solution = pd.DataFrame()

    return solution
