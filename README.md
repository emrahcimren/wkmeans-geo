Weighted KMeans Clustering for Geolocational Problem
====================================================

Repo for weighted k means clustering for specifically geo locational problems. 

For an example and mathematical explanation:

https://emrahcimren.github.io/data%20science/Greenfield-Analysis-with-Weighted-Clustering/

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
pip freeze > requirements.txt
```

Installation
------------

```
pip install cimren-wkmeans-geo
```

Inputs
------

*input_locations* is a pandas dataframe with the following format.

LOCATION_NAME | LATITUDE | LONGITUDE | WEIGHT
--- | --- | --- | --- 
LOC 0 | -27.0065 | 170.583 | 1

*number_of_clusters*: Number of clusters to be created

*minimum_elements_in_a_cluster*: Minimum elements in a cluster

*maximum_elements_in_a_cluster*: Maximum elements in a cluster

*maximum_iteration*: How many maximum number of steps the algorithm takes to stop if it does not find the solution

*enable_minimum_maximum_elements_in_a_cluster*: True/False to enable minimum and maximum cluster size

*objective_range*: Acceptable difference between objectives at each iteration

Data
----
Package has a sample data set

```
from wkmeans_geo.src import data
data.
```

How to use
----------

```
from wkmeans_geo import wkmeans_clustering as wkc
clusters, locations_with_clusters = wkc.calculate_clusters(...)
```
