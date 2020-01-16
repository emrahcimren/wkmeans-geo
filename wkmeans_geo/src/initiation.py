from wkmeans_geo.src import clusters as cl


def randomly_assign_clusters(number_of_clusters, input_locations):
    '''
    Randomly assign locations to clusters
    :param number_of_clusters:
    :param input_locations:
    :return:
    '''
    # randomly assign customers to K clusters
    clusters = list(range(0, number_of_clusters)) * round(
        len(input_locations) / number_of_clusters + 1)

    clusters = clusters[:len(input_locations)]
    locations_with_clusters = input_locations.copy()
    locations_with_clusters['CLUSTER'] = clusters
    locations_with_clusters['CLUSTER'] = locations_with_clusters['CLUSTER'].astype(str)

    return locations_with_clusters


def initiate_algorithm(iteration,
                       locations_with_clusters):
    '''
    Initiatie the algorithm
    :param iteration:
    :param locations_with_clusters:
    :return:
    '''

    clusters = cl.calculate_cluster_centers(locations_with_clusters)

    locations_with_clusters = locations_with_clusters.merge(clusters, how='left', on='CLUSTER')

    locations_with_clusters = cl.calculate_weighted_distance(locations_with_clusters)
    locations_with_clusters['ITERATION'] = iteration

    objective = locations_with_clusters['WEIGHTED_DISTANCE'].sum().round(2)
    locations_with_clusters['OBJECTIVE'] = objective

    clusters['ITERATION'] = iteration
    locations_with_clusters['SOLUTION'] = 0

    return objective, clusters, locations_with_clusters
