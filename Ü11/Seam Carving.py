from pgm import read_pgm, write_pgm
import heapq

def create_graph(image, height, width):
    N = len(image)
    # graph direkt erweitern für start und ziel
    graph = [[] for k in range(N+2)]
    weights = {}
    for index in range(N):
        color = image[index]
        # pixel index in x und y werte ändern
        x, y = index % width, index // width

        # für pixel in erster zeile die kante vom start einfügen
        if y == 0:
            graph[N].append(index)
            weights[(N, index)] = 0

        # für pixel in letzter zeile kante zum ziel einfügen
        if y == height-1:
            graph[index].append(N + 1)
            weights[(index, N + 1)] = 0

        # außer für pixel in der letzen zeile nun knoten in die nächste zeile einfügen
        if y != height-1:
            # pixel am linken rand haben keine kante nach unten links
            if x != 0:
                index_left = (x-1) + (y+1) * width
                graph[index].append(index_left)
                weights[(index, index_left)] = abs(color - image[index_left])

            # eine kante gerade nach unten haben alle
            index_down = x + (y+1) * width
            graph[index].append(index_down)
            weights[(index, index_down)] = abs(color - image[index_down])

            # pixel am rechten rand haben keine kante nach unten links
            if x != width-1:
                index_right = (x+1) + (y+1) * width
                graph[index].append(index_right)
                weights[(index, index_right)] = abs(color - image[index_right])

    return graph, weights

def dijkstra(graph, weights, start, destination):
    # initialisiere parents und heap für berechnung
    parents = [None] * len(graph)
    q = []
    heapq.heappush(q, (0.0, start, start))

    while len(q) > 0:  # solange heap nicht leer
        # obersten knoten ansehen, es ist der kürzester weg den wir bisher kennen
        length, node, predecessor = heapq.heappop(q)
        # prüfen ob wir schonmal an diesem knoten waren (da gäbe es bereits kürzeren weg zu diesem knoten)
        if parents[node] is not None:
            continue
        # kürzester weg zu diesem knoten gefunden, vorgänger merken für pfad
        parents[node] = predecessor
        if node == destination:  # ziel erreicht, mit dem kürzesten weg, da er ganz oben war
            break  # beenden
        # wege zu allen nachbarn bestimmen und in heap einfügen (im heap wird dann automatisch die länge sortiert
        for neighbor in graph[node]:
            if parents[neighbor] is None:
                heapq.heappush(q, (length + weights[(node, neighbor)], neighbor, node))

    if parents[destination] is None: # falls ziel nicht gefunden
        return None, None

    path = [destination] # pfad rekonstruieren
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()  # reihenfolge anpassen
    return path

# man kann davon ausgehen, dass der pfad keine wichtigen pixel enthält, da nach def der gewichte der kürzeste pfad
# immer der ist bei dem am wenigsten veränderung der pixel stattfindet, also zum beispiel ein himmelbereich in dem fast
# alles blau ist, wird so als unwichtig eingestuft

def drop_pixels(image, path):
    new_image = []
    i = 0
    # einfach prüfen ob das pixel im weg liegt oder nicht, je nachdem in das neue bild einfügen
    for pixel in image:
        if i not in path:
            new_image.append(pixel)
        i += 1
    return new_image

def seam_carving(image, width, height, new_width):
    # bild für schleife kopieren
    new_image = list(image)
    # bis breite richtig ist aus bild jeweils graph erzeugen, dann kürzesten weg finden und weg aus dem bild entfernen
    while width != new_width:
        graph, weights = create_graph(new_image, height, width)
        N = len(graph)
        path = dijkstra(graph, weights, N - 2, N - 1)
        new_image = drop_pixels(new_image, path)
        width -= 1

    return new_image


if __name__ == "__main__":
    width, height, image = read_pgm("coast.pgm")
    graph, weights = create_graph(image, height, width)
    N = len(graph)

    path = dijkstra(graph, weights, N-2, N-1)
    new_image = drop_pixels(image, path)
    write_pgm(width-1, height, new_image, "coast-1.pgm")

    squared_image = seam_carving(image, width, height, height)
    write_pgm(height, height, squared_image, "coast-square.pgm")

    