from skimage.transform import resize
def check_dimension_compatibility(img_as_array, N, dimension):
    return (img_as_array.shape[dimension] % N == 0)

def make_dimensions_compatible(img_as_array, N):
    #
    # Maintain the aspect ratio as best as possible
    img_shape = img_as_array.shape
    aspect_ratio = float(img_shape[1]) / float(img_shape[0])
    #
    # Get new dimensions
    new_d1 = img_shape[0]
    new_d2 = img_shape[1]
    if not check_dimension_compatibility(img_as_array, N, 0):
        new_d1 = img_as_array.shape[0] - (img_as_array.shape[0] % N) + N
        expected_d2 = int(new_d1 * aspect_ratio)
        new_d2 = expected_d2 - (expected_d2 % N) + N
    elif not check_dimension_compatibility(img_as_array, N, 1):
        new_d2 = img_as_array.shape[1] - (img_as_array.shape[1] % N) + N
        expected_d1 = int(new_d2 / aspect_ratio)
        new_d1 = expected_d1 - (expected_d1 % N) + N
    #
    # Determine whether reshaping is needed
    if img_shape[0] != new_d1 or img_shape[1] != new_d2:
        img_as_array = resize(img_as_array, [new_d1, new_d2])
    #
    return img_as_array
