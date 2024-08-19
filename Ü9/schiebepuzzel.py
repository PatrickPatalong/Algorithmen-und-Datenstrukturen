import random
from collections import deque
import math
import time


def print_pos(p):
    for i in range(0, 16):
        if i % 4 == 3:
            print(p[i])
        else:
            print(p[i], end="  ")


def shuffle_pos(N, p):  # Wir müssen wissen, was gemixt werden soll!!!
    i = 0
    for j in range(0, 16):
        if p[j] == "":
            i = j
    old_choice = None
    while N >= 1:
        a = []
        if i % 4 != 0:  # linkscheck
            a.append(0)
        if i % 4 != 3:  # rechtscheck
            a.append(2)
        if i >= 4:  # obencheck
            a.append(1)
        if i <= 11:  # untencheck
            a.append(3)

        choice = random.choice(a)
        while (choice + 2) % 4 == old_choice:
            choice = random.choice(a)

        p, i = shuffle_pos_ex(p, choice, i)
        old_choice = choice
        N -= 1

    return p


def shuffle_pos_ex(p, n, i):
    if n == 0:
        p[i], p[i - 1] = p[i - 1], p[i]
        i = i - 1
    elif n == 2:
        p[i], p[i + 1] = p[i + 1], p[i]
        i = i + 1
    elif n == 1:
        p[i], p[i - 4] = p[i - 4], p[i]
        i = i - 4
    elif n == 3:
        p[i], p[i + 4] = p[i + 4], p[i]
        i = i + 4
    else:
        print("Irgendetwas ist falsch gelaufen")
    return p, i


def solve_pos(p, maxmove, destination):  # Wir müssen wissen, wohin wir gehen!!!
    i = 0
    k = 0
    parents = {str(p): None}
    for j in range(0, 16):
        if p[j] == "":
            i = j
    visited = []

    q = deque()  # Queue für die zu besuchenden Knoten
    q.append(p)  # Startknoten in die Queue einfügen

    while k < maxmove:
        print(len(visited))
        node = q.popleft()  # Knoten aus der Queue nehmen (first in - first out)

        for j in range(0, 16):
            if node[j] == "":
                i = j
        a = []
        if i % 4 != 0:  # linkscheck
            a.append(0)
        if i % 4 != 3:  # rechtscheck
            a.append(2)
        if i >= 4:  # obencheck
            a.append(1)
        if i <= 11:  # untencheck
            a.append(3)
        for possible in a:
            temp = node.copy()
            neighbor, u = shuffle_pos_ex(temp, possible, i)
            if neighbor in visited:
                continue
            else:
                steps = {str(neighbor): node}
                parents.update(steps)
                visited.append(neighbor)
                q.append(neighbor)
            if neighbor == destination:  # Zielknoten erreicht
                k = maxmove
                break  # => Suche beenden
            if k == maxmove - 1:
                print(f"Selbst mit mindestens einer Tiefe von {math.log(maxmove, 4)} ist keine Lösung gefunden worden")

        k += 1
    print(parents)
    print(f"Wir haben eine Länge von {len(parents)}")

    # Pfad durch die parents-Kette zurückverfolgen und speichern
    path = [destination]
    for i in range(len(parents)):
        for x in parents:
            if str(x) == str(destination):
                destination = parents[x]
                path.append(destination)
                del parents[x]
                break

    print(f"Der kürzeste Weg hat die Länge {len(path) - 2} und benötigt folgende Schritte:")
    for u in range(len(path) - 2, -1, -1):
        print_pos(path[u])


if __name__ == "__main__":
    solve1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ""]
    solve2 = ["", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    copy = solve2.copy()
    p = shuffle_pos(10, copy)
    #problem = [3, 7, 11, 4, 2, 5, 6, 8, 1, 9, 12, "", 13, 10, 14, 15]
    b = time.process_time()
    p = solve_pos(p, 20000000000, solve2)
    c = time.process_time() - b
    print(f"Der Schmarrn hat jetzt {c}sekunden gedauert")
