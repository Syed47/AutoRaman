import numpy as np
import imagej, scyjava
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pycromanager import  Acquisition, Core, Studio, multi_d_acquisition_events
from tifffile import imsave

# %%
ij = imagej.init('C:\\Users\\19719431\\Fiji.app')
ij.ui().showUI() # if you want to display the GUI immediately
