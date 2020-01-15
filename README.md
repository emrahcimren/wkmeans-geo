**Weighted KMeans Clustering for Geolocational Problem**
=================

Repo for weighted k means clustering for specifically geo locational problems. 

Prerequisites
-------------

Install environment.yml for prerequisites.

```
conda env create -f environment.yml
```

To recreate environment.yml

```
conda env export > environment.yml
```

To create requirements.txt from environment.yml

```
conda list -e > requirements.txt
```

Installation
------------

```
pip install cimren-wkmeans-geo
```

How to use
----------

```
from wkmeans_geo import wkmeans_clustering as wkc

clusters, locations_with_clusters = wkc.calculate_clusters(input_locations,
                                                                   number_of_clusters,
                                                                   minimum_elements_in_a_cluster,
                                                                   maximum_elements_in_a_cluster,
                                                                   maximum_iteration,
                                                                   enable_minimum_maximum_elements_in_a_cluster,
                                                                   objective_range)
```
