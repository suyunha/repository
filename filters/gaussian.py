from scipy.signal import sepfir2d
from numpy import ones, zeros
from numpy import pad
from numpy import sum
from numpy import convolve
from utils.image_wrapper import image_wrapper
from numpy import empty
from scipy.stats import norm
from numpy import float32


def two_d_gaussian_filter(img_wrapper, padding_type='mirror', kernel_length=5):
    #
    # First, get a padded version of the image
    #
    # You will have to implement the 'get_padded_img()' method in the img_wrapper class
    padded_image = img_wrapper.get_padded_image(padding_size=kernel_length)
    #
    # Generate the 1D Gaussian kernel using either:
    #   - true_one_d_gaussian_kernel, or
    #   - approximate_one_d_gaussian_kernel
    #
    # You will have to implement these functions below
    one_d_gaussian_kernel = approximate_one_d_gaussian_kernel(desired_kernel_length=kernel_length)
    #one_d_gaussian_kernel = true_one_d_gaussian_kernel(desired_kernel_length = kernel_length)
    #
    # Apply the filter to the image using the function sepfir2d(). 
    # Note:
    #   - We can only do this because the Gaussian kernel is separable.
    #   - We're using a symmetric Gaussian for our blur, which 
    #   means that the same kernel will be used for both the horizontal
    #   and vertical directions. It's possible to use different ones in
    #   each direction.
    a = padded_image.shape
    blurred_img = zeros(a)
    for z in range(a[2]):
        blurred_img[:, :, z] = sepfir2d(padded_image[:, :, z], one_d_gaussian_kernel, one_d_gaussian_kernel)
    #
    # Create a new img_wrapper using the blurred img
    #
    # You will have to implement the image_wrapper.extract_from_padding() method
    blurred_img_wrapper = image_wrapper(image_array=blurred_img, padding_size=kernel_length)
    # 
    return blurred_img_wrapper

def true_one_d_gaussian_kernel(desired_kernel_length=5, desired_probability_mass=0.95):
    '''Compute the weights assigned to each pixel in the 1-d Gaussian filter

    Inputs:
         - desired_kernel_length (int): how many pixels do you want to average (must be an odd number to center at the pixel)
         - desired_probability_mass (float): what fraction of the Gaussian distribution are you going to spread out over those pixels

    Returns:
        - one_d_gaussian_kernel (ndarray[float]): normalized, i.e., its entries sum to one, kernel of length 'desired_kernel_length'
    '''
    #
    # Initialize
    one_d_gaussian_kernel = empty(desired_kernel_length, dtype = float32)
    #
    # Throw an error if the kernel length is not odd
    if desired_kernel_length % 2 == 0: 
        raise Exception("Kernel length must be odd.")
    #
    # First figure out the value of x such that P(-x < X < x) = desired_probability_mass
    # Hint: 
    #   1. Use the inverse CDF function to compute y1 such that P(X < y1) = (1/2) * (desired_probability_mass + 1)
    #   2. Use the inverse CDF function to compute y2 such that P(x < y2) = (1/2) * (1 - desired_probability_mass)
    #   3. Compute 2 * x = y1 - y2
    x = norm.ppf(.5 * (desired_probability_mass + 1))

    #
    # Second, figure out how big the interval corresponding to each pixel will be
    # Hint: Assume each pixel corresponds to an interval of equal length, interval_length, and that interval_length * desired_kernel_length = 2 * x
    interval_length = (x * 2)/desired_kernel_length
    #
    # Third, create an array containing the left boundary of every interval and an array containing 
    # the right boundary of every interval
    # Hint: 
    #   1. The left boundary of the first interval is just -x
    #   2. Create a matrix of integers, ints = [0, 1, 2, ..., (desired_kernel_length - 1)], using the arange() function
    #   3. left_boundary_array = -x + interval_length * ints
    #   4. The right boundary of the /last/ interval is just x
    #   5. Reverse the ints array and call it reverse_ints
    #   6. right_boundary_array = x - interval_length * reverse_ints 
    left_boundary_array = empty(desired_kernel_length)
    right_boundary_array = empty(desired_kernel_length)

    for n in range(0, desired_kernel_length):
        left_boundary_array[n] = -x + (n * interval_length)
        right_boundary_array[desired_kernel_length-1-n] = x - (n * interval_length)
    #
    # Fourth, compute the CDF of left_boundary_array and right_boundary_array. The CDF function is designed to 
    # accept ndarrays as arguments, so you can do each array all at once.
    cdf_left_boundary_array = norm.cdf(left_boundary_array)
    cdf_right_boundary_array = norm.cdf(right_boundary_array)
    #
    # Fifth, compute the difference cdf_right_boundary_array - cdf_left_boundary_array. Call it one_d_gaussian_kernel.
    # This is your penultimate result and each entry in this array is the not-normalized weight that will be
    # assigned to the pixels in the neighborhood of the pixel that you are blurring.  Each entry is the 
    # probability associated with the interval corresponding to a given pixel.
    for n in range(0, desired_kernel_length):
        one_d_gaussian_kernel[n] = (cdf_right_boundary_array[n] - cdf_left_boundary_array[n])/(desired_probability_mass)

    #
    # Finally, normalize the result so that sum(one_d_gaussian_kernel) = 1.

    #
    return one_d_gaussian_kernel

