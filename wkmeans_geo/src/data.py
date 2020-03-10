'''
Create test data for testing
'''

import pandas as pd
import random
from faker import Faker
fake = Faker()

number_of_locations = 100
number_of_clusters = 3
minimum_elements_in_a_cluster = 0
maximum_elements_in_a_cluster = 200
maximum_volume_in_a_cluster = 100
maximum_iteration = 100
objective_range = 0.001
enable_minimum_maximum_elements_in_a_cluster = True

# create locations test
locations_with_clusters_test = []
for location in range(0, number_of_locations):
    locations_with_clusters_test.append({'LOCATION_NAME': 'LOC {}'.format(str(location)),
                                         'LATITUDE': float(fake.latitude()),
                                         'LONGITUDE': float(fake.longitude()),
                                         'VOLUME': 1,
                                         'WEIGHT': 1,
                                         'CLUSTER': random.randint(1, number_of_clusters)})
locations_with_clusters_test = pd.DataFrame(locations_with_clusters_test)
locations_test = locations_with_clusters_test.drop(['CLUSTER'], 1)

del location
del number_of_locations
del fake
