**Weighted KMeans Clustering for Geolocational Problem**
=================



Installation
------------

```
pip install cimren-wkmeans-geo
```

How to use
----------

```
from wkmeans_geo import wkmeans_clustering as wkc

clusters, locations_with_clusters = wkc.get_all_files_in_directory(input_locations,
                                                                   number_of_clusters,
                                                                   minimum_elements_in_a_cluster,
                                                                   maximum_elements_in_a_cluster,
                                                                   maximum_iteration,
                                                                   objective_range)
```
