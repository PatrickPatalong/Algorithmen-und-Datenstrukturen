import random

def partition(a,l,r):
    pivot = a[r]
    i=l
    k=r-1
    j=0
    while True:
        while i<r and a[i] <=pivot:
            i = i + 1
            j = j +1
        while k > l and a[k] >= pivot:
            k = k-1
            j = j+1
        if i < k:
            a[i], a[k] = a[k], a[i]
            print(a)
        else:
            break
    return j


def quick_sort(a):
    quick_sort_impl(a,0,len(a)-1)
    return a

def quick_sort_impl(a,l,r):
    if r <= l:
        return a
    k = partition(a,l,r)
    quick_sort_impl(a,l,k-1)
    quick_sort_impl(a,k+1,r)

if __name__ == "__main__":
    a = [4,5,2,6,8,3,6]
    sort = quick_sort(a)
    print(sort)