def approximate_one_d_gaussian_kernel(desired_kernel_length=5):
    '''Approximate the weights assigned to each pixel in the 1-d Gaussian filter

    Inputs:
         - desired_kernel_length (int): how many pixels do you want to average (must be an odd number to center at the pixel)

    Returns:
        - one_d_gaussian_kernel (ndarray[float]): normalized, i.e., its entries sum to one, kernel of length 'desired_kernel_length'
    '''
    #
    # Initialize
    one_d_gaussian_kernel = (None)
    #
    # Throw an error if the kernel length != 4*n + 1, for some integer n
    if (desired_kernel_length - 1) % 4 != 0: 
        raise Exception("Kernel length must be 4*n + 1, for integer n")
    #
    # Compute the initial convolution size
    d = ((desired_kernel_length - 1) // 4) + 1 # <-- / is normal division. // is 'floor' division or 'integer' division. Returns the closest integer rounded down.
    #
    # Create a 1D box kernel of length d using the ones() function. Call it box_kernel

    box_kernel = ones(d, dtype=float32)

    #
    # Pad box_kernel with d zeroes on either side using the pad() function in 'constant' mode

    pad(box_kernel, d, 'constant')

    #
    # Create a 1D tent kernel by convolving box_kernel with box_kernel (itself), using
    # the convolve() function. Call it tent_kernel

    tent_kernel = convolve(box_kernel, box_kernel)

    #
    # Approximate the Gaussian kernel by convolving tent_kernel with tent_kernel (itself), 
    # using the convolve() function. Assign it to one_d_gaussian_kernel

    one_d_gaussian_kernel = convolve(tent_kernel, tent_kernel)

    #
    # You'll notice that the size of one_d_gaussian_kernel is too big. That's because it
    # has a bunch of zeros on padding its outside. So, figure out the indices where the
    # nonzero entries are.
    # Hint:
    #   1. Get the current length of the kernel: n = len(one_d_gaussian_kernel)
    #   2. Determine the number of zero entries: zed = n - desired_kernel_length
    #   3. Extract the desired kernel, which is in the entries one_d_gaussian_kernel((n//2):(n//2 + desired_kernel_length))
    #   4. Make sure you still assign the extraction to one_d_gaussian_kernel :)
    #
    # Normalize one_d_gaussian_kernel so that sum(one_d_gaussian_kernel) = 1

    n = len(one_d_gaussian_kernel)
    zed = n - desired_kernel_length
    one_d_gaussian_kernel = one_d_gaussian_kernel[(zed//2):(zed//2+desired_kernel_length)]
    norm = sum(one_d_gaussian_kernel)
    for x in range(desired_kernel_length):
        one_d_gaussian_kernel[x] = one_d_gaussian_kernel[x]/norm

    #
    return one_d_gaussian_kernel