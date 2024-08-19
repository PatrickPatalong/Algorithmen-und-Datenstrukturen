# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 23:12:31 2020

@author: Theresa
"""
import json
from heapq import heappush, heappop
from math import pi, cos, sin, acos

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

def check_symmetry(edge_property_map):
    """Prüft ob eine Kanten Property Map symmetrisch ist"""
    for indices, distance in edge_property_map.items():
        i = indices[0]
        j = indices[1]
        if distance != edge_property_map[(j, i)]:
            return False
    return True

# =============================================================================
# Aufgabenteil b)
# =============================================================================

def dijkstra(graph, weights, startnode, destination):
    """Der Algorithmus von Dijkstra, so wie er im Vorlesungsskript behandelt wurde."""
    parents = [None]*len(graph)       # registriere für jeden Knoten den Vaterknoten im Pfadbaum

    q = []                            # Array q wird als Heap verwendet
    heappush(q, (0.0, startnode, startnode))  # Startknoten in Heap einfügen

    while len(q) > 0:                 # solange es noch Knoten im Heap gibt:
        length, node, predecessor = heappop(q)   # Knoten aus dem Heap nehmen
        if parents[node] is not None: # parent ist schon gesetzt => es gab einen anderen, kürzeren Weg
            continue                  #   => wir können diesen Weg ignorieren
        parents[node] = predecessor   # parent setzen
        if node == destination:       # Zielknoten erreicht
            break                     #   => Suche beenden
        for neighbor in graph[node]:  # die Nachbarn von node besuchen,
            if parents[neighbor] is None:   # aber nur, wenn ihr kürzester Weg noch nicht bekannt ist
                new_length = length + weights[(node,neighbor)]   # berechne Pfadlänge zu neighbor
                heappush(q, (new_length, neighbor, node))  # und füge neighbor in den Heap ein

    if parents[destination] is None:  # Suche wurde beendet ohne den Zielknoten zu besuchen
        return None, None             # => kein Pfad gefunden (unzusammenhängender Graph)

    # Pfad durch die parents-Kette zurückverfolgen und speichern
    path = [destination]
    while path[-1] != startnode:
        path.append(parents[path[-1]])
    path.reverse()                    # Reihenfolge umdrehen (Ziel => Start wird zu Start => Ziel)
    return path, length, len(graph) - parents.count(None)  # gefundenen Pfad und dessen Länge sowie Anzahl besuchter Knoten zurückgeben

def print_shortest_path(names, weights, path, distance):
    result = names[path[0]]
    for i in range(1, len(path)):
        result += " => %.1f km => %s" % (weights[(path[i-1], path[i])], names[path[i]])
    result += " (insgesamt: %.1f km, %d Zwischenstationen)" % (distance, len(path)-2)
    print(result)

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


def compute_air_distance(data):
    result = {}
    for i, (city1, item1) in enumerate(data.items()):
        for j, (city2, item2) in enumerate(data.items()):
            if i == j:
                # Wir behandeln den Fall "Abstand zu sich selbst" separat,
                # weil die geometrische Formel in diesem Fall numerisch instabil ist:
                # Manchmal kommt sin(b1)*sin(b2) + cos(b1)*cos(b2)*cos(l2-l1) > 1.0
                # heraus, was zu einem ValueError in acos(...) führt.
                # Wir könnten diesen Fall auch überspringen, weil der A*-Algorithmus
                # result[(i, i)] niemals abfragt.
                result[(i, i)] = 0.0
            elif i < j:
                # Wir müssen den Abstand nur einmal berechnen, weil er symmetrisch ist.
                b1, l1 = read_position(data[city1]["Koordinaten"])
                b2, l2 = read_position(data[city2]["Koordinaten"])
                e = 6378.137 * acos( sin(b1)*sin(b2) + cos(b1)*cos(b2)*cos(l2-l1) )
                result[(i, j)] = e
                result[(j, i)] = e
    return result

def test_estimates(weights, estimates):
    for indices, distance in weights.items():
        if (estimates[indices] > distance):
            return False
    return True

def a_star(graph, weights, estimates, startnode, destination):
    """A* als Weiterentwicklung der Dijkstra-Implementation."""
    parents = [None]*len(graph)       # registriere für jeden Knoten den Vaterknoten im Pfadbaum

    q = []                            # Array q wird als Heap verwendet
    heappush(q, (0.0, 0.0, startnode, startnode))  # Startknoten in Heap einfügen

    # An erster Stelle jedes Tupels im Heap steht die Entfernungsabschätzung,
    # damit diese als Priorität im Heap verwendet wird und jeweils der Knoten
    # mit der geringsten geschätzten Entfernung vom Ziel als nächstes betrachtet wird.

    while len(q) > 0:                 # solange es noch Knoten im Heap gibt:
        # Der Heapeintrag enthaelt als ersten Parameter die Entfernungsabschätzung.
        # Diese wird verworfen, da sie nur zum Sortieren der Warteschlagee
        # benötigt wird.
        old_estimate, length, node, predecessor = heappop(q)   # Knoten aus dem Heap nehmen
        if parents[node] is not None: # parent ist schon gesetzt => es gab einen anderen, kürzeren Weg
            continue                  #   => wir können diesen Weg ignorieren
        parents[node] = predecessor   # parent setzen
        if node == destination:       # Zielknoten erreicht
            break                     #   => Suche beenden
        for neighbor in graph[node]:  # die Nachbarn von node besuchen,
            if parents[neighbor] is None:   # aber nur, wenn ihr kürzester Weg noch nicht bekannt ist
                new_length = length + weights[(node, neighbor)]   # berechne Pfadlänge zu neighbor
                priority = new_length + estimates[(neighbor, destination)] # berechne geschätzte Entfernung zum Ziel
                heappush(q, (priority, new_length, neighbor, node))  # und füge neighbor in den Heap ein

    if parents[destination] is None:  # Suche wurde beendet ohne den Zielknoten zu besuchen
        return None, None             # => kein Pfad gefunden (unzusammenhängender Graph)

    # Pfad durch die parents-Kette zurückverfolgen und speichern
    path = [destination]
    while path[-1] != startnode:
        path.append(parents[path[-1]])
    path.reverse()                    # Reihenfolge umdrehen (Ziel => Start wird zu Start => Ziel)
    return path, length, len(graph) - parents.count(None)  # gefundenen Pfad und dessen Länge sowie Anzahl besuchter Knoten zurückgeben


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
    symmetric = check_symmetry(weights)
    print("Aufgabenteil a):")
    print("-"*80)
    print("'weights' ist für den Entfernungsgraphen {0:s}symmetrisch.".format("" if symmetric else "nicht "))

    # Für die folgenden Aufgabenteile können wir also beruhigt voraussetzen, dass
    # weights symmetrisch ist, d. h. für alle Knotenindizes i, j gilt:
    # Die Kante von i nach j hat das gleiche Gewicht wie die Kante von j nach i.


    print("\n" + "-"*80)
    # Aufgabenteil b)
    print("Aufgabenteil b):")
    cities = [
            ("Aachen", "Passau"),
            ("Saarbrücken", "Leipzig"),
            ("München", "Greifswald"),
            ("Konstanz", "Kassel"),
    ]

    # Aufgabenteil c)
    print("Aufgabenteil c):")
    print("-"*80)
    print("air_distance muss auch Paare von Knoten enthalten, zwischen denen keine Kante besteht, \
da der A*-Algorithmus von jedem beliebigen Knoten aus in der Lage sein muss, \
einen Schätzwert für die Restdistanz zu jedem beliebigen anderen, als Endknoten \
gewählten Knoten zu bekommen.")
    print("-"*80 + "\n")

    air_distance = compute_air_distance(distance_dict)

    print("Der Test bestätigt{0:s}, dass die Luftlinienentfernungen für direkt verbundene Städtepaare \
nie größer sind als die Straßenentfernungen.".format("" if test_estimates(weights, air_distance) else "vnicht"))


    print("-"*80 + "\n")

    print("-"*80)
    for c in cities:
        print("Bestimme Entfernung... ")
        start = distance_dict[c[0]]["Index"]
        destination = distance_dict[c[1]]["Index"]
        path_d, distance_d, count_d = dijkstra(graph, weights, start, destination)
        path_a, distance_a, count_a = a_star(graph, weights, air_distance, start, destination)

        if(path_d == path_a and distance_d == distance_a):
            print_shortest_path(names, weights, path_d, distance_d)
            print("Anzahl besuchter Knoten Dijkstra:", count_d)
            print("Anzahl besuchter Knoten A*:      ", count_a)
        else:
            print("Fehler! Gefundene Wege sind nicht die gleichen.")
        print("-"*80)

    print("Wir stellen fest: Der A*-Algorithmus führt zu einer deutlichen Beschleunigung. \
Wir besuchen jeweils nur etwa ein Viertel bis die Hälfte der Knoten, die der Dijkstra-Algorithmus besucht hat.")

