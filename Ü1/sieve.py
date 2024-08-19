def sieve(n):

    primes = [i for i in range(0,n+1)]
    p = 2

    while (p*p <= n):

        if primes[p] > 0:

            for j in range(p*2, len(primes), p):
                primes[j] = 0

        p = p+1

    for k in range(n, 0, -1):
        if primes[k] == 0:
            k -= 1
            del primes[k+1]

    del primes[1]
    del primes[0]

    return primes
