from os.path import abspath
from os.path import dirname
from os.path import join


#
# See if you can figure out how to get the
# absolute path to /this/ file first using
# the 'abspath' function. Hint: read up on 
# the __file__ variable
THIS_FILE_PATH = abspath(__file__)
#print(THIS_FILE_PATH)
#
# Using the THIS_FILE_PATH and the 'dirname' function,
# see if you can get the absolute path to the
# directory containing this file.
THIS_DIR_PATH = dirname(THIS_FILE_PATH)
#print(THIS_DIR_PATH)
#
# Using the same idea that you used to create
# THIS_DIR_PATH, it should be easy to get
# the absolute path to the parent directory of
# utils, i.e., whatever ABS_PATH_ROOT in 
# ABS_PATH_ROOT/utils would be
ROOT_DIR_PATH = dirname(THIS_DIR_PATH)
#print(ROOT_DIR_PATH)
#
# Now create a string variable that contains
# the absolute path of the img directory using
# the 'join' function.
IMG_DIR_PATH = join(ROOT_DIR_PATH, "img")