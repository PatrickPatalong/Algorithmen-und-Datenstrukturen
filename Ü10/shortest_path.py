import heapq  # heapq implementiert die Funktionen für Heaps
import json
import numpy as np


def create_graph(distance_dict):
    graph = np.zeros((len(distance_dict), len(distance_dict)))  # TODO: Vielleicht ein "einfacheres" 2-dim. Array. Hab
    # aber kein Bock das zu machen...
    citynames = {}
    i = 0
    for city in distance_dict:  # Propertymap für alle Städtenamen
        temp = {i: city}
        citynames.update(temp)
        i += 1

    #  Adjazenzliste für die Map
    for i in range(len(distance_dict)):  # Alle Zeilen abklappern
        for j in range(len(distance_dict)):  # Die Spalte abklappern
            if citynames[i] in distance_dict[citynames[j]]["Nachbarn"]:
                graph[i][j] += [1]
                # weight[(j,i)] = distance_dict[city]["Nachbarn"][neighbor] # Propertymap für Entfernungen
                # TODO: Ich weiß nicht, wie man ein Array aufbaut, sodass es ein Tupel (i,j) annimmt, sd.
                #  weight[(i,j)] funzt. Seit wann kann man das, wtf?
                # Klar, isses symmetrisch, duh...
            # else:
            # weight[(j,i)] = -1   #  Markiere, wo Entfernung nicht bekannt ist

    return graph, citynames  # , weights


if __name__ == "__main__":
    with open("entfernungen.json", encoding="utf-8") as f:
        distance_dict = json.load(f)

    graph, citynames = create_graph(distance_dict)
    print(citynames)
