from numpy import real, imag, uint8, linspace, pi, sin, zeros
from numpy import asarray, outer, arange, ones
from numpy import where, array_equal
from matplotlib.pyplot import imread, imshow, show
from unimodular_dict import viable_primes_cos
from utils import make_dimensions_compatible

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
    if p not in viable_primes_cos:
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
    if not array_equal(sub_image.shape, C.shape):
        raise Exception("The sub image and FFCT matrix must have the same dimensions")
    #
    # Apply the cosine transform
    sub_image[:,:]= (C @ sub_image[:,:] @ C.T) % p
    #
    return sub_image

def get_subimages(img, N):
    p = img.shape[0] // N
    q = img.shape[1] // N
    for i in range(p):
        for j in range(q):
            yield tuple([slice(i*N, (i+1)*N), slice(j*N, (j+1)*N)])

def get_sinusoidal_watermark(img):
    m, n = img.shape
    p = m // 6 + 1
    q = n // 8 + 1
    wave_period = [
        [ 0,  0,  0,  0, 255, 0,  0,  0],
        [ 0,  0,  0, 255, 0, 255, 0,  0],
        [ 0,  0, 255, 0,  0 , 0, 255, 0],
        [ 0,  0, 255, 0,  0 , 0, 255, 0],
        [ 0, 255, 0,  0,  0 , 0,  0, 255],
        [255, 0,  0,  0,  0 , 0,  0,  0],
    ]
    wave_period = asarray(wave_period)
    watermark = zeros((p * 6, q * 8))
    for i in range(p):
        for j in range(q):
            watermark[(i*6):((i+1)*6), (j*8):((j+1)*8)] = wave_period
    return watermark[:m, :n]

p = 7
N = 2
xi = 2+2j

x = arange(N)
Cprime = outer(2*x + 1, x)
C = compute_FFCT_matrix(Cprime, xi, p)

A = (imread("grayscale.png") * 255).astype(uint8)

# AA = make_dimensions_compatible(A, N)
# AA_r = AA % p
# AA_m = AA - AA_r

# for si in get_subimages(AA_r, N):
#     AA_r[si] = FFCT_sub_image(AA_r[si], C, p)

get_sinusoidal_watermark(A)

# print(AA.shape)
# print(A.shape)

# imshow(A, cmap="gray")
# show()

imshow(get_sinusoidal_watermark(A), cmap="gray")
show()
