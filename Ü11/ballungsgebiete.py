# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 23:12:31 2020

@author: Theresa
"""
import json
from heapq import heappush, heappop
from math import pi, cos, sin, acos
import matplotlib.pyplot as plt

# =============================================================================
# Aufgabenteil a)
# =============================================================================

def create_graph(data):
    '''Erstellt den Graphen und die benoetigten property maps'''

    # Erstelle leere Adjazenzliste
    size = len(data)
    graph = [ [] for _ in range(size) ]

    # Erstelle leere property maps
    vertex_property_map = [""]*size
    edge_property_map = {}

    # Iteration über data um die Kanten der Adjazenzliste zu erstellen
    for city, item in data.items():
        i = item["Index"]
        vertex_property_map[i] = city
        for neighbour, distance in item["Nachbarn"].items():
            j = data[neighbour]["Index"]
            graph[i].append(j)
            edge_property_map[(i, j)] = float(distance)

    return graph, vertex_property_map, edge_property_map

# =============================================================================
# Aufgabenteil c) (Tests siehe unten)
# =============================================================================

def read_position(pos):
    '''Transformiert einen input dict {"Breite": "48N50", "Länge": "10E06"}
in ein Tuple (0.8523, -0.1937)'''

    s = pos["Breite"]
    i, j = s.find("N"), s.find("S")
    if i != -1:
      breite = (float(s[:i]) + float(s[i+1:]) / 60.0) / 180.0 * pi
    elif j != -1:
      breite = -1.0 * (float(s[:j]) + float(s[j+1:]) / 60.0) / 180.0 * pi
    else:
      raise RuntimeError("Invalid Position String")

    s = pos["Länge"]
    i, j = s.find("E"), s.find("W")
    if i != -1:
      laenge = (float(s[:i]) + float(s[i+1:]) / 60.0) / 180.0 * pi
    elif j != -1:
      laenge = -1.0 * (float(s[:j]) + float(s[j+1:]) / 60.0) / 180.0 * pi
    else:
      raise RuntimeError("Invalid Position String")

    return (breite, laenge)

def cluster(graph, weights, threshold):
    forest = graph.copy()
    for city in range(len(graph)):
        i = 0
        for neighbor in graph[city]:
            if weights[(city, neighbor)] > threshold:
                forest[city][i] = None
            i += 1
    return forest

def components(forest):
    labels = {}
    count = 0
    cluster = []
    majordump = []

    for city in range(len(forest)):
        if city not in majordump:
            dump = [city]
            cluster += [city]
            while len(cluster) > 0:
                x = cluster[0]
                for neighbor in forest[x]:
                    if neighbor not in dump and neighbor is not None:
                        cluster.append(neighbor)
                        dump.append(neighbor)
                        majordump.append(neighbor)
                del(cluster[0])

            label = {count: dump}
            labels.update(label)
            count += 1

    return labels, count

def comparison_plt(distance_dict, min_threshold,max_threshold):
    BG = [None] * min_threshold
    for i in range(min_threshold, max_threshold):
        graph, names, weights = create_graph(distance_dict)
        forest = cluster(graph, weights, i)
        labels, count = components(forest)
        BG += [count]
    plt.plot(BG, label="Ballungsgebietsanzahl")
    plt.xlabel("Threshold")
    plt.ylabel("Clustering")
    plt.xlim(min_threshold, max_threshold+1)
    plt.ylim(0, BG[min_threshold])
    plt.legend()
    plt.show()

def cluster_map(labels, distance_dict):
    mapping = {}
    i = 0
    cluster_map = []
    for city in distance_dict:
        b, l = read_position(distance_dict[city]["Koordinaten"])
        temp = {i : (b,l)}
        mapping.update(temp)
        i += 1

    for i in range(len(labels)):
        temp = []
        for city in labels[i]:
            temp.append(mapping[city])
        cluster_map.append(temp)

    for j in range(len(cluster_map)):
        x_val = [x[0] for x in cluster_map[j]]
        y_val = [x[1] for x in cluster_map[j]]
        plt.plot(y_val, x_val)

    plt.savefig("ballungsgebiete.svg")



# =============================================================================
# Main-Funktion
# =============================================================================

if __name__ == '__main__':

    #Aufgabenteil a)
    with open("entfernungen.json", encoding="utf-8") as f:
        distance_dict = json.load(f)

    # Iteration durch die Städtenamen der JSON Daten. Jede Stadt erhält
    # zusätzlich einen Index, den wir ins distance_dict einfügen, damit
    # wir den zugehörigen Knoten zu einem Städtenamen schnell finden können
    for i, city in enumerate(distance_dict):
        distance_dict[city]["Index"] = i

    graph, names, weights = create_graph(distance_dict)
    forest = cluster(graph, weights, 35)
    labels, count = components(forest)
    comparison_plt(distance_dict, 50, 130)
    cluster_map(labels, distance_dict)