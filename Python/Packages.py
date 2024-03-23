import numpy as np
import aicsimageio as Io
import skimage.morphology as skmM
import skimage.filters as skmF
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from skimage import io
import sklearn.cluster as slC
import sklearn.metrics.pairwise as slCM
from scipy.spatial.distance import cdist
import tifffile as tfl
import xlsxwriter as xel
import matplotlib.patches as ptc
import skimage.measure as skM
import skimage.feature as skcanny
import skimage.segmentation as skS
import math as ma
from os import listdir
from os.path import isfile, join
import matplotlib.gridspec as grd
import matplotlib as mpt
from matplotlib import cm
from matplotlib.widgets import Button
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable as ml
import imageio as imgIO
import scipy.stats as stat
import scipy.signal as ssig
from scipy import spatial as spt
import pandas as pd
import sys
import time
from multiprocessing import Pool