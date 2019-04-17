#from scipy.misc import imread
#from scipy.misc import imsave
#from scipy.misc import imshow
from matplotlib.pyplot import imshow
from matplotlib.pyplot import show
from utils.constants import IMG_DIR_PATH
from os.path import join
from numpy import uint8
from imageio import imread
from numpy import empty
from numpy import shape
from numpy import put

class image_wrapper(object):
    
    def __init__(self, image_name=None, image_array=None, padding_size=None):
        '''Creates wrapper from the specified image'''
        #
        # Note: in order to access variables that
        # are specific to this instance of an
        # image_wrapper object, you must
        # assign and refer to the variables using
        # the self.VARIABLE_NAME. The same is true if
        # you want to use functions defined /inside/ of
        # the image_wrapper class definition, e.g.:
        if image_name is not None:
            self.img = self.load(image_name)
        else:
            if image_array is None:
                raise Exception("Must provide either image_name or image_array")
            
            if padding_size is None:
                self.img = image_array
            else:
                self.img = self.extract_from_padding(image_array, padding_size)
            #
        #
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
        #img_array = imread(img_file_name)
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
        #imshow(self.extract_from_padding(image_array = self.get_padded_image(padding_size=20), padding_size = 20))
        show()
        return

    def extract_from_padding(self, image_array, padding_size):
        '''Return an the part of the image array that is not padding.'''
        #extracted_image_array = None
        #
        # I'll let you figure this one out by yourself. :)
        size = image_array.shape
        print(size)
        extracted_image_array = empty([size[0]-2*padding_size, size[1]-2*padding_size, size[2]], dtype = uint8)
        
        for z in range(size[2]):
            for y in range(size[1]-2*padding_size):
                for x in range(size[0]-2*padding_size):
                    extracted_image_array[x, y, z] = image_array[x+padding_size-1, y+padding_size-1, z]


        #
        return extracted_image_array

    def get_padded_image(self, padding_size=None):
        '''Return the wrapper's image with padding added.'''
        #padded_image = None
        #
        # I'll let you figure this one out by yourself. :)
        size = self.img.shape
        padded_image = empty([size[0]+2*padding_size, size[1]+2*padding_size, size[2]], dtype = uint8)
        copypos = [0, 0, 0]

        #rewrite this eventually maybe

        for z in range(size[2]):
            copypos[2] = z
            for y in range(size[1] + 2*padding_size):
                if (y<padding_size):
                    copypos[1] = padding_size - y
                elif (y>=padding_size+size[1]):
                    copypos[1] = size[1] - 1 - (y-size[1]-padding_size)
                else:
                    copypos[1] = y - padding_size
                for x in range(size[0] + 2*padding_size):
                    if (x<padding_size):
                        copypos[0] = padding_size - x
                    elif (x>=padding_size+size[0]):
                        copypos[0] = size[0] - 1 - (x-size[0]-padding_size)
                    else:
                        copypos[0] = x - padding_size
                    padded_image[x, y, z] = self.img[copypos[0], copypos[1], copypos[2]]

        return padded_image

    def resize_image_for_watermarking(self, transform_size):
        """
        Must be a multiple of N in both length and width, where N = transform_size
        """

        return

    
