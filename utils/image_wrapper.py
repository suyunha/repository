#from scipy.misc import imread
#from scipy.misc import imsave
#from scipy.misc import imshow
from matplotlib.pyplot import imshow
from matplotlib.pyplot import show
from utils.constants import IMG_DIR_PATH
from os.path import join
from numpy import uint8
from imageio import imread

class image_wrapper(object):
    
    def __init__(self, image_name):
        '''Creates wrapper from the specified image'''
        #
        # Note: in order to access variables that
        # are specific to this instance of an
        # image_wrapper object, you must
        # assign and refer to the variables using
        # the self.VARIABLE_NAME. The same is true if
        # you want to use functions defined /inside/ of
        # the image_wrapper class definition, e.g.:
        self.img = self.load(image_name)
        return

    def load(self, image_name):
        '''
        Loads image data from the img folder using the
        IMG_DIR_PATH defined in utils/constants.py

        Arguments:
            - image_name (str)

        Returns:
            - img_array (ndarray)
        '''
        #
        # Hint: Use the 'imload' function and the
        # python 'open()' function. Read up on the
        # 'open()' function and learn about the different
        # modes ('r', 'w', 'b') in which you can open a 
        # file. 
        # Hint 2: Also, make sure the file closes after you're
        # done loading the image data! Read up on using
        # a 'with:' block in combination with the 'open()'
        # function.
        #
        img_file_name = join(IMG_DIR_PATH, image_name)
        img_array = imread(img_file_name).astype(uint8) # Modify this assignment to return the correct result
        #
        return img_array

    def save(self, image_name):
        '''
        Saves image data to the img folder using the
        IMG_DIR_PATH defined in utils/constants.py

        Arguments:
            - image_name (str)

        Returns:
            - None
        '''
        #
        # Hint: Use the 'imsave' function and the
        # python 'open()' function. Read up on the
        # 'open()' function and learn about the different
        # modes ('r', 'w', 'b') in which you can open a 
        # file. 
        # Hint 2: Also, make sure the file closes after you're
        # done loading the image data! Read up on using
        # a 'with:' block in combination with the 'open()'
        # function.
        # Hint 3: Make sure to use the image data saved inside of
        # the object: self.img
        #imageio.imsave(image_name, self.img)
        return

    def view(self):
        '''Pop up a window with the image in it using the 'show()' function'''
        #
        # Hint: If I remember correctly you will have to
        # (counterintuitively) use both 'imshow()' and 'show()'
        # functions to actually pop up a window with the desired
        # image.
        # Hint 2: Make sure to use the image data saved inside of
        # the object: self.img
        imshow(self.img)
        show()
        return

