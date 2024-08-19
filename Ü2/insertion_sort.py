import random
import numpy as np
import matplotlib.pyplot as plt
import timeit

def insertion_sort(a):
    count2 = 0
    N = len(a)
    for i in range(1,N):
        current = a[i]
        k = i
        while k > 0:
            if current < a[k-1]:
                count2 = count2+1
                a[k-1],a[k] = a[k],a[k-1]
            else:
                count2 = count2+1
                break
            k = k-1
        a[k] = current
    return count2

def main():
    MD = []
    ED = []
    for m in range(1,100):
        countarray = []
        for i in range(1,50):
            a = list(range(m))
            random.shuffle(a)
            count2 = insertion_sort(a)
            countarray = countarray + [count2]

        Durchschnitt = np.sum(countarray) / len(countarray)
        MatheDurchschnitt = m*m / 4

        ED = ED + [Durchschnitt]
        MD = MD + [MatheDurchschnitt]

    plt.plot(ED)
    plt.plot(MD)
    plt.ylabel("Empirischer/ Mathematischer Durchschnitt")
    plt.xlabel("Arraylaenge")
    plt.show()

def Zeit():
    code_to_be_measured = "insertion_sort(a)"

    initialisation = '''
    N = 1000 
    a = list(range(N)) 
    random.shuffle(a)
    '''

    t = timeit.Timer(code_to_be_measured, initialisation)

    M = 100
    time = t.timeit(M)
    print("average execution time:", time/M)




main()