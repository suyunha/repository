from numpy import real, imag, uint8
from numpy import asarray, outer, arange, ones
from numpy import where, array_equal
from matplotlib.pyplot import imread, imshow, show

def modulo_product(A, B, p):
    return (A * B) % p

def modulo_power(xi, A, p):
    #
    # Flatten just so that it's easier to think about
    # (this is not necessary)
    original_shape = A.shape
    powers = A.flatten()
    #
    # Create the zeroth power array as init
    Z = ones(powers.shape) + 0j
    #
    # Iterate over all powers in the array
    # and multiply by xi for each power
    # being sure to modulo at each step to prevent
    # overflow
    m = max(powers)
    for k in range(m):
        cur_mask = where(powers > k)
        Z[cur_mask] = Z[cur_mask] * xi
        Z = (real(Z) % p) + (imag(Z) % p) * 1j
    #
    return Z.reshape(original_shape)


def compute_FFCT_matrix(A, xi, p):
    #
    # Confirm that p is a supported prime number
    if p not in [7, 11, 19, 23, 31, 43, 47, 127]:
        raise Exception("Only the following prime numbers are supported: [7, 11, 19, 23, 31, 43, 47, 127]")
    #
    # Confirm that xi is unimodular in GF(p)
    modulus = (real(xi)**2 + imag(xi)**2)
    modmod = modulus % p
    if modmod != 1.:
        raise Exception("Your choice of xi in GF(p) must be unimodular: %i != 1 mod %i" % (int(modulus), p))
    #
    # Compute the cos transform
    cosA = real(modulo_power(xi, A, p)).astype(int)
    #
    return cosA


def FFCT_sub_image(sub_image, C, p):
    #
    # Make sure the subimage is the right size
    if not array_equal(sub_image.shape[:2], C.shape):
        raise Exception("The sub image and FFCT matrix must have the same dimensions")
    #
    # Iterate over each channel and apply the cosine transform
    for i in range(sub_image.shape[2]):
        sub_image[:,:,i] = (C @ sub_image[:,:,i] @ C.T) % p
    #
    return sub_image

p = 7
N = 2
xi = 2+2j

x = arange(N)
Cprime = outer(2*x + 1, x)
Z = compute_FFCT_matrix(Cprime, xi, p)

A = (imread("grayscale.png") * 255).astype(uint8)

imshow(A, cmap="gray")
show()


