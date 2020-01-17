'''
Create clusters from an input file
'''

from wkmeans_geo.src import clusters as cl
import pandas as pd


def create_initial_clusters_from_given_input(number_of_clusters, initial_solution):
    '''
    Function to create initial clusters from input
    :param number_of_clusters:
    :param initial_solution:
    :return:
    '''

    given_number_of_clusters = len(initial_solution['CLUSTER'].unique())

    if number_of_clusters > given_number_of_clusters:

        initial_solution_clusters = cl.calculate_cluster_centers(initial_solution)
        initial_solution_with_clusters = initial_solution.merge(initial_solution_clusters, how='left', on='CLUSTER')
        initial_solution_with_clusters = cl.calculate_weighted_distance(initial_solution_with_clusters )

        initial_solution_summary = initial_solution_with_clusters.groupby(['CLUSTER'], as_index=False).agg({'LOCATION_NAME': 'count', 'WEIGHTED_DISTANCE': 'sum'})
        initial_solution_summary.rename(columns={'LOCATION_NAME': 'NUMBER_OF_LOCATIONS', 'WEIGHTED_DISTANCE': 'TOTAL_WEIGHTED_DISTANCE'}, inplace=True)
        initial_solution_summary.sort_values(by=['TOTAL_WEIGHTED_DISTANCE'], ascending=False, inplace=True)

        # filter clusters where number of locations is twice as big as given cluster and number of cluster difference
        filter_clusters = initial_solution_summary['NUMBER_OF_LOCATIONS'] > 2*(number_of_clusters - given_number_of_clusters)
        top_clusters = initial_solution_summary[filter_clusters]
        top_clusters = top_clusters.head(1)

        #
        top_cluster = initial_solution_with_clusters[initial_solution_with_clusters['CLUSTER']==top_clusters['CLUSTER'].iloc[0]]
        top_cluster.sort_values(by=['WEIGHTED_DISTANCE'], ascending=False, inplace=True)

        clusters_added = range(1, (number_of_clusters - given_number_of_clusters)+1)
        idx=0
        cluster_no = given_number_of_clusters
        new_location_store = []
        for cluster in clusters_added:
            cluster_no = cluster_no + 1
            new_location_store.append(pd.DataFrame([{'LOCATION_NAME': top_cluster.iloc[idx]['LOCATION_NAME'],
                                        'NEW_CLUSTER': str(cluster_no)}]))
            idx=idx+1
        new_location_store = pd.concat(new_location_store)

        initial_solution = initial_solution.merge(new_location_store, how='left')
        filter_new_clusters = initial_solution['NEW_CLUSTER'].notnull()
        initial_solution.loc[filter_new_clusters, 'CLUSTER'] = initial_solution.loc[filter_new_clusters, 'NEW_CLUSTER']
        initial_solution.drop(['NEW_CLUSTER'], 1, inplace=True)

        return initial_solution

    else:

        raise Exception('Number of Clusters should be more than total number of clusters in the initial solution')