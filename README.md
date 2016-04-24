generate-graph
==============

Generates a pyploy barplot from a YAML file

Input
-----

The script takes a YAML file of the following format:

```
---
title: "test1 x vs y"
x-axis: x
y-axis: y
bar-labels:
   - a 
   - b 
   - c
   - d
   - e
cluster-labels: 
   - c1 
   - c2 
   - c3
   - c4
clusters:
   #  a  b  c  d  e
   - [1, 1, 1, 1, 1] # c1
   - [1, 2, 3, 4, 5] # c2
   - [1, 3, 4, 2, 9] # c3
   - [1, 3, 4, 2, 9] # c4
...
```

- title -- the title of the graph
- x-axis -- the x-axis label
- y-axis -- the y-axis label
- bar-labels -- the labels for the different bars within a cluster (these show up in the legend)
- cluster-labels -- the labels for each cluster/subset of bars in the bar plot
- clusters -- the actual data

The number of cluster labels must be consistent with the number of items in the clusters sequence, and the number of bar labels must be consistent with the number of elements in each sub-sequence (each cluster).

Running
```
python generate-graph.py sample.yaml sample.png
```
produces `0_sample.png` and `1_sample.png`

Output
------
A graph generated by matplotlib.pyplot. Depending on the extension of the base filename you pass in, you could get any of these file types supported by matplotlib:
 * eps
 * jpeg, jpg
 * pdf
 * pgf
 * png
 * ps
 * raw
 * rgba
 * svg
 * svgz
 * tif, tiff

Usage
-----
```
./generate-graph.py -i <yaml-filename> <base_filename>
```
