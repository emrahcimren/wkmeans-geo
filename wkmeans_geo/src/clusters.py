
from helpers import haversine_distance


def calculate_cluster_centers(locations_with_clusters):
    '''
    Calculate cluster centers
    :param locations_with_clusters:
    :return:
    '''

    cluster_lat_lons = locations_with_clusters.groupby(['CLUSTER'], as_index=False).agg(
        {'LATITUDE': 'sum', 'LONGITUDE': 'sum',
         'LOCATION_NAME': 'count'}).rename(
        columns={'LATITUDE': 'NEW_CLUSTER_LATITUDE', 'LONGITUDE': 'NEW_CLUSTER_LONGITUDE',
                 'LOCATION_NAME': 'NUMBER_OF_CUSTOMERS_IN_A_CLUSTER'})

    cluster_lat_lons['NEW_CLUSTER_LATITUDE'] = cluster_lat_lons['NEW_CLUSTER_LATITUDE'] / cluster_lat_lons['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']
    cluster_lat_lons['NEW_CLUSTER_LONGITUDE'] = cluster_lat_lons['NEW_CLUSTER_LONGITUDE'] / cluster_lat_lons['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']

    cluster_lat_lons['CLUSTER_LATITUDE'] = cluster_lat_lons['NEW_CLUSTER_LATITUDE']
    cluster_lat_lons['CLUSTER_LONGITUDE'] = cluster_lat_lons['NEW_CLUSTER_LONGITUDE']
    cluster_lat_lons.drop(['NEW_CLUSTER_LATITUDE', 'NEW_CLUSTER_LONGITUDE', 'NUMBER_OF_CUSTOMERS_IN_A_CLUSTER'], 1, inplace=True)

    return cluster_lat_lons


def calculate_weighted_distance(locations_with_clusters):
    '''
    Calculate weighted distance
    :param locations_with_clusters:
    :return:
    '''

    distance = haversine_distance.calculate_haversine_distance(locations_with_clusters['LATITUDE'],
                                                               locations_with_clusters['LONGITUDE'],
                                                               locations_with_clusters['CLUSTER_LATITUDE'],
                                                               locations_with_clusters['CLUSTER_LONGITUDE'])
    locations_with_clusters['DISTANCE'] = distance
    locations_with_clusters['WEIGHTED_DISTANCE'] = locations_with_clusters['DISTANCE'] * locations_with_clusters['WEIGHT']

    return locations_with_clusters


def calculate_distance_matrix(locations_at_iteration, clusters_for_distance):
    '''
    Calculate distance matrix
    :param locations_at_iteration:
    :param clusters_for_distance:
    :return:
    '''

    locations_at_iteration['Key'] = 0
    clusters_for_distance['Key'] = 0
    locations_at_iteration_with_clusters = locations_at_iteration.merge(clusters_for_distance)
    locations_at_iteration_with_clusters = calculate_weighted_distance(locations_at_iteration_with_clusters)

    return locations_at_iteration_with_clusters [['LOCATION_NAME', 'CLUSTER', 'DISTANCE', 'WEIGHTED_DISTANCE', 'VOLUME']]
