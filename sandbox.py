from utils.image_wrapper import image_wrapper
from filters.gaussian import two_d_gaussian_filter
from numpy import shape

a = image_wrapper("example.png")
b = two_d_gaussian_filter(img_wrapper = a)
b.view()