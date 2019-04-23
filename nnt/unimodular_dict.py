"""
Choose a couple of prime numbers and unimodular elements 
corresponding to them from the paper, and put them in a dictionary 
here. The 'key' of the dictionary is the prime number (e.g. 7), and
the value iw a dictionary containing 1/4th the multiplicity (N) and
the unimodular element (xi)
"""

viable_primes_cos = [7, 11, 19, 23, 31, 43, 47, 127]

unimodular_dict = {
    7: {
        'N': 2,
        'xi': 2 + 2j
    },
    11: {
        'N': 3,
        'xi': 3 + 5j
    },
    19: {
        'N': 5,
        'xi': 4 + 2j
    },
    23: {
        'N': 2,
        'xi': 9 + 9j
    },
    31: {
        'N': 2,
        'xi': 4 + 4j
    },
    43: {
        'N': 11,
        'xi': 9 + 7j
    },
    47: {
        'N': 2,
        'xi': 20 + 20j
    },
    127: {
        'N': 2,
        'xi': 8 + 8j
    }
}

