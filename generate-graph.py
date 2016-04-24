#!/usr/bin/env python2

# Special thanks to Ellis Michael for YAML parsing code

from sys import argv, exit
import yaml
from matplotlib import cm
from matplotlib import pyplot as plt

from pylab import *

#########################################
## PARSE DATA
#########################################

def parse_yaml(f):
    graphs = yaml.load_all(f)
    output = [g for g in graphs]
    f.close()
    return output

#########################################
## PLOTS
#########################################

# get the set of all i-th bars in the clusters
def getBars(clusters,i):
    bars = []

    for cluster in clusters:
        bars.append(cluster[i])

    return bars

def graph(g, out_file_base, graph_num, num_graphs):
    # extract graph info
    title   = g['title']
    y_label = g['y-axis']
    x_label = g['x-axis']
    bar_labels = g['bar-labels'] # each bar in the cluster
    cluster_labels = g['cluster-labels'] # each cluster
    clusters = g['clusters'] # the actual data

    overlap = False

    # create a figure
    #fig, ax = plt.subplots(figsize=(100, 5))
    #fig, ax = plt.subplots(figsize=(15, 5))
    fig, ax = plt.subplots()

    # max width of bar
    maxwidth = 0.7
    barwidth = maxwidth

    # pass number of "clusters" to np.arrange
    X = np.arange(len(cluster_labels))  # for the x axis

    # draw bars
    barsPerCluster = len(bar_labels)
    if not overlap:
        barwidth = maxwidth / barsPerCluster
    bars = []
    for i in range(barsPerCluster):
        Ys = getBars(g['clusters'],i)
        if overlap:
            bars.append(ax.bar(X+0*barwidth, Ys, width=barwidth, facecolor=cm.jet(1.0*i/len(bar_labels)), edgecolor="black"))
        else:
            bars.append(ax.bar(X+i*barwidth, Ys, width=barwidth, facecolor=cm.jet(1.0*i/len(bar_labels)), edgecolor="black"))
        # now label values
        #for x,y in zip(X,Ys):
        #    ax.text(x+barwidth*(0.5+i), y, y, ha="center", va="bottom")

    # asthetics...
    ax.set_title(title)         #title
    ax.set_xlabel(x_label)  #X-label
    ax.set_ylabel(y_label)       #Y-label
    ax.set_xticklabels(cluster_labels) #X-benchmark labels
    ax.set_xticks(X+maxwidth/2)    #center labels

    # rotate labels
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

    xlim([0, len(cluster_labels)])
    ylim([0, 1.1*max([max(cluster) for cluster in clusters])])

    #legend
    if len(bar_labels) > 1:
        lgd = ax.legend(bars, bar_labels, bbox_to_anchor=(0.80, -0.3), ncol=2, fancybox=True)

    # fix spacing issues
    fig.tight_layout()

    if num_graphs > 1:
        save_name = "%s_%s" % (str(graph_num),out_file_base)
    else:
        save_name = out_file_base

    if len(bar_labels) > 1:
        savefig(save_name, dpi=80, bbox_extra_artists=(lgd,), bbox_inches='tight')
    else:
        savefig(save_name, dpi=80, bbox_inches='tight')

if __name__ == '__main__':
    # Parse arguments
    if len(argv) < 3:
        print("Usage: ./generate-graph.py <.yaml file> <output filename base>")
        exit(1)

    input_file_name = argv[1]
    out_file_base = argv[2]

    input_file = open(input_file_name, 'r')

    # parse yaml to find out what graphs we need to make
    graphs = parse_yaml(input_file)

    # generate each graph
    for i in range(len(graphs)):
        graph(graphs[i], out_file_base, i, len(graphs))
