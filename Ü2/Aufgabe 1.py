#Wir besitzen eine totale Ordnung in allen Sinnen

"""
a)
def "x>y":
    x not "<=" y

def "x==y":
    x "<=" y and y "<=" x

def "x>=y":
    x > y or x == y

def "x != y":
    not x == y

def " x < y":
    x =< y and x!=y
"""

#b)
def issorted(a):
    for i in range(0, len(a)-1):
        if a[i] <= a[i+1]:
            i = i+1
        else:
            print(f"Nix sortiert an {i}ter Stelle")
            break

#Dies reicht aus da "<=" tranisitv ist

