from numpy import zeros, arange, triu, tril, eye
from numpy import all as np_all
from numpy import argmax as np_argmax
from numpy import abs as np_abs


def pg5_ex1(U, b):
    #
    # If U is a numpy array, then U.shape is a list 
    # containing the length of each dimension of U. Thus,
    # U.shape[0] is the number of rows of U
    n = U.shape[0]
    #
    # Create an n x 1 vector of zeros
    x = zeros(n, 1)
    #
    # for k = n, n-1, ..., 2, 1 -- in decreasing order!
    for k in range(n, 0, -1):
        #
        # Divide the kth entry b by (k,k) entry of U
        # and assign it to the kth entry of x
        x[k] = b[k] / U[k, k]
        #
        # Create a list of integers: [0, 1, ..., k-2]
        i = arange(k-1)
        #
        # Assign b[0, 1, ..., k-2] all at once
        b[i] = b[i] - x[k] * U[i, k]
    #
    return x


def pg5_ex2(U, b):
    n = U.shape[0]
    x = zeros(n, 1)
    for k in range(n, 0, -1):
        j = range(k+1, n)
        x[k] = (b[k] - U[k,j] * x[j]) / U[k,k]
    return x


def lutx(A):
    #
    # Get dimensions and create permutation tracker
    n = A.shape[0]
    p = arange(n)
    #
    # Iterate over n-1 rows...k = 0, 1, ..., n-2
    for k in range(n-1):
        #
        # Find the largest element below the diagonal
        # in the kth column
        m = np_argmax(
                np_abs(
                    A[k+1:n,k]
                )
            )
        m = m + k
        #
        # Skip elimination if the column is zero
        if A[m,k] != 0:
            #
            # Swap pivot row
            if m != k:
                A[[k,m],:] = A[[m,k],:]
                p[[k,m]] = p[[m,k]]
            #
            # Compute multipliers
            i = arange(k+1,n)
            A[i,k] = A[i,k] / A[k,k]
            #
            # Update the remainder of the matrix
            j = arange(k+1,n)
            A[i,j] = A[i,j] - A[i,k] @ A[k,j]
    #
    # Separate result
    L = tril(A, -1) + eye(n)
    U = triu(A)
    #
    print(L)
    print(U)
    #
    return L, U, p
