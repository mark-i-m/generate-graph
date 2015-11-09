#!/usr/bin/env python2

# Special thanks to Ellis Michael for YAML parsing code

import argparse
import yaml
from matplotlib import cm
from matplotlib import pyplot as plt

from pylab import *

#########################################
## PARSE COMMAND LINE ARGS
#########################################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
        type=argparse.FileType('r'), required=True)

    return vars(parser.parse_args())

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

def graph(g):

    # extract graph info
    title   = g['title']
    y_label = g['y-axis']
    x_label = g['x-axis']
    bar_labels = g['bar-labels'] # each bar in the cluster
    cluster_labels = g['cluster-labels'] # each cluster
    clusters = g['clusters'] # the actual data

    # create a figure
    fig, ax = plt.subplots()

    # max width of bar
    maxwidth = 0.7
    barwidth = maxwidth

    # pass number of "clusters" to np.arrange
    X = np.arange(len(cluster_labels))  # for the x axis

    # draw bars
    barsPerCluster = len(bar_labels)
    barwidth = maxwidth / barsPerCluster
    bars = []
    for i in range(barsPerCluster):
        Ys = getBars(g['clusters'],i)
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
    lgd = ax.legend(bars, bar_labels, bbox_to_anchor=(0.80, -0.3), ncol=2, fancybox=True)

    # fix spacing issues
    fig.tight_layout()

    savefig(title+".pdf", dpi=80, bbox_extra_artists=(lgd,), bbox_inches='tight')

def main():
    # Parse arguments
    args = parse_args()
    input_file = args['input']

    # parse yaml to find out what graphs we need to make
    graphs = parse_yaml(input_file)

    # generate each graph
    for g in graphs:
        graph(g)

if __name__ == '__main__':
    main()
