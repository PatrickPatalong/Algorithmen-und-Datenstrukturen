from math import sqrt
import time

def A1():
    print(f"1) sqrt() befindet sich im Modul math und kann mit from math import sqrt() importiert werden.")

def A2():
    print(f"Es kommt ein ValueError")

def mysqrt1():
    x = int(input("Eine kleine Zahl bitte:"))
    if x > -1:
        y = sqrt(x)
        print(y)
    else:
        print(f"mysqrt()funktioniert nicht für negative Zahlen, du Dussel!")

def mysqrt2():
    try:
        x = int(input("Eine negative Zahl bitte :"))
        y = sqrt(x)
        print(y)
    except:
        print(f"mysqrt() funktioniert nicht für negative Zahlen, du Dussel!")

def A4():
    for i in range(-10, 11):
        print(f"{i}(mod 5) = {i%5}")
    print(f"In den Kommentaren wird erlaeuter wie Modulo funktioniert")
                                    #Well, der Modulooperator gibt die Differenz zwischen a-x*b: x*b<=a und x*(b+1)>a
                                     #, wobei x \in \mathbb{Z} und a,b \in \mathbb{N}

def A5():
    print("""No, really
    it doesn´t do anything
    really... stop reading
    ...
    ...
    ...
    ok... I ate your last
    piece of cake""")
    print(f"Wie man erkennt ist es fuer mehrzeilige Strings ")

def A6():
    print(f"Dictionary erlaubt durch Keywoerter an den gewünschten Wert zu gelangen. Aber nur one-way")

def A7():
    print(f"__init__() initiiert automatisch mit den geg. Argumenten in einer Klasse ein Objekt")


def main():
    print(f"Die Aufgabe 1:")
    A1()
    time.sleep(2)
    print("-"*40)
    print(f"Die Aufgabe 2:")
    A2()
    time.sleep(1)
    print("-" * 40)
    print(f"Die Aufgabe 3(if):")
    mysqrt1()
    print(f"Die Aufgabe 3(try):")
    mysqrt2()
    print("-" * 40)
    time.sleep(1)
    print(f"Die Aufgabe 4:")
    A4()
    time.sleep(2)
    print("-" * 40)
    print(f"Die Aufgabe 5:")
    A5()
    time.sleep(1)
    print("-" * 40)
    print(f"Die Aufgabe 6:")
    A6()
    time.sleep(2)
    print("-" * 40)
    print(f"Die Aufgabe 7:")
    A7()
    time.sleep(1)
    print("-" * 40)



main()
