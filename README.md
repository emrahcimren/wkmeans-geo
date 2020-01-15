**Weighted KMeans Clustering for Geolocational Problem**
=================

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

clusters, locations_with_clusters = wkc.get_all_files_in_directory(input_locations,
                                                                   number_of_clusters,
                                                                   minimum_elements_in_a_cluster,
                                                                   maximum_elements_in_a_cluster,
                                                                   maximum_iteration,
                                                                   objective_range)
```
