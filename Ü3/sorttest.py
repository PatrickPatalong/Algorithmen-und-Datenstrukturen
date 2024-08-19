import random
import numpy as np
import matplotlib.pyplot as plt
import timeit


def insertion_sort(a):
    count2 = 0
    N = len(a)
    for i in range(1, N):
        current = a[i]
        k = i
        while k > 0:
            if current < a[k - 1]:
                count2 = count2 + 1
                a[k - 1], a[k] = a[k], a[k - 1]
            else:
                count2 = count2 + 1
                break
            k = k - 1
        a[k] = current
    return count2


def partition(list, l, r):  # partition Funktion für Quick Sort
    p = random.randint(l, r)  # random pivot fpr stabilität
    pivot = list[p]
    list[p], list[r] = list[r], list[p]  # pivot an den rand setzen
    i, j = l, r - 1

    while True:
        while i < r and list[i] <= pivot:  # von links nach rechts elem suchen,
            # bis eines größer als pivot
            i += 1
            list[len(list) - 1] += 1  # je nur ein vergleich von listen elem
        list[len(list) - 1] += 1  # letzte while schleife macht vergleich auch
        # wenn nichts ausgeführt wird
        while j > l and list[j] >= pivot:  # von rechts elem suchen,
            # bis eines kleiner als pivot
            j -= 1
            list[len(list) - 1] += 1
        list[len(list) - 1] += 1

        if i < j:  # falls noch auf richtiger seite tauschen, sonst beenden
            list[i], list[j] = list[j], list[i]
        else:
            break

    list[r] = list[i]  # wissen, dass i erstes im bereich rechts von pivot ist,
    # also setzen wir es nach rechts
    list[i] = pivot  # an "frei" gewordene stelle setzen wir pivot
    return i


def quicky(list, l, r):
    if r > l:
        k = partition(list, l, r)
        quicky(list, l, k - 1)
        quicky(list, k + 1, r)
    return


def quick_sort(list):
    list.append(0)  # letztes element der list zählt vergleich
    quicky(list, 0, len(list) - 2)
    return list.pop()  # letztes elem der liste entfernen und ausgeben


def partition2(list, l, r):  # partition Funktion für Quick Sort
    pivot = list[r]  # immer rechts um stabilität zu verringern, lol
    i, j = l, r - 1

    while True:
        while i < r and list[i] <= pivot:  # von links nach rechts elem suchen,
            # bis eines größer als pivot
            i += 1
            list[len(list) - 1] += 1  # je nur ein vergleich von listen elem
        list[len(list) - 1] += 1  # letzte while schleife macht vergleich auch
        # wenn nichts ausgeführt wird
        while j > l and list[j] >= pivot:  # von rechts elem suchen,
            # bis eines kleiner als pivot
            j -= 1
            list[len(list) - 1] += 1
        list[len(list) - 1] += 1

        if i < j:  # falls noch auf richtiger seite tauschen, sonst beenden
            list[i], list[j] = list[j], list[i]
        else:
            break

    list[r] = list[i]  # wissen, dass i erstes im bereich rechts von pivot ist,
    # also setzen wir es nach rechts
    list[i] = pivot  # an "frei" gewordene stelle setzen wir pivot
    return i


def quicky2(list, l, r):
    if r > l:
        k = partition2(list, l, r)
        quicky2(list, l, k - 1)
        quicky2(list, k + 1, r)
    return


def quick_sort2(list):
    list.append(0)  # letztes element der list zählt vergleich
    quicky2(list, 0, len(list) - 2)
    return list.pop()  # letztes elem der liste entfernen und ausgeben


def comparison_plot(listsize, iteration=50):
    MDins, MDquick = [], []
    EDinsR, EDquickR = [], []  # Random Array Werte
    EDinsS, EDquickS, EDquick2S = [], [], []  # Sorted Array Werte
    for m in range(1, listsize + 1):  # Listengrößen 1 bis N (inklusiv)
        countinsR, countquickR = [], []  # Random Array Zähler pro Versuch
        countinsS, countquickS, countquick2S = [], [], []  # Sorted Array Zähler pro Versuch
        for i in range(0, iteration):  # anzahl versuche pro größe
            a = list(range(m))
            countinsS.append(insertion_sort(a))
            countquickS.append(quick_sort(a))
            countquick2S.append(quick_sort2(a))

            random.shuffle(a)
            b = list.copy(a)  # kopierte liste für quick sort
            countinsR.append(insertion_sort(a))
            countquickR.append(quick_sort(b))

        EDinsR.append(np.sum(countinsR) / len(countinsR))
        EDinsS.append(np.sum(countinsS) / len(countinsS))
        MDins.append(m * m / 4)

        EDquickR.append(np.sum(countquickR) / len(countquickR))
        EDquickS.append(np.sum(countquickS) / len(countquickS))
        EDquick2S.append(np.sum(countquick2S) / len(countquick2S))
        MDquick.append(1.38 * m * np.log2(m))

    plt.plot(MDins, label="Insertion Sort Mathematisch")
    plt.plot(MDquick, label="Quick Sort Mathematisch")
    plt.plot(EDinsR, label="Insertion Sort Empirisch (Zufälliges Array)")
    plt.plot(EDquickR, label="Quick Sort Empirisch (Zufälliges Array)")
    plt.plot(EDinsS, label="Insertion Sort Empirisch (Sortiertes Array)")
    plt.plot(EDquickS, label="Quick Sort Empirisch (Sortieres Array)")
    plt.plot(EDquick2S, label="Quick Sort 2 Empirisch (Sortieres Array)")
    plt.ylabel("Empirischer/Mathematischer Durchschnitt")
    plt.xlabel("Arraylänge")
    plt.legend()
    plt.show()


def timer(N, code, M=100):
    initialisation = f'''
import random
from __main__ import insertion_sort, quick_sort
N = {N}
a = list(range(N))'''
    code = "random.shuffle(a)\n" + code

    t = timeit.Timer(code, initialisation)
    return t.timeit(M)


def timer_plot(N, M=100):
    ratioins = []
    ratioquick = []
    for k in range(1, N + 1):
        t1 = timer(k, "insertion_sort(a)", M)
        t2 = timer(k, "quick_sort(a)", M)
        ratioins.append(0.25 * k * k / t1)
        ratioquick.append(1.38 * k * np.log2(k) / t2)

    plt.plot(ratioins, label=f"Insertion Sort")
    plt.plot(ratioquick, label=f"Quick Sort")
    plt.ylabel("(Anzahl der errechneten Vergleiche) / (tatsächliche Zeit)")
    plt.xlabel("Arraylänge")
    plt.legend()
    plt.show()


comparison_plot(200)
timer_plot(200)
