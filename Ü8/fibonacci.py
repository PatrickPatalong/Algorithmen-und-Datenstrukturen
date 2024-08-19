import time
import matplotlib.pyplot as plt

def fib1(n):
    if n <= 1:
        return n
    else:
        return fib1(n-1) + fib1(n-2)

def fib3(n):
    f_n_plus_1 , f_n = fib3_impl(n)
    return f_n
def fib3_impl(n):
    if n == 0:
        return 1, 0
    else:
        f_n, f_n_minus_1 = fib3_impl(n-1)
        return f_n + f_n_minus_1, f_n

def fib5(n):
    f_k, f_k_minus_1 = 1,0
    while n > 0:
        f_k, f_k_minus_1 = f_k + f_k_minus_1, f_k
        n -= 1
    return f_k_minus_1
##########################################################################################################

def Timer(func):
    b = time.process_time()
    n = 1
    while n > 0:
        t = time.process_time()
        k = func(n)
        elapsed_time = time.process_time() - t
        wow_time = time.process_time() - b
        if wow_time > 10: # Ich war eingeschüchtert von der individuellen Laufzeit von fib5/6/7, deswegen bewertet dies
                          # im Kollektiv
            print(f"{n} Dieses Ergebnis ergibt mehr Sinn um für 10 sek suitable zu sein, ansonsten ist alles zu schnell")
            break
        if elapsed_time > 10: # Das ist die ursprügliche Laufzeit, wie gedacht, denk ich.
            print(f"{elapsed_time}sekunden: {n}, {k}")
            return elapsed_time
        elif n >= 69000: # Abbruchskriterium
            print(f"{elapsed_time}sekunden: {n}, {k}")
            wow_time = time.process_time() - b
            print(f"{wow_time} sekunden... so lange hat es gedauert bis zum Error, also n == 6900")
            return elapsed_time
        else:
            if n % 1000 == 0: #Progress
                print(n)
            n += 1

def mul2x2(a,b):
    result = []
    for m in range(4):
        result.append(None)

    for i in range(2):
        p = 2*i
        for j in range(2):
            u = p + j
            result[u] = a[p]*b[j] + a[p+1]*b[j+2]
    return result

def fib6(n):
    I = [1,1,1,0]
    temp = I
    if n == 0:
        return 0
    while n > 1:
        I = mul2x2(I, temp)
        n -= 1
    return I[2]

def fib7(n):
    temp = [] #für ungerade n sehr wichtig für multiplikation am ende
    I = [1,1,1,0]
    if n == 0:
        return 0
    while n > 1:
        if n%2 == 0:
            I = mul2x2(I,I)
            n = n/2
        elif n%2 == 1:
            temp.append(I)
            I = mul2x2(I,I)
            n = (n-1)/2

    for i in range(len(temp)-1, -1, -1): # non kommutativität beachten
        I = mul2x2(temp[i], I)

    return I[2]

if __name__ == "__main__":
    #Timer(fib1)  #n = 38
    #Timer(fib3) #Irgendetwas bigges ist damit falsch
    #Timer(fib5) #Lineare Komplexität, aber kommt bei mir zu keinem Ende... selbst bei 6900...
    #  Wie schon in der VL erklärt, ist die Komplexität des unteren linear, wobei fib5 die Zwischendaten nicht
    #  speichert ,sondern nur das Endresultat aufzeigen
    Timer(fib6) # Genau das gleiche wie fib5, aber bei linearer Entwicklung müsste es bei n=2400000 bei 10 sek sein
    Timer(fib7)  # Jesus... das war schnell




