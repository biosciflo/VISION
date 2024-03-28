"""
Created on Wed Oct 19 12:39:12 2022

@author: P41650
"""

#performance
import copy
#import pyi_splash

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


#ForGUI
from PyQt5 import uic, QtCore, QtWidgets,QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QGuiApplication
import sys

#for equation checks
from sympy import sympify
from sympy.core.sympify import SympifyError


#ForPLots
from PyQt5.QtWidgets import QWidget, QVBoxLayout,QTableWidgetItem
from matplotlib.ticker import FixedLocator
from matplotlib.widgets import RectangleSelector


#from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

import numpy as np
import seaborn as sns
import seaborn_image as isns
import pandas as pd
import json

#For Splashscreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen

import time

#ForOpenDirectory
from PyQt5.QtWidgets import  QFileDialog,QMessageBox

from os import listdir,getcwd
from os.path import isfile, join, basename,dirname
from PyQt5.QtCore import Qt



#GP Analyser
import Analyzer_V1_0_0 as analyzer


#OpenFormat

import xmltodict


import tifffile as lsm
import czifile
from readlif.reader import LifFile
import obf_support


#for Erroe handling
import traceback


##segment color map:
from matplotlib.colors import ListedColormap
num_unique_colors = 8
accent_r_palette = sns.color_palette("Accent_r", num_unique_colors)

# Assuming your segment numbers are integers starting from 1
segment_numbers = list(range(1, num_unique_colors + 1))

# Create a color map: a dictionary mapping segment numbers to colors
color_map = {segment_number: color for segment_number, color in zip(segment_numbers, accent_r_palette)}



#varlist = [ 'NaN', 'NaN', 'NaN', 'NaN']
def apply_dark_palette(app):
    app.setStyle("Fusion")  # Optional: Set Fusion style for a more modern look
    dark_palette = QtGui.QPalette()
    
    # Adjust palette colors for dark mode
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.int32):
            return int(obj)  # Convert int32 to regular int
        elif isinstance(obj, np.int64):
            return int(obj)  # Convert int64 to regular int
        return json.JSONEncoder.default(self, obj)


class WorkerThread(QThread):
    finished = pyqtSignal()
    terminate_thread = pyqtSignal()

    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        try:
            print("Thread run start")
            self.window.Run()
            print("Thread run end")
            self.finished.emit()
            print("Thread finished emitted")
        except Exception as e:
            error_trace = traceback.format_exc() 
            print(f"Error: An exception occurred in run: In Line {error_trace}: {e}")
            if getattr(sys, 'frozen', False):
                # For standalone executables
                current_directory =dirname(sys.executable)
            else:
                # For running as a script
#                 current_directory = dirname(abspath(__file__))
                # or 
                current_directory = getcwd()
            error_log_path = join(current_directory, 'error_log.txt')
            with open(error_log_path, 'w') as f:
                f.write(time.asctime(time.localtime()))
                f.write(f"Error message: {e}\n")
                f.write(f"In Run Traceback:\n{error_trace}")
            self.window.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.window.plainTextEdit_1.appendPlainText(f"Error: An exception occurred in RunAnalysis: \n In Run Traceback:\n{error_trace}")
            self.terminate_thread.emit()
        
    def testthresholding(self): #SavingThread
        try:
            self.window.testThresholding()
            self.finished.emit()
        except Exception as e:
            error_trace = traceback.format_exc() 
            print(f"Error: An exception occurred in run: In Line {error_trace}: {e}")
            if getattr(sys, 'frozen', False):
                # For standalone executables
                current_directory =dirname(sys.executable)
            else:
                # For running as a script
#                 current_directory = dirname(abspath(__file__))
                # or 
                current_directory = getcwd()
            error_log_path = join(current_directory, 'error_log.txt')
            with open(error_log_path, 'w') as f:
                f.write(f"Error message: {e}\n")
                f.write(f"In Run Traceback:\n{error_trace}")
            print(f"Error: An exception occurred in TestThreshold: {e}")
            self.window.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.window.plainTextEdit_1.appendPlainText(f"Error: An exception occurred in TestThreshold: \nIn Run Traceback:\n{error_trace}")
            self.terminate_thread.emit()
            
    def SavingThread(self): #SavingThread
        try:
            self.window.Data_Saving()
            self.finished.emit()
        except Exception as e:
            print(f"Error: An exception occurred in DataSaving: {e}")
            self.window.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.window.plainTextEdit_1.appendPlainText(f"Error: An exception occurred in DataSaving: {e}")
            self.terminate_thread.emit()


def RunAnalyser(mode, filename, Lambdachannel,
                image, dims, varlist,
                ObjectDetection, profiler,profilershape,
                autoff, PDiamCutoff, proDim1,
                proDim2, text, histpars,
                histpars_cyto,text_cyto, profile_cyto,
                varlist_cyto, n_debranch, tol0,
                tol1,savecroppedmembrane, savecroppedcyto,
                savelinearized, savepath, objlinear,
                recentering, dim_line,
                MaskParams_mem, MaskParams_cyto,
                Colocalization, savephasors,
                tocut =0,radius = 'auto'):
    if tocut == 0:
        radius = 'auto'
    else:
        radius = tocut
    if varlist[0] == 'NaN':
        return 0
    else:
        return analyzer.GP_Analyser(mode, filename, Lambdachannel,
                        image, dims, varlist,
                        ObjectDetection, profiler,profilershape,
                        autoff, PDiamCutoff, proDim1,
                        proDim2, text, histpars,
                        histpars_cyto,text_cyto, profile_cyto,
                        varlist_cyto, n_debranch, tol0,
                        tol1,savecroppedmembrane, savecroppedcyto,
                        savelinearized, savepath, objlinear,
                        recentering, dim_line,
                        MaskParams_mem, MaskParams_cyto, # NEW
                        Colocalization, savephasors,
                        radius)



def load_and_process_czi(fullpath):
#for spectral ana multi chanell
    metadata = {
        "Pixelsize": None,
        "Nchannels": None,
        "ChannelColors": [],
        "Dimensions": None,
        "BitDepth": None
        }
    DimensionTime = DimensionZ = DimensionX = DimensionY = DimensionChannels = 1
    with czifile.CziFile(fullpath) as czi:
        czi_metadata = xmltodict.parse(czi.metadata())
        
        metadata['Pixelsize']=float(czi_metadata["ImageDocument"]["Metadata"]["Scaling"]["Items"]["Distance"][0].get("Value", 1))
        DimensionChannels=int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("SizeC", 1))
        metadata['Nchannels']=DimensionChannels
        DimensionTime = int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("SizeT", 1))
        DimensionZ = int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("SizeZ", 1))
        DimensionX = int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("SizeX", 1))
        DimensionY = int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("SizeY", 1))
        metadata['BitDepth']=int(czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"].get("ComponentBitCount", 1))
        metadata['Dimensions'] = [DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]
        for subdict in czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]:
            if subdict ["@Name"].isdigit():
                metadata['ChannelColors'].append(int(subdict["@Name"]))
            else:
                metadata['ChannelColors'].append(int(float(subdict["EmissionWavelength"])))
        
        metadata['ChannelColors']=np.array(metadata['ChannelColors'])

    data = np.squeeze(np.transpose(czifile.imread(fullpath)[0, 0, :, :, :, :, :, 0], (1, 2, 3, 4, 0)))
    
    return data, metadata


def load_and_process_lsm(fullpath):
#for spectral ana multi chanell
    metadata = {
    "Pixelsize": None,
    "Nchannels": None,
    "ChannelColors": None,
    "Dimensions": None,
    "BitDepth": None
    }
    DimensionTime = DimensionZ = DimensionX = DimensionY = DimensionChannels = 1
    
    with lsm.TiffFile(fullpath) as tif:
        if hasattr(tif, 'lsm_metadata'):
            lsm_metadata = tif.lsm_metadata
    
        metadata['Pixelsize'] = lsm_metadata.get("VoxelSizeX", None)
        DimensionChannels = lsm_metadata.get("DimensionChannels", 1)
        metadata['Nchannels'] = DimensionChannels
        
        if "ChannelColors" in lsm_metadata and all(item.isdigit() for item in lsm_metadata["ChannelColors"]["ColorNames"]):
            metadata['ChannelColors'] = np.array([int(float(item)) for item in lsm_metadata["ChannelColors"]["ColorNames"]])
        else:
            metadata['ChannelColors'] = ((np.mean(lsm_metadata["ChannelWavelength"] , axis=1))*1e9).astype(int)
        
        DimensionTime = lsm_metadata.get("DimensionTime", 1)
        DimensionZ = lsm_metadata.get("DimensionZ", 1)
        DimensionX = lsm_metadata.get("DimensionX", 1)
        DimensionY = lsm_metadata.get("DimensionY", 1)
        
        metadata['Dimensions'] = [DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]
        
        data = lsm.imread(fullpath)
        
        if data.dtype == np.uint16:
            metadata['BitDepth']=16
        elif data.dtype == np.uint8:
            metadata['BitDepth']=8
        
        if metadata['Nchannels'] >1:
            if data.ndim == 3:
                data = np.transpose(data, (1, 2, 0))
            elif data.ndim == 4:
                data = np.transpose(data, (0, 2, 3, 1))
            elif data.ndim == 5:
                data = np.transpose(data, (0, 1, 3, 4, 2))
        else:
            data = np.expand_dims(data, axis=-1)

    return data, metadata

def load_and_process_lif(fullpath):
    metadata={}
    data={}
    lif = LifFile(fullpath)
    xml=xmltodict.parse(lif.xml_header)
    images = lif.image_list
    i=0
    for image in images:
        
        metadata[i] = {
        "Pixelsize": [],
        "Nchannels": [],
        "ChannelColors": [],
        "Dimensions": [],
        "BitDepth": []
        }
        channel_data=[]
        
        nthimage=lif.get_image(i)
        metadata[i]['Pixelsize'] = image["scale"][0]
        metadata[i]['Nchannels'] = image["channels"]
        DimensionChannels=nthimage.channels
        if  metadata[i]['Nchannels'] > 1:
            for n in range(metadata[i]['Nchannels']):
                metadata[i]['ChannelColors'].append(xml["LMSDataContainerHeader"]["Element"]["Children"]["Element"][i]["Data"]["Image"]["ImageDescription"]["Channels"]["ChannelDescription"][n]["@LUTName"])
                frame_data = np.array(nthimage.get_frame(c=n))
                channel_data.append(frame_data)
                data[i]=np.stack(channel_data, axis=-1)
                
                
        else:
            metadata[i]['Nchannels'] = image["dims_n"][5]
            DimensionChannels=image["dims_n"][5]
            for n in range(DimensionChannels):
                metadata[i]['ChannelColors'].append(n+1)
                frame_data = np.array(nthimage.get_plane((1, 2),n))
                channel_data.append(frame_data)
                data[i]=np.stack(channel_data, axis=-1)
    
        metadata[i]['BitDepth'] = image["bit_depth"][0]
        
        DimensionTime = nthimage.dims.t
        DimensionZ = nthimage.dims.z
        DimensionX = nthimage.dims.x
        DimensionY = nthimage.dims.y
        
        metadata[i]['ChannelColors']=np.array(metadata[i]['ChannelColors'])
        metadata[i]['Dimensions']=[DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]

        i+=1
    return data,metadata

def load_and_process_obf(fullpath):
    # Load an image file
    obf = obf_support.File(fullpath)
    xml=xmltodict.parse(obf.meta["ome_xml"])
    
    
    metadata={}
    data={}
    
    for i, stack in enumerate(obf.stacks[:]):
        metadata[i] = {
        "name":[],
        "Pixelsize": [],
        "Nchannels": [],
        "ChannelColors": [],
        "Dimensions": [],
        "BitDepth": [],
        }
        metadata[i]['name'] = xml["OME"]["Image"][i]["@Name"]
        metadata[i]['Pixelsize'] = float(xml["OME"]["Image"][i]["Pixels"]["@PhysicalSizeX"])
        metadata[i]['Nchannels'] = int(xml["OME"]["Image"][i]["Pixels"]["@SizeC"])
        
        metadata[i]['ChannelColors'] = int(float(xml["OME"]["Image"][i]["Pixels"]["Channel"]["@EmissionWavelength"]))
        
        DimensionChannels=int(xml["OME"]["Image"][i]["Pixels"]["@SizeC"])
        DimensionTime = int(xml["OME"]["Image"][i]["Pixels"]["@SizeT"])
        DimensionZ = int(xml["OME"]["Image"][i]["Pixels"]["@SizeZ"])
        DimensionX = int(xml["OME"]["Image"][i]["Pixels"]["@SizeX"])
        DimensionY = int(xml["OME"]["Image"][i]["Pixels"]["@SizeY"])
        
        metadata[i]['Dimensions']=[DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]
        
        metadata[i]['BitDepth'] = xml["OME"]["Image"][i]["Pixels"]["@Type"]
        digits = [char for char in metadata[i]['BitDepth'] if char.isdigit()]
        metadata[i]['BitDepth'] = int(''.join(digits))
        
        stack_data=[]
        stack_data.append(stack.data)
        data[i]=np.squeeze(np.stack(stack_data, axis=-1))
    
    return data,metadata

def load_and_process_ometiff(fullpath):
    metadata = {
        "Pixelsize": None,
        "Nchannels": None,
        "ChannelColors": [],
        "Dimensions": None,
        "BitDepth": None,
        "PixelsizeUnit": None
        }
    DimensionTime = DimensionZ = DimensionX = DimensionY = DimensionChannels = 1
    with lsm.TiffFile(fullpath) as tif:
        if hasattr(tif, 'ome_metadata') and tif.ome_metadata:
            ometiff_metadata = xmltodict.parse(tif.ome_metadata)
            metadata['Pixelsize'] = float(ometiff_metadata["OME"]["Image"]["Pixels"]["@PhysicalSizeX"])
            metadata['Nchannels'] = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeC"])
            i=1
            if metadata['Nchannels']>1:
                for channels in ometiff_metadata["OME"]["Image"]["Pixels"]["Channel"]:
                    if "@Name" in channels:
                        if channels["@Name"].isdigit():
                            metadata['ChannelColors'].append(int(channels["@Name"]))
                            i+=1
                        else:
                            metadata['ChannelColors'].append(int(i))
                            i+=1
                    else:
                        metadata['ChannelColors'].append(int(i))
                        i+=1
            else:
                metadata['ChannelColors'].append(int(i))
                
            metadata['ChannelColors']=np.array(metadata['ChannelColors'])
            
            DimensionChannels=int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeC"])
            DimensionTime = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeT"])
            DimensionZ = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeZ"])
            DimensionX = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeX"])
            DimensionY = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeY"])
            
            metadata['Dimensions']=[DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]
            
            metadata['BitDepth'] = ometiff_metadata["OME"]["Image"]["Pixels"]["@Type"]
            digits = [char for char in metadata['BitDepth'] if char.isdigit()]
            metadata['BitDepth'] = int(''.join(digits))
            metadata['PixelsizeUnit'] = ometiff_metadata["OME"]["Image"]["Pixels"]["@PhysicalSizeZUnit"]
            
            data = tif.asarray()
            
            
            if metadata['Nchannels'] >1:
                if data.ndim == 3:
                    data = np.transpose(data, (1, 2, 0))
                elif data.ndim == 4:
                    data = np.transpose(data, (0, 2, 3, 1))
                elif data.ndim == 5:
                    data = np.transpose(data, (0, 1, 3, 4, 2))
            else:
                data = np.expand_dims(data, axis=-1)
                
    return data,metadata

def openfile(fullfilepath):
    
    if fullfilepath.endswith(('.lsm')):
        data,metadata=load_and_process_lsm(fullfilepath)
        return data, metadata
    elif fullfilepath.endswith(('.czi')):
        data,metadata=load_and_process_czi(fullfilepath)
        return data, metadata
    elif fullfilepath.endswith(('.lif')):
        data,metadata=load_and_process_lif(fullfilepath)
        return data, metadata
    elif fullfilepath.endswith(('.obf')):
        data,metadata=load_and_process_obf(fullfilepath)
        return data, metadata
    elif fullfilepath.endswith(('.ome.tif')):
        data,metadata=load_and_process_ometiff(fullfilepath)
        return data, metadata
    else:
        print("Only .lsm, .czi, & .ome.tif !!! Your filefomate is currently not supported. Pls send us a test image and we will gladly incorporte it (.lif and .obf are prepeared but I had no test images so pls send me some and I can implement it")
        
class Splashscreen(QSplashScreen):
        def __init__(self):
            super(QSplashScreen,self).__init__()
#             self.UI_FILE_SPLASH = str(Path(__file__).parent / "splash.ui")
#             uic.loadUi(self.UI_FILE_SPLASH, self)  
#             ui_file = join(dirname(sys.argv[0]), "ui/splash.ui") # for python
            ui_file = join(getattr(sys, '_MEIPASS', dirname(sys.argv[0])), "ui/splash.ui") # Standalone
            uic.loadUi(ui_file,self)
            self.setWindowFlag(Qt.FramelessWindowHint)
            pixmap = QPixmap("ui/splashscreen.png")
            self.setPixmap(pixmap)
            
        def progress(self,n):
            for i in range(n):
                time.sleep(0.1)

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget,self).__init__(parent)
        self.figure = Figure(facecolor='#434343')  # Set figure background color
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_facecolor('#2D2D2D')  # Set axes background color
        self.figure.tight_layout()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.toolbar)
        self.layoutvertical.addWidget(self.canvas)
        self.layoutvertical.setContentsMargins(0, 0, 0, 0)
        self.layoutvertical.setSpacing(0)

class MatplotlibWidgetPolar(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidgetPolar,self).__init__(parent)
        self.figure = Figure(facecolor='#434343')  # Set figure background color
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111,projection='polar')
        self.axis.set_facecolor('#2D2D2D')  # Set axes background color
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.toolbar)
        self.layoutvertical.addWidget(self.canvas)
        self.layoutvertical.setContentsMargins(0, 0, 0, 0)
        self.layoutvertical.setSpacing(0)    
        
def px_to_dp(pixels):
    return int(pixels * QGuiApplication.primaryScreen().physicalDotsPerInch() / 96)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_file = join(getattr(sys, '_MEIPASS', dirname(sys.argv[0])), "ui/gui_V1.0.0.ui")  # Standalone
        self.ui = uic.loadUi(ui_file, self)

    # Convert sizes to dp - example for a label
        if hasattr(self, 'label'):  # Check if the label exists
            label_width_dp = px_to_dp(self.label.width())
            self.label.setFixedWidth(label_width_dp)

        # Wrap existing central widget with QScrollArea
        self.wrapCentralWidgetWithScrollArea()
                

        # Set window size in dp
        self.resize(px_to_dp(self.width()), px_to_dp(self.height()))

        #for matplotlib widget1 Rawfile
        self.matplotlibwidget = MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget)
        self.layoutvertical.addWidget(self.matplotlibwidget)
        #self.pushButton.clicked.connect(self.plot_widget)
        
        #for matplotlib widget2 Mask
        self.matplotlibwidget_2 = MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_2)
        self.layoutvertical.addWidget(self.matplotlibwidget_2)
        
        #for matplotlib widget3 GP image
        self.matplotlibwidget_3 = MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_3)
        self.layoutvertical.addWidget(self.matplotlibwidget_3)
        
        #for matplotlib widget4 GP Histogramm 
        self.matplotlibwidget_4= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_4)
        self.layoutvertical.addWidget(self.matplotlibwidget_4)
        
        
        #for matplotlib widget5 Object overview
        self.matplotlibwidget_5= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_5)
        self.layoutvertical.addWidget(self.matplotlibwidget_5)
        
        #for matplotlib widget6 Phasor plot GP
        self.matplotlibwidget_6= MatplotlibWidgetPolar()
        self.layoutvertical = QVBoxLayout(self.MplWidget_6)
        self.layoutvertical.addWidget(self.matplotlibwidget_6)
        
        #for matplotlib widget7 hist intensities
        self.matplotlibwidget_7= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_7)
        self.layoutvertical.addWidget(self.matplotlibwidget_7)
        
        #for matplotlib widget8 zoom in of Object
        self.matplotlibwidget_8= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_8)
        self.layoutvertical.addWidget(self.matplotlibwidget_8)
        
        #for matplotlib widget9 hist GP of Object
        self.matplotlibwidget_9= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_9)
        self.layoutvertical.addWidget(self.matplotlibwidget_9)
        
        #for matplotlib widget10 hist intensities of object
        self.matplotlibwidget_10= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_10)
        self.layoutvertical.addWidget(self.matplotlibwidget_10)
        
        #for matplotlib widget11 Phasor plot GP of object
        self.matplotlibwidget_11= MatplotlibWidgetPolar()
        self.layoutvertical = QVBoxLayout(self.MplWidget_11)
        self.layoutvertical.addWidget(self.matplotlibwidget_11)

        #for matplotlib widget12 Phasor plot GP of object
        self.matplotlibwidget_12= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_12)
        self.layoutvertical.addWidget(self.matplotlibwidget_12)


        #for matplotlib widget13 cytoprifer object plot GP of object
        self.matplotlibwidget_13= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_13)
        self.layoutvertical.addWidget(self.matplotlibwidget_13)

        #for matplotlib widget14 cytoprifer object plot GP of object
        self.matplotlibwidget_14= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_14)
        self.layoutvertical.addWidget(self.matplotlibwidget_14)
        
        #for matplotlib widget17 hist GP of Object
        self.matplotlibwidget_17= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_17)
        self.layoutvertical.addWidget(self.matplotlibwidget_17)
        
        #for matplotlib widget15 hist intensities of object
        self.matplotlibwidget_15= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_15)
        self.layoutvertical.addWidget(self.matplotlibwidget_15)
        
        #for matplotlib widget16 Phasor plot GP of object
        self.matplotlibwidget_16= MatplotlibWidgetPolar()
        self.layoutvertical = QVBoxLayout(self.MplWidget_16)
        self.layoutvertical.addWidget(self.matplotlibwidget_16)
        
        #for matplotlib widget18 Cytosol Mask 
        self.matplotlibwidget_18= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_18)
        self.layoutvertical.addWidget(self.matplotlibwidget_18)
        
        #for matplotlib widget19 Cytosol Whole Image
        self.matplotlibwidget_19= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_19)
        self.layoutvertical.addWidget(self.matplotlibwidget_19)
        
        #for matplotlib MplWidget_20 Cytosol histogramme Image
        self.matplotlibwidget_20= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_20)
        self.layoutvertical.addWidget(self.matplotlibwidget_20)
        
        #for matplotlib MplWidget_21 Cytosol intensities Image
        self.matplotlibwidget_21= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_21)
        self.layoutvertical.addWidget(self.matplotlibwidget_21)
        
        #for matplotlib MplWidget_22 Cytosol polar Image
        self.matplotlibwidget_22= MatplotlibWidgetPolar()
        self.layoutvertical = QVBoxLayout(self.MplWidget_22)
        self.layoutvertical.addWidget(self.matplotlibwidget_22)
        
        #for matplotlib MplWidget_23 Cytosol object overview image
        self.matplotlibwidget_23= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_23)
        self.layoutvertical.addWidget(self.matplotlibwidget_23)
        
        #for matplotlib MplWidget_24 Membrane Segment 
        self.matplotlibwidget_24= MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.MplWidget_24)
        self.layoutvertical.addWidget(self.matplotlibwidget_24)

        #Settings
        self.B_LoadFiles.clicked.connect(self.LoadFiles) #(self.tranPath)
        self.B_LoadFolder.clicked.connect(self.LoadFolder) #(self.tranPath)
        
        self.B_ClearTable.clicked.connect(self.ClearTable) #(self.tranPath)
        self.B_DeletEntry.clicked.connect(self.DeletEntry) #(self.tranPath)
        self.B_ClearSelection.clicked.connect(self.ClearSelection)
        

        
        self.pushButton_3.clicked.connect(self.start_worker_thread_2)

        
        self.checkBox_2.stateChanged.connect(self.objectDetectionEnable)
        self.checkBox_4.stateChanged.connect(self.removeObjectsEnable)
        self.checkBox_5.stateChanged.connect(self.fillHolesEnable)
        self.checkBox_6.stateChanged.connect(self.dilateEnable)
        self.checkBox_3.stateChanged.connect(self.compressEnable)
        self.checkBox_8.stateChanged.connect(self.profilerEnable)
        self.checkBox_9.stateChanged.connect(self.autoCutOffEnable)
        self.checkBox_14.stateChanged.connect(self.toggle_Colocalization)
        self.checkBox_31.stateChanged.connect(self.toggle_Detailed_cyto)
        self.checkBox_24.stateChanged.connect(self.toggle_Detailed_membrane)
        
        self.comboBox_3.currentIndexChanged.connect(self.threholdEnable)
        self.comboBox_21.currentIndexChanged.connect(self.threholdEnable_cyto)
        self.checkBox.stateChanged.connect(self.cytoprofilerEnable)
        self.checkBox_34.stateChanged.connect(self.removeObjectsEnable_cyto)
        self.checkBox_35.stateChanged.connect(self.fillHolesEnable_cyto)
        self.checkBox_37.stateChanged.connect(self.dilateEnable_cyto)
        self.checkBox_32.stateChanged.connect(self.compressEnable_cyto)
        
        self.checkBox_27.stateChanged.connect(self.threholdChannelEnable)
        self.checkBox_36.stateChanged.connect(self.threholdChannelEnable_cyto)
        self.checkBox_26.stateChanged.connect(self.gaussEnable)
        self.checkBox_33.stateChanged.connect(self.gaussEnable_cyto)
        self.checkBox_16.stateChanged.connect(self.toggle_background_std_cyto)
        self.checkBox_15.stateChanged.connect(self.toggle_background_std_membrane)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,1100-250)
        
        self.checkBox_18.stateChanged.connect(self.toggleSaveJSONResults)
        self.checkBox_19.stateChanged.connect(self.JSONResultsWarning)
        
        self.tableWidget.itemSelectionChanged.connect(self.updatePlots)

        
        
        self.verticalScrollBar.valueChanged.connect(self.updatePlots)
        self.verticalScrollBar_2.valueChanged.connect(self.updatePlots)
        self.verticalScrollBar_3.valueChanged.connect(self.updatePlots)
        
        self.horizontalScrollBar.valueChanged.connect(self.updatePlots)
        self.horizontalScrollBar_2.valueChanged.connect(self.updatePlots)
        self.horizontalScrollBar_3.valueChanged.connect(self.updatePlots)
        self.horizontalScrollBar_4.valueChanged.connect(self.updatePlots)
        self.horizontalScrollBar_5.valueChanged.connect(self.updatePlots)
        
        self.tableWidget_2.itemClicked.connect(self.updatePlots_Objects)
        self.tableWidget.itemSelectionChanged.connect(self.updatePlots_Objects)
        
        self.verticalScrollBar.valueChanged.connect(self.updatePlots_Objects)
        self.verticalScrollBar_2.valueChanged.connect(self.updatePlots_Objects)
        self.verticalScrollBar_3.valueChanged.connect(self.updatePlots_Objects)
        
        self.horizontalScrollBar.valueChanged.connect(self.updatePlots_Objects)
        self.horizontalScrollBar_2.valueChanged.connect(self.updatePlots_Objects)
        self.horizontalScrollBar_3.valueChanged.connect(self.updatePlots_Objects)
        self.horizontalScrollBar_4.valueChanged.connect(self.updatePlots_Objects)
        self.horizontalScrollBar_5.valueChanged.connect(self.updatePlots_Objects)
        
        self.horizontalScrollBar_4.valueChanged.connect(self.updateLambda_1)
        self.horizontalScrollBar_5.valueChanged.connect(self.updateLambda_2)
        
        #DetailedMasking_Setting
        self.tableWidget.itemSelectionChanged.connect(self.Update_Detailed_Membrane_Masking_Setting)
        self.tableWidget.itemSelectionChanged.connect(self.Update_Detailed_Cytosol_Masking_Setting)
        self.comboBox_17.activated.connect(self.Update_formZ_Detailed_Membrane_Masking_Setting)
        self.comboBox_24.activated.connect(self.Update_formZ_Detailed_Cytosol_Masking_Setting)
        self.tableWidget_3.itemChanged.connect(self.Detailed_Membrane_Masking_onItemChanged)
        self.tableWidget_6.itemChanged.connect(self.Detailed_Cytosol_Masking_onItemChanged)
        self.pushButton_6.clicked.connect(self.helper_for_button_updater)
        self.pushButton_7.clicked.connect(self.helper2_for_button_updater)
        
        self.pushButton_2.clicked.connect(self.activate_rectangle_selector)
        
        
        self.progressBar_1.setVisible(False)
        self.label_10.setVisible(False)
        
        self.plainTextEdit_1.setReadOnly(True)
        
        self.tabWidget_2.currentChanged.connect(self.updatePlots)
        
        
        self.pushButton.clicked.connect(self.test)
        self.pushButton.setVisible(False)
        
        self.B_selectsavingpath.clicked.connect(self.Select_Saving_Path)
        
        
        self.BLUB=True
        
        
        self.B_Run.clicked.connect(self.start_worker_thread)
        

        
        
        self.tabWidget.setCurrentIndex(0) 
        
        self.Results={}
        self.Membrane_Maskdata={}
        self.Cyto_Maskdata={}
        self.previously_selected_file=[None]
        self.dims={}
        self.RawImages={}
        self.Metadata={}
        self.GPImage={}
        self.FullImage_Parameters={}
        self.Cyto_GPImage={}
        self.GPImage_per_object={}  
        self.GPPhasor={}     
        self.Cyto_GPPhasor={}     
        self.Masks={}
        self.Cyto_Masks={}
        self.Intensities={}
        self.Cyto_Intensities={}
        self.nobjects={}
        self.Object_Parameters={}
        self.Object_Morphology={}
        self.Object_Coordinates={}
        self.Mask_Object_Coordinates={}
        self.Intensities_per_object={}
        self.Channellamda={}
        self.phasex_object={}
        self.phasey_object={}
        self.GPPhasor_polar_all={}
        self.Cyto_GPPhasor_polar_all={}
        self.GPPhasor_polar_obj={}
        self.key={}
        self.ConnectSliders={}
        self.Profile={}
        self.MembraneSegments={}
        self.Cytoprof={}
        self.Cyto_Image={}
        self.FullImage_Parameters_cyto={}
        self.Object_Parameters_cyto={}
        self.Cyto_Intensities_per_object={}
        self.Cyto_GPPhasor_polar_obj={}
        self.savingpath=str([])
        self.DifferentSavingPath=str([])


#### for testing purposes
        global Results_g
        global Membrane_Maskdata_g
        global Cyto_Maskdata_g
        global previously_selected_file_g
        global dims_g
        global RawImages_g
        global Metadata_g
        global GPImage_g
        global FullImage_Parameters_g
        global Cyto_GPImage_g
        global GPImage_per_object_g
        global GPPhasor_g
        global Masks_g
        global Intensities_g
        global Cyto_Intensities_g
        global nobjects_g
        global Object_Parameters_g
        global Object_Morphology_g
        global Object_Coordinates_g
        global Mask_Object_Coordinates_g
        global Intensities_per_object_g
        global Channellamda_g
        global phasex_object_g
        global phasey_object_g
        global GPPhasor_polar_all_g
        global Cyto_GPPhasor_polar_all_g
        global GPPhasor_polar_obj_g
        global key_g
        global ConnectSliders_g
        global Profile_g
        global MembraneSegments_g
        global Cytoprof_g
        global Cyto_Image_g
        global FullImage_Parameters_cyto_g
        global Object_Parameters_cyto_g
        global Cyto_Intensities_per_object_g
        global Cyto_GPPhasor_polar_obj_g
        global savingpath_g

        
    def test(self):
        res=1/0
        global Results_g
        Results_g = self.Results
        global Membrane_Maskdata_g
        Membrane_Maskdata_g = self.Membrane_Maskdata
        global Cyto_Maskdata_g
        Cyto_Maskdata_g = self.Cyto_Maskdata
        global previously_selected_file_g
        previously_selected_file_g = self.previously_selected_file
        global dims_g
        dims_g = self.dims
        global RawImages_g
        RawImages_g = self.RawImages
        global Metadata_g
        Metadata_g = self.Metadata
        global GPImage_g
        GPImage_g = self.GPImage
        global FullImage_Parameters_g
        FullImage_Parameters_g = self.FullImage_Parameters
        global Cyto_GPImage_g
        Cyto_GPImage_g = self.Cyto_GPImage
        global GPImage_per_object_g
        GPImage_per_object_g = self.GPImage_per_object
        global Cyto_GPPhasor_polar_all_g
        Cyto_GPPhasor_polar_all_g = self.Cyto_GPPhasor_polar_all
        global Cyto_GPPhasor_g
        Cyto_GPPhasor_g = self.Cyto_GPPhasor
        global Masks_g
        Masks_g = self.Masks
        global Cyto_Masks_g
        Cyto_Masks_g = self.Cyto_Masks
        global Intensities_g
        Intensities_g = self.Intensities
        global Cyto_Intensities_g
        Cyto_Intensities_g = self.Cyto_Intensities
        global nobjects_g
        nobjects_g = self.nobjects
        global Object_Parameters_g
        Object_Parameters_g = self.Object_Parameters
        global Object_Morphology_g
        Object_Morphology_g = self.Object_Morphology
        global Object_Coordinates_g
        Object_Coordinates_g = self.Object_Coordinates
        global Mask_Object_Coordinates_g
        Mask_Object_Coordinates_g = self.Mask_Object_Coordinates
        global Intensities_per_object_g
        Intensities_per_object_g = self.Intensities_per_object
        global Channellamda_g
        Channellamda_g = self.Channellamda
        global phasex_object_g
        phasex_object_g = self.phasex_object
        global phasey_object_g
        phasey_object_g = self.phasey_object
        global GPPhasor_polar_all_g
        GPPhasor_polar_all_g = self.GPPhasor_polar_all
        global GPPhasor_polar_obj_g
        GPPhasor_polar_obj_g = self.GPPhasor_polar_obj
        global key_g
        key_g = self.key
        global ConnectSliders_g
        ConnectSliders_g = self.ConnectSliders
        global Profile_g
        Profile_g = self.Profile
        global MembraneSegments_g
        MembraneSegments_g = self.MembraneSegments
        global Cytoprof_g
        Cytoprof_g = self.Cytoprof
        global Cyto_Image_g
        Cyto_Image_g = self.Cyto_Image
        global Object_Parameters_cyto_g
        Object_Parameters_cyto_g = self.Object_Parameters_cyto
        global FullImage_Parameters_cyto_g
        FullImage_Parameters_cyto_g = self.FullImage_Parameters_cyto
        global Cyto_Intensities_per_object_g
        Cyto_Intensities_per_object_g = self.Cyto_Intensities_per_object
        global Cyto_GPPhasor_polar_obj_g
        Cyto_GPPhasor_polar_obj_g = self.Cyto_GPPhasor_polar_obj
        global savingpath_g
        savingpath_g = self.savingpath
    
    def toggle_Colocalization(self):
        self.comboBox_8.setEnabled(self.checkBox_14.checkState())
    
    def toggleSaveJSONResults(self):
        self.checkBox_19.setEnabled(self.checkBox_18.checkState())
    
    def JSONResultsWarning(self):
        if self.checkBox_19.checkState():
            QMessageBox.warning(self, 'Warning', 'Enabling this option can significantly slow down performance. Additionally, please be aware that the file size will be considerably larger compared to the original image. It is not recommended to use this for batch processing; instead, it is best suited for single images.')
    
    def toggle_background_std_membrane(self):
        self.doubleSpinBox_9.setEnabled(self.checkBox_15.checkState())
        self.doubleSpinBox_7.setEnabled(self.checkBox_15.checkState())
    
    def toggle_background_std_cyto(self):
        self.doubleSpinBox_10.setEnabled(self.checkBox_16.checkState())
        self.doubleSpinBox_20.setEnabled(self.checkBox_16.checkState())
    
    def toggle_Detailed_cyto(self):
        self.comboBox_24.setEnabled(not self.checkBox_31.checkState()) 
        self.tableWidget_6.setEnabled(not self.checkBox_31.checkState()) 
    
    def toggle_Detailed_membrane(self):
        self.comboBox_17.setEnabled(not self.checkBox_24.checkState()) 
        self.tableWidget_3.setEnabled(not self.checkBox_24.checkState()) 
    
    def updateLambda_1(self, value):
        # Update the QLabel with the current value of the QScrollBar
        self.label_7.setText(str(self.comboBox.itemText(value+1)))

    def updateLambda_2(self, value):
        # Update the QLabel with the current value of the QScrollBar
        self.label_42.setText(str(self.comboBox.itemText(value+1)))


    def wrapCentralWidgetWithScrollArea(self):
            central_widget = self.centralWidget()
            if central_widget is not None:
                # Create a QScrollArea
                scroll_area = QtWidgets.QScrollArea()
                scroll_area.setWidget(central_widget)  # Set the existing central widget as the scroll area's widget
                scroll_area.setWidgetResizable(True)  # Make the scroll area resize with its contents

                # Set the QScrollArea as the new central widget
                self.setCentralWidget(scroll_area)

                # Adjust layout contents margins in dp, if necessary
                layout = central_widget.layout()
                if layout is not None:
                    margins = layout.contentsMargins()
                    margins_dp = QtCore.QMargins(px_to_dp(margins.left()), px_to_dp(margins.top()),
                                                 px_to_dp(margins.right()), px_to_dp(margins.bottom()))
                    layout.setContentsMargins(margins_dp)
                    
    def start_worker_thread(self): # Run analyzer
        self.progressBar_1.setVisible(True)
        self.label_10.setVisible(True)
        result,msg, = self.find_unique_valid_letters(self.plainTextEdit.toPlainText(),
                                                  self.comboBox.currentText(),
                                                  self.comboBox_2.currentText(),
                                                  self.comboBox_6.currentText(),
                                                  self.comboBox_7.currentText())
        if result:
            if not self.checkBox.isChecked():
                self.thread = QThread()
                self.worker = WorkerThread(self)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.terminate_thread.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.finished.connect(self.on_thread_finished)
                self.disable_parts()
                self.thread.start()
            elif self.checkBox.isChecked():
                result1,msg1, = self.find_unique_valid_letters(self.plainTextEdit_2.toPlainText(),
                                                       self.comboBox_13.currentText(),
                                                       self.comboBox_14.currentText(),
                                                       self.comboBox_15.currentText(),
                                                       self.comboBox_16.currentText())
                if result1:
                    self.thread = QThread()
                    self.worker = WorkerThread(self)
                    self.worker.moveToThread(self.thread)
                    self.thread.started.connect(self.worker.run)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.terminate_thread.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.finished.connect(self.on_thread_finished)
                    self.disable_parts()
                    self.thread.start()
                else:
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(msg1)
                    self.progressBar_1.setVisible(False)
            else:
                pass
        else:
            self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.plainTextEdit_1.appendPlainText(msg)
            self.progressBar_1.setVisible(False)
            
        
    def start_worker_thread_2(self): # Thresholding allone
        self.progressBar_1.setVisible(True)
        self.label_10.setVisible(True)
        result,msg, = self.find_unique_valid_letters(self.plainTextEdit.toPlainText(), self.comboBox.currentText(), self.comboBox_2.currentText(), self.comboBox_6.currentText(), self.comboBox_7.currentText())

        if result:
            if not self.checkBox.isChecked():
                self.thread = QThread()
                self.worker = WorkerThread(self)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.testthresholding)
                self.worker.finished.connect(self.thread.quit)
                self.worker.terminate_thread.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.finished.connect(self.on_thread_finished)
                self.disable_parts()
                self.thread.start()
            elif self.checkBox.isChecked():
                result1,msg1, = self.find_unique_valid_letters_cyto(self.plainTextEdit_2.toPlainText(),
                                                       self.comboBox_13.currentText(),
                                                       self.comboBox_14.currentText(),
                                                       self.comboBox_15.currentText(),
                                                       self.comboBox_16.currentText())
                if result1:
                    self.thread = QThread()
                    self.worker = WorkerThread(self)
                    self.worker.moveToThread(self.thread)
                    self.thread.started.connect(self.worker.testthresholding)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.terminate_thread.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.finished.connect(self.on_thread_finished)
                    self.disable_parts()
                    self.thread.start()
                else:
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(msg1)
                    self.progressBar_1.setVisible(False)
            else:
                pass
        else:
            self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.plainTextEdit_1.appendPlainText(msg)
            self.progressBar_1.setVisible(False)
            
        
    def on_thread_finished(self):
        # Thread finished execution
        #print("Thread finished.1")
        if self.tableWidget.currentRow() !=-1:
            self.tableWidget.selectRow(self.tableWidget.currentRow())
            self.updatePlots()
        #print("Thread finished.2")
        self.enablee_parts()
        self.progressBar_1.setVisible(False)
        self.label_10.setVisible(False)
        print("Thread finished")
        self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
        self.plainTextEdit_1.appendPlainText("Thread finished")

    def convert_to_type(self,value, value_type):
        try:
            # Attempt to convert the value to the primary type
            converted_value = value_type[0](value)
            return converted_value
        except ValueError:
            # If conversion fails, check if there's a secondary type defined
            if len(value_type) > 1:
                # Check if the value is "NAN" (case insensitive)
                if value.strip().lower() == "nan":
                    # If the value is "NAN", return it as a string
                    return "NaN"
                else:
                    # Otherwise, raise an exception
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText("Invalid value. Expected 'NAN'.")
            else:
                # If there's no secondary type, raise a general conversion exception
                self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                self.plainTextEdit_1.appendPlainText("Invalid value conversion.")

    def Detailed_Membrane_Masking_onItemChanged(self, item):

        row = item.row()
        newValue = item.text()
        T_value= item.column()
        Z_Value= self.comboBox_17.currentIndex()
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        
        translation_table = {
                                'Thresholding Mode': {'key': 'Ttype', 'type': (str,)},
                                'Manual Cutoff Level': {'key': 'ValManual', 'type': (int,)},
                                'Compression True/False': {'key': 'compress', 'type': (bool,)},
                                'Compression Value': {'key': 'Kvalue', 'type': (float,)},
                                'Remove Object': {'key': 'objSize', 'type': (int, str)},  # can be str or int
                                'Fill Holes': {'key': 'holesSize', 'type': (float, str)},  # can be str or float
                                'Dilate True/False': {'key': 'dilate', 'type': (bool,)},
                                'Dilation Shape': {'key': 'shape', 'type': (str,)},
                                'Dilation Shape Dimension 1': {'key': 'dim1', 'type': (int,)},
                                'Dilation Shape Dimension 2': {'key': 'dim2', 'type': (int,)},
                                'Gaussian Filter': {'key': 'GaussianS', 'type': (float, str)},  # can be str or int
                                'Signal to Noise Ratio': {'key': 'S_N', 'type': (float,)},
                                'Background StdDev': {'key': 'stddev', 'type': (float,)},  # can be 1 or float
                                'Background Mean': {'key': 'bgmean', 'type': (float, str)},  # can be str or float
                                'Specific Channel Wavelength': {'key': 'lambdaThr', 'type': (int, str)},  # can be str or int
                                # Add more translations as needed
                            }
        translation = translation_table.get(self.tableWidget_3.verticalHeaderItem(row).text())
        Error=True
        
        if translation:
            key = translation['key']
            if key == "Ttype":
                if newValue != "Otsu" and newValue != "Manual":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Thresholding Mode'. (Otsu or Manual)")
                    Error=False
            elif key == "ValManual":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Manual Cutoff Level'. (a int)")
                    Error=False
            elif key == "compress":
                if newValue != "True" and newValue != "False":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Compression True/False'. (True or False)")
                    Error=False
            elif key == "Kvalue":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Compression Value'. (a float)")
                    Error=False
            elif key == "objSize":
                if not newValue.isdigit() and newValue != "NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Remove Object'. (NaN or a int)")
                    Error=False
            elif key == "holesSize":
                if not newValue.replace(".", "", 1).isdigit() and newValue != "NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Fill Holes'. (NaN or a float)")
                    Error=False
            elif key == "dilate":
                if newValue != "True" and newValue != "False":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilate True/False'. (True or False)")
                    Error=False
            elif key == "shape":
                if newValue != "octagon" and newValue != "disk" and newValue != "square":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape'. (octagon ,disk or square)")
                    Error=False
            elif key == "dim1":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape Dimension 1'. (a int)")
                    Error=False
            elif key == "dim2":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape Dimension 2'. (a int)")
                    Error=False
            elif key == "GaussianS":
                if not newValue.isdigit() and newValue!="NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Gaussian Filter'. (NaN or a float)")
                    Error=False
            elif key == "S_N":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Signal to Noise Ratio'. (a float)")
                    Error=False
            elif key == "stddev":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Background StdDev'. (a float)")
                    Error=False
            elif key == "bgmean":
                if not newValue.replace(".", "", 1).isdigit() and newValue!="NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Background Mean'. (NaN or a float)")
                    Error=False
            elif key == 'lambdaThr':
                combo_items = [self.comboBox_18.itemText(i) for i in range(self.comboBox_18.count())]
                if newValue not in combo_items:
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Specific Channel Wavelength'. (NaN or a available channel number)")
                    Error=False
                    
            if Error:
                value_type = translation['type']
                maxT = self.tableWidget_3.columnCount()
                maxZ = self.comboBox_17.count()
        
                if filename in self.Membrane_Maskdata:
                    if maxT > 1 and maxZ < 1:  # T only
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Membrane_Maskdata[filename][T_value][key] = converted_value
                    elif maxT < 2 and maxZ > 1:  # Z only
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Membrane_Maskdata[filename][Z_Value][key] = converted_value
                    elif maxT > 1 and maxZ > 1:  # TZ
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Membrane_Maskdata[filename][T_value][Z_Value][key] = converted_value
                    elif maxT < 2 and maxZ < 1:  # TZ
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Membrane_Maskdata[filename][key] = converted_value
        

    def Update_formZ_Detailed_Membrane_Masking_Setting(self):
        if not self.tableWidget.rowCount() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().isSelected():
                    filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
                    self.tableWidget_3.blockSignals(True)
                    if filename in self.Membrane_Maskdata:
                        maxT=self.tableWidget_3.columnCount()
                        maxZ=self.comboBox_17.count()
                        
                        # Verwenden Sie die umgekehrte Übersetzungstabelle, um den Anzeigenamen in den internen Variablennamen umzuwandeln
                        reverse_translation_table = {
                        'Ttype': 'Thresholding Mode',
                        'ValManual': 'Manual Cutoff Level',
                        'compress': 'Compression True/False',
                        'Kvalue': 'Compression Value',
                        'objSize': 'Remove Object',
                        'holesSize': 'Fill Holes',
                        'dilate': 'Dilate True/False',
                        'shape': 'Dilation Shape',
                        'dim1': 'Dilation Shape Dimmension 1',
                        'dim2': 'Dilation Shape Dimmension 2',
                        'GaussianS': 'Gaussian Filter',
                        'S_N': 'Signal to Noise Ratio',
                        'stddev': 'Background StdDev',
                        'bgmean': 'Background Mean',
                        'lambdaThr': 'Specific Channel Wavelength',
                        }
                        
                        if maxT < 2 and maxZ > 1: # Z only
                            for T_index in range(self.tableWidget_3.columnCount()):
                                for key, value in self.Membrane_Maskdata[filename][self.comboBox_17.currentIndex()].items():
                                    translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                    header_index = None
                                    for i in range(self.tableWidget_3.rowCount()):
                                        if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                            header_index = i
                                            break  # Exit the column search loop once a match is found
                        
                                    # Set the value if a matching column was found
                                    if header_index is not None:
                                        item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                        self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            
                        elif maxT > 1 and maxZ > 1: # TZ
                            for T_index in range(self.tableWidget_3.columnCount()):
                                for key, value in self.Membrane_Maskdata[filename][T_index][self.comboBox_17.currentIndex()].items():
                                    translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                    header_index = None
                                    for i in range(self.tableWidget_3.rowCount()):
                                        if self.tableWidget_3.verticalHeaderItem(i).text() == key:
                                            header_index = i
                                            break  # Exit the column search loop once a match is found
                        
                                    # Set the value if a matching column was found
                                    if header_index is not None:
                                        item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                        self.tableWidget_3.setItem(header_index,T_index,QTableWidgetItem(item_value))
                    self.tableWidget_3.blockSignals(False)
                    
    def helper_for_button_updater(self):
        if self.tableWidget.rowCount() != 0 and self.tableWidget.currentItem() is not None and self.tableWidget.currentItem().isSelected():
            filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
            path=self.tableWidget.item(self.tableWidget.currentRow(),1).text() if self.tableWidget.currentRow() >= 0 else None
            self.update_toglobal_values_membrane(filename=filename, path=path)
        

    def update_toglobal_values_membrane(self,filename=None, path=None):
        self.tableWidget_3.blockSignals(True)
        if filename is None:
            filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
            path=self.tableWidget.item(self.tableWidget.currentRow(),1).text() if self.tableWidget.currentRow() >= 0 else None
            if path is None:
                return
        image,metadata=openfile(join(path,filename))
        Standard_Values={"Ttype":self.comboBox_3.currentText(),
           "ValManual":int(self.spinBox.value()),
           "compress": bool(self.checkBox_3.isChecked()),
           "Kvalue": float(self.doubleSpinBox.value()),
           "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
           "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
           "pxlSize":metadata['Pixelsize'],
           "dilate": bool(self.checkBox_6.isChecked()),
           "shape": self.comboBox_4.currentText(),
           "dim1":int(self.spinBox_4.value()), #shpae dim1
           "dim2":int(self.spinBox_5.value()), #shpae dim2
           "PixelDepth":metadata['BitDepth'],
           "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
           "S_N":self.doubleSpinBox_8.value(),
           "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
           "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
           "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText())),
           }
        reverse_translation_table = {
        'Ttype': 'Thresholding Mode',
        'ValManual': 'Manual Cutoff Level',
        'compress': 'Compression True/False',
        'Kvalue': 'Compression Value',
        'objSize': 'Remove Object',
        'holesSize': 'Fill Holes',
        'dilate': 'Dilate True/False',
        'shape': 'Dilation Shape',
        'dim1': 'Dilation Shape Dimmension 1',
        'dim2': 'Dilation Shape Dimmension 2',
        'GaussianS': 'Gaussian Filter',
        'S_N': 'Signal to Noise Ratio',
        'stddev': 'Background StdDev',
        'bgmean': 'Background Mean',
        'lambdaThr': 'Specific Channel Wavelength',
        }
        
        if metadata:
            if "Dimensions" in metadata:
                if metadata['Dimensions'][0]>1: #its a T stack
                    self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                else: # Z or 3dim
                    self.tableWidget_3.setColumnCount(1)
                
                for T_index in range(self.tableWidget_3.columnCount()):
                    for key, value in Standard_Values.items():
                        translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                        header_index = None
                        for i in range(self.tableWidget_3.rowCount()):
                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                header_index = i
                                break  # Exit the column search loop once a match is found
            
                        # Set the value if a matching column was found
                        if header_index is not None:
                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
            
                #self.comboBox_17.addItems([str(x) for x in metadata['Dimensions'][1]])
                
                if metadata['Dimensions'][1]>1:
                    self.comboBox_17.clear()
                    self.comboBox_17.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                else:
                    self.comboBox_17.clear()
                    
            elif "0" in metadata: # for lif and obl
                for n in range(len(metadata)):
                    print(metadata[n]['Dimensions'])
        self.Save_Detailed_Membrane_Masking_Setting(filename=filename, path=path)
        self.tableWidget_3.blockSignals(False)
        
    def Update_Detailed_Membrane_Masking_Setting(self):
        if not self.tableWidget.rowCount() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().isSelected():
                    filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
                    path=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
                    self.tableWidget_3.blockSignals(True)
                    reverse_translation_table = {
                    'Ttype': 'Thresholding Mode',
                    'ValManual': 'Manual Cutoff Level',
                    'compress': 'Compression True/False',
                    'Kvalue': 'Compression Value',
                    'objSize': 'Remove Object',
                    'holesSize': 'Fill Holes',
                    'dilate': 'Dilate True/False',
                    'shape': 'Dilation Shape',
                    'dim1': 'Dilation Shape Dimmension 1',
                    'dim2': 'Dilation Shape Dimmension 2',
                    'GaussianS': 'Gaussian Filter',
                    'S_N': 'Signal to Noise Ratio',
                    'stddev': 'Background StdDev',
                    'bgmean': 'Background Mean',
                    'lambdaThr': 'Specific Channel Wavelength',
                    }
                    if filename in self.Membrane_Maskdata:
                        self.comboBox_17.clear()
                        self.tableWidget_3.setColumnCount(0)
                        image,metadata=openfile(join(path,filename))
                        if "Dimensions" in metadata:
                            if metadata['Dimensions'][0]>1 and metadata['Dimensions'][1]>1 : #its a TZ stack
                                self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                                self.comboBox_17.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                for T_index in range(self.tableWidget_3.columnCount()):
                                    for key, value in self.Membrane_Maskdata[filename][T_index][self.comboBox_17.currentIndex()].items():
                                        translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                        header_index = None
                                        for i in range(self.tableWidget_3.rowCount()):
                                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif metadata['Dimensions'][0]>1 and not metadata['Dimensions'][1]>1 : #its a T stack
                                self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                                for T_index in range(self.tableWidget_3.columnCount()):
                                    for key, value in self.Membrane_Maskdata[filename][T_index].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_3.rowCount()):
                                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif not metadata['Dimensions'][0]>1 and metadata['Dimensions'][1]>1 : #its a Z stack
                                self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                                self.comboBox_17.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                for T_index in range(self.tableWidget_3.columnCount()):
                                    for key, value in self.Membrane_Maskdata[filename][self.comboBox_17.currentIndex()].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_3.rowCount()):
                                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif not metadata['Dimensions'][0]>1 and not metadata['Dimensions'][1]>1 : #its a Z stack
                                self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                                for T_index in range(self.tableWidget_3.columnCount()):
                                    for key, value in self.Membrane_Maskdata[filename].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_3.rowCount()):
                                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                    elif filename not in self.Membrane_Maskdata and filename:
                        image,metadata=openfile(join(path,filename))
                        Standard_Values={"Ttype":self.comboBox_3.currentText(),
                           "ValManual":int(self.spinBox.value()),
                           "compress": bool(self.checkBox_3.isChecked()),
                           "Kvalue": float(self.doubleSpinBox.value()),
                           "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                           "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                           "pxlSize":metadata['Pixelsize'],
                           "dilate": bool(self.checkBox_6.isChecked()),
                           "shape": self.comboBox_4.currentText(),
                           "dim1":int(self.spinBox_4.value()), #shpae dim1
                           "dim2":int(self.spinBox_5.value()), #shpae dim2
                           "PixelDepth":metadata['BitDepth'],
                           "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                           "S_N":self.doubleSpinBox_8.value(),
                           "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                           "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                           "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText())),
                           }
                        if metadata:
                            if "Dimensions" in metadata:
                                if metadata['Dimensions'][0]>1: #its a T stack
                                    self.tableWidget_3.setColumnCount(metadata['Dimensions'][0])
                                else: # Z or 3dim
                                    self.tableWidget_3.setColumnCount(1)
                                
                                for T_index in range(self.tableWidget_3.columnCount()):
                                    for key, value in Standard_Values.items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_3.rowCount()):
                                            if self.tableWidget_3.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_3.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            
                                #self.comboBox_17.addItems([str(x) for x in metadata['Dimensions'][1]])
                                
                                if metadata['Dimensions'][1]>1:
                                    self.comboBox_17.clear()
                                    self.comboBox_17.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                else:
                                    self.comboBox_17.clear()
                                    
                            elif "0" in metadata: # for lif and obl
                                for n in range(len(metadata)):
                                    print(metadata[n]['Dimensions'])
                        self.Save_Detailed_Membrane_Masking_Setting(filename=filename, path=path)
                else: 
                    self.tableWidget_3.setColumnCount(0)
                    self.comboBox_17.clear()
                    
                self.tableWidget_3.blockSignals(False)

        
    def Save_Detailed_Membrane_Masking_Setting(self,filename=None, path=None):
        if not self.tableWidget.rowCount() == 0:
            if filename is None:
                filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
                path=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
            image,metadata=openfile(join(path,filename))
            
            self.Membrane_Maskdata[filename]=[]
            if self.tableWidget_3.columnCount()>1: # only T
                for i in range(self.tableWidget_3.columnCount()): 
                    self.Membrane_Maskdata[filename].append({"Ttype":self.comboBox_3.currentText(),
                       "ValManual":int(self.spinBox.value()),
                       "compress": bool(self.checkBox_3.isChecked()),
                       "Kvalue": float(self.doubleSpinBox.value()),
                       "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                       "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                       "pxlSize":metadata['Pixelsize'],
                       "dilate": bool(self.checkBox_6.isChecked()),
                       "shape": self.comboBox_4.currentText(),
                       "dim1":int(self.spinBox_4.value()), #shpae dim1
                       "dim2":int(self.spinBox_5.value()), #shpae dim2
                       "PixelDepth":metadata['BitDepth'],
                       "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                       "S_N":self.doubleSpinBox_8.value(),
                          "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                       "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                       "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText())),
                       })
                    if self.comboBox_17.count() > 1: # TZ
                        self.Membrane_Maskdata[filename][i]=[]
                        for n in range(self.comboBox_17.count()):
                            self.Membrane_Maskdata[filename][i].append({"Ttype":self.comboBox_3.currentText(),
                               "ValManual":int(self.spinBox.value()),
                               "compress": bool(self.checkBox_3.isChecked()),
                               "Kvalue": float(self.doubleSpinBox.value()),
                               "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                               "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                               "pxlSize":metadata['Pixelsize'],
                               "dilate": bool(self.checkBox_6.isChecked()),
                               "shape": self.comboBox_4.currentText(),
                               "dim1":int(self.spinBox_4.value()), #shpae dim1
                               "dim2":int(self.spinBox_5.value()), #shpae dim2
                               "PixelDepth":metadata['BitDepth'],
                               "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                               "S_N":self.doubleSpinBox_8.value(),
                                  "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                               "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                               "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText())),
                               })
                            
            else:
                if self.comboBox_17.count() > 1: # only Z
                    self.Membrane_Maskdata[filename]=[]
                    for n in range(self.comboBox_17.count()):
                        self.Membrane_Maskdata[filename].append({"Ttype":self.comboBox_3.currentText(),
                           "ValManual":int(self.spinBox.value()),
                           "compress": bool(self.checkBox_3.isChecked()),
                           "Kvalue": float(self.doubleSpinBox.value()),
                           "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                           "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                           "pxlSize":metadata['Pixelsize'],
                           "dilate": bool(self.checkBox_6.isChecked()),
                           "shape": self.comboBox_4.currentText(),
                           "dim1":int(self.spinBox_4.value()), #shpae dim1
                           "dim2":int(self.spinBox_5.value()), #shpae dim2
                           "PixelDepth":metadata['BitDepth'],
                           "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                           "S_N":self.doubleSpinBox_8.value(),
                              "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                           "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                           "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText())),
                           })
                else: # only 3dim
                    self.Membrane_Maskdata[filename]={"Ttype":self.comboBox_3.currentText(),
                       "ValManual":int(self.spinBox.value()),
                       "compress": bool(self.checkBox_3.isChecked()),
                       "Kvalue": float(self.doubleSpinBox.value()),
                       "objSize":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                       "holesSize":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                       "pxlSize":metadata['Pixelsize'],
                       "dilate": bool(self.checkBox_6.isChecked()),
                       "shape": self.comboBox_4.currentText(),
                       "dim1":int(self.spinBox_4.value()), #shpae dim1
                       "dim2":int(self.spinBox_5.value()), #shpae dim2
                       "PixelDepth":metadata['BitDepth'],
                       "GaussianS":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                       "S_N":self.doubleSpinBox_8.value(),
                          "stddev": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                       "bgmean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                       "lambdaThr":"NaN" if not self.checkBox_27.isChecked() else (int(self.comboBox_18.currentText()))
                       }


    def Detailed_Cytosol_Masking_onItemChanged(self, item):
        row = item.row()
        newValue = item.text()
        T_value= item.column()
        Z_Value= self.comboBox_24.currentIndex()
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        
        translation_table = {
                                'Thresholding Mode': {'key': 'Ttype', 'type': (str,)},
                                'Manual Cutoff Level': {'key': 'ValManual', 'type': (int,)},
                                'Compression True/False': {'key': 'compress', 'type': (bool,)},
                                'Compression Value': {'key': 'Kvalue', 'type': (float,)},
                                'Remove Object': {'key': 'objSize', 'type': (int, str)},  # can be str or int
                                'Fill Holes': {'key': 'holesSize', 'type': (float, str)},  # can be str or float
                                'Dilate True/False': {'key': 'dilate', 'type': (bool,)},
                                'Dilation Shape': {'key': 'shape', 'type': (str,)},
                                'Dilation Shape Dimension 1': {'key': 'dim1', 'type': (int,)},
                                'Dilation Shape Dimension 2': {'key': 'dim2', 'type': (int,)},
                                'Gaussian Filter': {'key': 'GaussianS', 'type': (float, str)},  # can be str or int
                                'Signal to Noise Ratio': {'key': 'S_N', 'type': (float,)},
                                'Background StdDev': {'key': 'stddev', 'type': (float,)},  # can be 1 or float
                                'Background Mean': {'key': 'bgmean', 'type': (float, str)},  # can be str or float
                                'Specific Channel Wavelength': {'key': 'lambdaThr', 'type': (int, str)},  # can be str or int
                                # Add more translations as needed
                            }
        translation = translation_table.get(self.tableWidget_3.verticalHeaderItem(row).text())
        Error=True
        
        if translation:
            key = translation['key']
            if key == "Ttype":
                if newValue != "Otsu" and newValue != "Manual":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Thresholding Mode'. (Otsu or Manual)")
                    Error=False
            elif key == "ValManual":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Manual Cutoff Level'. (a int)")
                    Error=False
            elif key == "compress":
                if newValue != "True" and newValue != "False":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Compression True/False'. (True or False)")
                    Error=False
            elif key == "Kvalue":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Compression Value'. (a float)")
                    Error=False
            elif key == "objSize":
                if not newValue.isdigit() and newValue != "NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Remove Object'. (NaN or a int)")
                    Error=False
            elif key == "holesSize":
                if not newValue.replace(".", "", 1).isdigit() and newValue != "NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Fill Holes'. (NaN or a float)")
                    Error=False
            elif key == "dilate":
                if newValue != "True" and newValue != "False":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilate True/False'. (True or False)")
                    Error=False
            elif key == "shape":
                if newValue != "octagon" and newValue != "disk" and newValue != "square":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape'. (octagon ,disk or square)")
                    Error=False
            elif key == "dim1":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape Dimension 1'. (a int)")
                    Error=False
            elif key == "dim2":
                if not newValue.isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Dilation Shape Dimension 2'. (a int)")
                    Error=False
            elif key == "GaussianS":
                if not newValue.isdigit() and newValue!="NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Gaussian Filter'. (NaN or a float)")
                    Error=False
            elif key == "S_N":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Signal to Noise Ratio'. (a float)")
                    Error=False
            elif key == "stddev":
                if not newValue.replace(".", "", 1).isdigit():
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Background StdDev'. (a float)")
                    Error=False
            elif key == "bgmean":
                if not newValue.replace(".", "", 1).isdigit() and newValue!="NaN":
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Background Mean'. (NaN or a float)")
                    Error=False
            elif key == 'lambdaThr':
                combo_items = [self.comboBox_18.itemText(i) for i in range(self.comboBox_18.count())]
                if newValue not in combo_items:
                    self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
                    self.plainTextEdit_1.appendPlainText(f"The value '{newValue}' is not valid for 'Specific Channel Wavelength'. (NaN or a available channel number)")
                    Error=False
                    
            if Error:
                value_type = translation['type']
                maxT=self.tableWidget_6.columnCount()
                maxZ=self.comboBox_24.count()
                
                if filename in self.Cyto_Maskdata:
                    if maxT > 1 and maxZ < 1:  # T only
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Cyto_Maskdata[filename][T_value][key] = converted_value
                    elif maxT < 2 and maxZ > 1:  # Z only
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Cyto_Maskdata[filename][Z_Value][key] = converted_value
                    elif maxT > 1 and maxZ > 1:  # TZ
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Cyto_Maskdata[filename][T_value][Z_Value][key] = converted_value
                    elif maxT < 2 and maxZ < 1:  # TZ
                        # Convert the value to the desired type
                        converted_value = self.convert_to_type(newValue, value_type)
                        self.Cyto_Maskdata[filename][key] = converted_value
                
    def Update_formZ_Detailed_Cytosol_Masking_Setting(self):
        if not self.tableWidget.rowCount() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().isSelected():
                    filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
                    self.tableWidget_6.blockSignals(True)
                    if filename in self.Cyto_Maskdata:
                        maxT=self.tableWidget_6.columnCount()
                        maxZ=self.comboBox_24.count()
                        
                        # Verwenden Sie die umgekehrte Übersetzungstabelle, um den Anzeigenamen in den internen Variablennamen umzuwandeln
                        reverse_translation_table = {
                        'Ttype': 'Thresholding Mode',
                        'ValManual': 'Manual Cutoff Level',
                        'compress': 'Compression True/False',
                        'Kvalue': 'Compression Value',
                        'objSize': 'Remove Object',
                        'holesSize': 'Fill Holes',
                        'dilate': 'Dilate True/False',
                        'shape': 'Dilation Shape',
                        'dim1': 'Dilation Shape Dimmension 1',
                        'dim2': 'Dilation Shape Dimmension 2',
                        'GaussianS': 'Gaussian Filter',
                        'S_N': 'Signal to Noise Ratio',
                        'stddev': 'Background StdDev',
                        'bgmean': 'Background Mean',
                        'lambdaThr': 'Specific Channel Wavelength',
                        }
                        
                        if maxT < 2 and maxZ > 1: # Z only
                            for T_index in range(self.tableWidget_6.columnCount()):
                                for key, value in self.Cyto_Maskdata[filename][self.comboBox_24.currentIndex()].items():
                                    translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                    header_index = None
                                    for i in range(self.tableWidget_6.rowCount()):
                                        if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                            header_index = i
                                            break  # Exit the column search loop once a match is found
                        
                                    # Set the value if a matching column was found
                                    if header_index is not None:
                                        item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                        self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            
                        elif maxT > 1 and maxZ > 1: # TZ
                            for T_index in range(self.tableWidget_6.columnCount()):
                                for key, value in self.Cyto_Maskdata[filename][T_index][self.comboBox_24.currentIndex()].items():
                                    translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                    header_index = None
                                    for i in range(self.tableWidget_6.rowCount()):
                                        if self.tableWidget_6.verticalHeaderItem(i).text() == key:
                                            header_index = i
                                            break  # Exit the column search loop once a match is found
                        
                                    # Set the value if a matching column was found
                                    if header_index is not None:
                                        item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                        self.tableWidget_6.setItem(header_index,T_index,QTableWidgetItem(item_value))
                    self.tableWidget_6.blockSignals(False)
                    

    def helper2_for_button_updater(self):
        if self.tableWidget.rowCount() != 0 and self.tableWidget.currentItem() is not None and self.tableWidget.currentItem().isSelected():
            filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
            path=self.tableWidget.item(self.tableWidget.currentRow(),1).text() if self.tableWidget.currentRow() >= 0 else None
            self.update_toglobal_values_cytosol(filename=filename, path=path)
            
    def update_toglobal_values_cytosol(self, filename=None,path=None):
       self.tableWidget_6.blockSignals(True)
       if filename is None:
           filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
           path=self.tableWidget.item(self.tableWidget.currentRow(),1).text() if self.tableWidget.currentRow() >= 0 else None
       if path is None:
           return
       image,metadata=openfile(join(path,filename))
       Standard_Values={"Ttype":self.comboBox_21.currentText(),
          "ValManual":int(self.spinBox_15.value()),
          "compress": bool(self.checkBox_32.isChecked()),
          "Kvalue": float(self.doubleSpinBox_23.value()),
          "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
          "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
          "pxlSize":metadata['Pixelsize'],
          "dilate": bool(self.checkBox_37.isChecked()),
          "shape": self.comboBox_22.currentText(),
          "dim1":int(self.spinBox_17.value()), #shpae dim1
          "dim2":int(self.spinBox_16.value()), #shpae dim2
          "PixelDepth":metadata['BitDepth'],
          "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
          "S_N":self.doubleSpinBox_21.value(),
          "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
          "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
          "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
          }
       reverse_translation_table = {
       'Ttype': 'Thresholding Mode',
       'ValManual': 'Manual Cutoff Level',
       'compress': 'Compression True/False',
       'Kvalue': 'Compression Value',
       'objSize': 'Remove Object',
       'holesSize': 'Fill Holes',
       'dilate': 'Dilate True/False',
       'shape': 'Dilation Shape',
       'dim1': 'Dilation Shape Dimmension 1',
       'dim2': 'Dilation Shape Dimmension 2',
       'GaussianS': 'Gaussian Filter',
       'S_N': 'Signal to Noise Ratio',
       'stddev': 'Background StdDev',
       'bgmean': 'Background Mean',
       'lambdaThr': 'Specific Channel Wavelength',
       }
       
       if metadata:
           if "Dimensions" in metadata:
               if metadata['Dimensions'][0]>1: #its a T stack
                   self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
               else: # Z or 3dim
                   self.tableWidget_6.setColumnCount(1)
               
               for T_index in range(self.tableWidget_6.columnCount()):
                   for key, value in Standard_Values.items():
                       translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                       header_index = None
                       for i in range(self.tableWidget_6.rowCount()):
                           if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                               header_index = i
                               break  # Exit the column search loop once a match is found
           
                       # Set the value if a matching column was found
                       if header_index is not None:
                           item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                           self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
           
               #self.comboBox_17.addItems([str(x) for x in metadata['Dimensions'][1]])
               
               if metadata['Dimensions'][1]>1:
                   self.comboBox_24.clear()
                   self.comboBox_24.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
               else:
                   self.comboBox_24.clear()
                   
           elif "0" in metadata: # for lif and obl
               for n in range(len(metadata)):
                   print(metadata[n]['Dimensions'])
       self.Save_Detailed_Cytosol_Masking_Setting(filename=filename, path=path)
       self.tableWidget_6.blockSignals(False)
       
    def Update_Detailed_Cytosol_Masking_Setting(self):
        if not self.tableWidget.rowCount() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().isSelected():
                    filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text() if self.tableWidget.currentRow() >= 0 else None
                    path=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
                    self.tableWidget_6.blockSignals(True)
                    reverse_translation_table = {
                    'Ttype': 'Thresholding Mode',
                    'ValManual': 'Manual Cutoff Level',
                    'compress': 'Compression True/False',
                    'Kvalue': 'Compression Value',
                    'objSize': 'Remove Object',
                    'holesSize': 'Fill Holes',
                    'dilate': 'Dilate True/False',
                    'shape': 'Dilation Shape',
                    'dim1': 'Dilation Shape Dimmension 1',
                    'dim2': 'Dilation Shape Dimmension 2',
                    'GaussianS': 'Gaussian Filter',
                    'S_N': 'Signal to Noise Ratio',
                    'stddev': 'Background StdDev',
                    'bgmean': 'Background Mean',
                    'lambdaThr': 'Specific Channel Wavelength',
                    }
                    if filename in self.Cyto_Maskdata:
                        self.comboBox_24.clear()
                        self.tableWidget_6.setColumnCount(0)
                        image,metadata=openfile(join(path,filename))
                        if "Dimensions" in metadata:
                            if metadata['Dimensions'][0]>1 and metadata['Dimensions'][1]>1 : #its a TZ stack
                                self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
                                self.comboBox_24.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                for T_index in range(self.tableWidget_6.columnCount()):
                                    for key, value in self.Cyto_Maskdata[filename][T_index][self.comboBox_24.currentIndex()].items():
                                        translated_key = reverse_translation_table.get(key, key)  # Übersetzen Sie den internen Variablennamen in den Anzeigenamen
                                        header_index = None
                                        for i in range(self.tableWidget_6.rowCount()):
                                            if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif metadata['Dimensions'][0]>1 and not metadata['Dimensions'][1]>1 : #its a T stack
                                self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
                                for T_index in range(self.tableWidget_6.columnCount()):
                                    for key, value in self.Cyto_Maskdata[filename][T_index].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_6.rowCount()):
                                            if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif not metadata['Dimensions'][0]>1 and metadata['Dimensions'][1]>1 : #its a Z stack
                                self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
                                self.comboBox_24.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                for T_index in range(self.tableWidget_6.columnCount()):
                                    for key, value in self.Cyto_Maskdata[filename][self.comboBox_24.currentIndex()].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_6.rowCount()):
                                            if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            elif not metadata['Dimensions'][0]>1 and not metadata['Dimensions'][1]>1 : #its a Z stack
                                self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
                                for T_index in range(self.tableWidget_6.columnCount()):
                                    for key, value in self.Cyto_Maskdata[filename].items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_6.rowCount()):
                                            if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                    elif filename not in self.Cyto_Maskdata and filename:
                        image,metadata=openfile(join(path,filename))
                        Standard_Values={"Ttype":self.comboBox_21.currentText(),
                           "ValManual":int(self.spinBox_15.value()),
                           "compress": bool(self.checkBox_32.isChecked()),
                           "Kvalue": float(self.doubleSpinBox_23.value()),
                           "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                           "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                           "pxlSize":metadata['Pixelsize'],
                           "dilate": bool(self.checkBox_37.isChecked()),
                           "shape": self.comboBox_22.currentText(),
                           "dim1":int(self.spinBox_17.value()), #shpae dim1
                           "dim2":int(self.spinBox_16.value()), #shpae dim2
                           "PixelDepth":metadata['BitDepth'],
                           "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                           "S_N":self.doubleSpinBox_21.value(),
                           "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                           "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                           "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
                           }
                        if metadata:
                            if "Dimensions" in metadata:
                                if metadata['Dimensions'][0]>1: #its a T stack
                                    self.tableWidget_6.setColumnCount(metadata['Dimensions'][0])
                                else: # Z or 3dim
                                    self.tableWidget_6.setColumnCount(1)
                                
                                for T_index in range(self.tableWidget_6.columnCount()):
                                    for key, value in Standard_Values.items():
                                        translated_key = reverse_translation_table.get(key, key)
                                        header_index = None
                                        for i in range(self.tableWidget_6.rowCount()):
                                            if self.tableWidget_6.verticalHeaderItem(i).text() == translated_key:
                                                header_index = i
                                                break  # Exit the column search loop once a match is found
                            
                                        # Set the value if a matching column was found
                                        if header_index is not None:
                                            item_value = str(value) if not isinstance(value, bool) else "True" if value else "False"
                                            self.tableWidget_6.setItem(header_index,T_index, QTableWidgetItem(item_value))
                            
                                #self.comboBox_24.addItems([str(x) for x in metadata['Dimensions'][1]])
                                
                                if metadata['Dimensions'][1]>1:
                                    self.comboBox_24.clear()
                                    self.comboBox_24.addItems([str(x+1) for x in range(metadata['Dimensions'][1])])
                                else:
                                    self.comboBox_24.clear()
                                    
                            elif "0" in metadata: # for lif and obl
                                for n in range(len(metadata)):
                                    print(metadata[n]['Dimensions'])
                        self.Save_Detailed_Cytosol_Masking_Setting(filename=filename, path=path)
                else: 
                    self.tableWidget_6.setColumnCount(0)
                    self.comboBox_24.clear()
                    
                self.tableWidget_6.blockSignals(False)

        
    def Save_Detailed_Cytosol_Masking_Setting(self,filename=None, path=None):
        if not self.tableWidget.rowCount() == 0:
            if filename is None:
                filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
                path=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
            image,metadata=openfile(join(path,filename))
            
            self.Cyto_Maskdata[filename]=[]
            if self.tableWidget_6.columnCount()>1: # only T
                for i in range(self.tableWidget_6.columnCount()): 
                    self.Cyto_Maskdata[filename].append({"Ttype":self.comboBox_21.currentText(),
                       "ValManual":int(self.spinBox_15.value()),
                       "compress": bool(self.checkBox_32.isChecked()),
                       "Kvalue": float(self.doubleSpinBox_23.value()),
                       "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                       "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                       "pxlSize":metadata['Pixelsize'],
                       "dilate": bool(self.checkBox_37.isChecked()),
                       "shape": self.comboBox_22.currentText(),
                       "dim1":int(self.spinBox_17.value()), #shpae dim1
                       "dim2":int(self.spinBox_16.value()), #shpae dim2
                       "PixelDepth":metadata['BitDepth'],
                       "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                       "S_N":self.doubleSpinBox_21.value(),
                       "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                       "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                       "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
                       })
                    if self.comboBox_24.count() > 1: # TZ
                        self.Cyto_Maskdata[filename][i]=[]
                        for n in range(self.comboBox_24.count()):
                            self.Cyto_Maskdata[filename][i].append({"Ttype":self.comboBox_21.currentText(),
                               "ValManual":int(self.spinBox_15.value()),
                               "compress": bool(self.checkBox_32.isChecked()),
                               "Kvalue": float(self.doubleSpinBox_23.value()),
                               "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                               "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                               "pxlSize":metadata['Pixelsize'],
                               "dilate": bool(self.checkBox_37.isChecked()),
                               "shape": self.comboBox_22.currentText(),
                               "dim1":int(self.spinBox_17.value()), #shpae dim1
                               "dim2":int(self.spinBox_16.value()), #shpae dim2
                               "PixelDepth":metadata['BitDepth'],
                               "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                               "S_N":self.doubleSpinBox_21.value(),
                               "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                               "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                               "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
                               })
                            
            else:
                if self.comboBox_24.count() > 1: # only Z
                    self.Cyto_Maskdata[filename]=[]
                    for n in range(self.comboBox_24.count()):
                        self.Cyto_Maskdata[filename].append({"Ttype":self.comboBox_21.currentText(),
                           "ValManual":int(self.spinBox_15.value()),
                           "compress": bool(self.checkBox_32.isChecked()),
                           "Kvalue": float(self.doubleSpinBox_23.value()),
                           "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                           "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                           "pxlSize":metadata['Pixelsize'],
                           "dilate": bool(self.checkBox_37.isChecked()),
                           "shape": self.comboBox_22.currentText(),
                           "dim1":int(self.spinBox_17.value()), #shpae dim1
                           "dim2":int(self.spinBox_16.value()), #shpae dim2
                           "PixelDepth":metadata['BitDepth'],
                           "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                           "S_N":self.doubleSpinBox_21.value(),
                           "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                           "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                           "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
                           })
                else: # only 3dim
                    self.Cyto_Maskdata[filename]={"Ttype":self.comboBox_21.currentText(),
                       "ValManual":int(self.spinBox_15.value()),
                       "compress": bool(self.checkBox_32.isChecked()),
                       "Kvalue": float(self.doubleSpinBox_23.value()),
                       "objSize":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                       "holesSize":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                       "pxlSize":metadata['Pixelsize'],
                       "dilate": bool(self.checkBox_37.isChecked()),
                       "shape": self.comboBox_22.currentText(),
                       "dim1":int(self.spinBox_17.value()), #shpae dim1
                       "dim2":int(self.spinBox_16.value()), #shpae dim2
                       "PixelDepth":metadata['BitDepth'],
                       "GaussianS":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                       "S_N":self.doubleSpinBox_21.value(),
                       "stddev": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                       "bgmean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                       "lambdaThr":"NaN" if not self.checkBox_36.isChecked() else (int(self.comboBox_23.currentText())),
                       }


    def changeverticalScrollBar(self):
        self.verticalScrollBar_2.setValue(self.verticalScrollBar.value())
        self.tableWidget_2.setCurrentCell(0,0)
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.verticalScrollBar_3.setValue(self.verticalScrollBar.value())

        
    def changeverticalScrollBar_2(self):
        self.verticalScrollBar.setValue(self.verticalScrollBar_2.value())
        self.tableWidget_2.setCurrentCell(0,0)
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.verticalScrollBar_3.setValue(self.verticalScrollBar_2.value())
        
    def changeverticalScrollBar_3(self):
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.verticalScrollBar.setValue(self.verticalScrollBar_3.value())
            self.tableWidget_2.setCurrentCell(0,0)
            self.verticalScrollBar_2.setValue(self.verticalScrollBar_3.value())
        
    def changehorzontalScrollBar(self):

        self.horizontalScrollBar_2.setValue(self.horizontalScrollBar.value())
        self.tableWidget_2.setCurrentCell(0,0)
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.horizontalScrollBar_3.setValue(self.horizontalScrollBar.value())
        
    def changehorzontalScrollBar_2(self):
        self.horizontalScrollBar.setValue(self.horizontalScrollBar_2.value())
        self.tableWidget_2.setCurrentCell(0,0)
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.horizontalScrollBar_3.setValue(self.horizontalScrollBar_2.value())
        
    def changehorzontalScrollBar_3(self):
        filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if filename in self.ConnectSliders:
            self.horizontalScrollBar.setValue(self.horizontalScrollBar_3.value())
            self.tableWidget_2.setCurrentCell(0,0)
            self.horizontalScrollBar_2.setValue(self.horizontalScrollBar_3.value())
        
    def updatePlots(self):
        if self.tableWidget.currentRow() !=-1:
            filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
            if self.tableWidget.item(self.tableWidget.currentRow(),0) != [] and filename in self.key:

                if self.key[filename]=="Zstack":
                    if filename in self.GPImage:
                        self.verticalScrollBar.setEnabled(True)
                        self.verticalScrollBar.setRange(0,len(self.GPImage[filename])-1)
                        self.horizontalScrollBar.setEnabled(False)
                        if self.nobjects[filename][0] != 0:
                            self.verticalScrollBar_2.setEnabled(True)
                            self.verticalScrollBar_2.setRange(0,len(self.GPImage[filename])-1)
                            self.horizontalScrollBar_2.setEnabled(False)
    
                    self.verticalScrollBar_3.setEnabled(True)
                    self.verticalScrollBar_3.setRange(0,len(self.RawImages[filename])-1)
                    self.horizontalScrollBar_3.setEnabled(False)
                    self.horizontalScrollBar_4.setEnabled(True)
                    self.horizontalScrollBar_4.setRange(0,len(self.RawImages[filename][0][0][0])-1)
                
                elif self.key[filename]=="Tstack":
                    if filename in self.GPImage:
                        self.horizontalScrollBar.setEnabled(True)
                        self.horizontalScrollBar.setRange(0,len(self.GPImage[filename])-1)
                        self.verticalScrollBar.setEnabled(False)
                        if self.nobjects[filename][0] != 0:
                            self.horizontalScrollBar_2.setEnabled(True)
                            self.horizontalScrollBar_2.setRange(0,len(self.GPImage[filename])-1)
                            self.verticalScrollBar_2.setEnabled(False)
                    
                    self.horizontalScrollBar_3.setEnabled(True)
                    self.horizontalScrollBar_3.setRange(0,len(self.RawImages[filename])-1)
                    self.verticalScrollBar_3.setEnabled(False)
                    self.horizontalScrollBar_4.setEnabled(True)
                    self.horizontalScrollBar_4.setRange(0,len(self.RawImages[filename][0][0][0])-1)
                
                elif self.key[filename]=="TZstack":
                    if filename in self.GPImage:
                        self.horizontalScrollBar.setEnabled(True)
                        self.horizontalScrollBar.setRange(0,len(self.GPImage[filename])-1)
                        self.verticalScrollBar.setEnabled(True)
                        self.verticalScrollBar.setRange(0,len(self.GPImage[filename][0])-1)
                        if self.nobjects[filename][0][0] != 0:
                            self.horizontalScrollBar_2.setEnabled(True)
                            self.horizontalScrollBar_2.setRange(0,len(self.GPImage[filename])-1)    
                            self.verticalScrollBar_2.setEnabled(True)
                            self.verticalScrollBar_2.setRange(0,len(self.GPImage[filename][0])-1)
                    
                    self.horizontalScrollBar_3.setEnabled(True)
                    self.horizontalScrollBar_3.setRange(0,len(self.RawImages[filename])-1)
                    self.verticalScrollBar_3.setEnabled(True)
                    self.verticalScrollBar_3.setRange(0,len(self.RawImages[filename][0])-1)
                    self.horizontalScrollBar_4.setEnabled(True)
                    self.horizontalScrollBar_4.setRange(0,len(self.RawImages[filename][0][0][0][0])-1)
                    
                else:
                    self.verticalScrollBar.setEnabled(False)
                    self.verticalScrollBar_2.setEnabled(False)
                    self.verticalScrollBar_3.setEnabled(False)
                    self.horizontalScrollBar.setEnabled(False)
                    self.horizontalScrollBar_2.setEnabled(False)
                    self.horizontalScrollBar_3.setEnabled(False)
                    self.horizontalScrollBar_4.setEnabled(True)
                    self.horizontalScrollBar_4.setRange(0,len(self.RawImages[filename][0][0])-1)
                

                if self.tabWidget_2.currentIndex() == 0 and filename in self.RawImages:
                    self.plot_RawImage(self.RawImages[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 0 and filename in self.Masks:
                    self.plot_Mask(self.Masks[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 0 and filename in self.Cyto_Masks:
                    self.plot_Cyto_Mask(self.Cyto_Masks[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.GPImage:
                    self.plot_GPImage(self.GPImage[filename],self.key[filename])
                    self.Update_Stats_FullImage(self.FullImage_Parameters[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.Cyto_GPImage:
                    self.plot_Cyto_GPImage(self.Cyto_GPImage[filename],self.key[filename])
                    self.Update_Stats_FullImage_cyto(self.FullImage_Parameters_cyto[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.GPImage: #GP Histogramm 
                    self.plot_GPHistogramm(self.GPImage[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.Cyto_GPImage: #GP Histogramm 
                    self.plot_Cyto_GPHistogramm(self.Cyto_GPImage[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.GPPhasor_polar_all: #Phasor
                    self.plot_GPPhasor(self.GPPhasor_polar_all[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.Cyto_GPPhasor_polar_all: #Phasor
                    self.plot_Cyto_GPPhasor(self.Cyto_GPPhasor_polar_all[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.Intensities: #Intensities Histogramm 
                    self.plot_IntesitieDist(self.Intensities[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 1 and filename in self.Cyto_Intensities: #Intensities Histogramm 
                    self.plot_Cyto_IntesitieDist(self.Cyto_Intensities[filename],self.key[filename])
                if self.tabWidget_2.currentIndex() == 2 and filename in self.nobjects:
                        if self.key[filename] == "3dim":
                            if self.nobjects[filename] != 0:
                                self.tableWidget_2.setRowCount(self.nobjects[filename])
                                row=0
                                for i in range(self.nobjects[filename]):
                                    self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                                    row=row+1
                                self.tableWidget_2.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Object Nr."))
                                self.plot_GPImage_Object(self.GPImage[filename],self.key[filename],self.Object_Coordinates[filename])
                                if filename in self.Cyto_Image:
                                    self.plot_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.key[filename],self.Object_Coordinates[filename])
                            else:
                                self.tableWidget_2.setRowCount(0)
                                self.plot_GPImage_Object([],[],[])
                                self.plot_Cyto_GPImage_Object([],[],[])
                                self.plot_GPHistogramm_Object([],[])
                                self.plot_Cyto_GPHistogramm_Object([],[])
                                self.plot_GPImageZoom_Object([],[])
                                self.Update_Stats_oject_membrane([],[],[])
                                self.plot_Membrane_Segment_Object([],[])
                                self.plot_IntesitieDist_Object([],[])
                                self.plot_Cyto_IntesitieDist_Object([],[])
                                self.plot_GPPhasor_Object([],[],[])
                                self.plot_Cyto_GPPhasor_Object([],[],[])
                                self.plot_GProfile_Object([],[])
                                self.plot_CytoObject([],[])
                                self.Update_Stats_oject_cyto([],[])
                                self.plot_CytoLineProfile([],[])
                                self.tableWidget_2.clear()
                                
                        elif self.key[filename] == "Zstack":
                            if self.nobjects[filename][0] != 0:
                                self.tableWidget_2.setRowCount(self.nobjects[filename][self.verticalScrollBar_2.value()])
                                row=0
                                for i in range(self.nobjects[filename][self.verticalScrollBar_2.value()]):
                                     self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                                     row=row+1
                                self.tableWidget_2.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Object Nr."))
                                self.plot_GPImage_Object(self.GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.verticalScrollBar_2.value()])
                                if filename in self.Cyto_Image:
                                    self.plot_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.verticalScrollBar_2.value()])
                            else:
                                self.tableWidget_2.setRowCount(0)
                                self.plot_GPImage_Object([],[],[])
                                self.plot_Cyto_GPImage_Object([],[],[])
                                self.plot_GPHistogramm_Object([],[])
                                self.plot_GPImageZoom_Object([],[])
                                self.Update_Stats_oject_membrane([],[],[])
                                self.plot_Membrane_Segment_Object([],[])
                                self.plot_IntesitieDist_Object([],[])
                                self.plot_Cyto_IntesitieDist_Object([],[])
                                self.plot_GPPhasor_Object([],[],[])
                                self.plot_Cyto_GPPhasor_Object([],[],[])
                                self.plot_GProfile_Object([],[])
                                self.plot_CytoObject([],[])
                                self.Update_Stats_oject_cyto([],[])
                                self.plot_CytoLineProfile([],[])
                                self.tableWidget_2.clear()
                                
                        elif self.key[filename] == "Tstack":
                            if self.nobjects[filename][0] != 0:
                                self.tableWidget_2.setRowCount(self.nobjects[filename][self.horizontalScrollBar_2.value()])
                                row=0
                                for i in range(self.nobjects[filename][self.horizontalScrollBar_2.value()]):
                                    self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                                    row=row+1
                                self.tableWidget_2.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Object Nr."))
                                self.plot_GPImage_Object(self.GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()])
                                if filename in self.Cyto_Image:
                                    self.plot_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()])
                            else:
                                self.tableWidget_2.setRowCount(0)
                                self.plot_GPImage_Object([],[],[])
                                self.plot_Cyto_GPImage_Object([],[],[])
                                self.plot_GPHistogramm_Object([],[])
                                self.plot_Cyto_GPHistogramm_Object([],[])
                                self.plot_GPImageZoom_Object([],[])
                                self.Update_Stats_oject_membrane([],[],[])
                                self.plot_Membrane_Segment_Object([],[])
                                self.plot_IntesitieDist_Object([],[])
                                self.plot_Cyto_IntesitieDist_Object([],[])
                                self.plot_GPPhasor_Object([],[],[])
                                self.plot_Cyto_GPPhasor_Object([],[],[])
                                self.plot_GProfile_Object([],[])
                                self.plot_CytoObject([],[])
                                self.Update_Stats_oject_cyto([],[])
                                self.plot_CytoLineProfile([],[])
                                self.tableWidget_2.clear()
                                
                        elif self.key[filename] == "TZstack":
                            if self.nobjects[filename][0][0] != 0:
                                self.tableWidget_2.setRowCount(self.nobjects[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()])
                                row=0
                                for i in range(self.nobjects[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()]):
                                    self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                                    row=row+1
                                self.tableWidget_2.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Object Nr."))
                                self.plot_GPImage_Object(self.GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()])
                                if filename in self.Cyto_Image:
                                    self.plot_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.key[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()])
                            else:
                                self.tableWidget_2.setRowCount(0)
                                self.plot_GPImage_Object([],[],[])
                                self.plot_Cyto_GPImage_Object([],[],[])
                                self.plot_GPHistogramm_Object([],[])
                                self.plot_Cyto_GPHistogramm_Object([],[])
                                self.plot_GPImageZoom_Object([],[])
                                self.Update_Stats_oject_membrane([],[],[])
                                self.plot_Membrane_Segment_Object([],[])
                                self.plot_IntesitieDist_Object([],[])
                                self.plot_Cyto_IntesitieDist_Object([],[])
                                self.plot_GPPhasor_Object([],[],[])
                                self.plot_Cyto_GPPhasor_Object([],[],[])
                                self.plot_GProfile_Object([],[])
                                self.plot_CytoObject([],[])
                                self.Update_Stats_oject_cyto([],[])
                                self.plot_CytoLineProfile([],[])
                                self.tableWidget_2.clear()
                else:
                        self.tableWidget_2.setRowCount(0)
                    
            else:
                self.plot_RawImage([],[])
                self.plot_Mask([],[])
                self.plot_Cyto_Mask([],[])
                self.plot_GPImage([],[])
                self.plot_Cyto_GPImage([],[])
                self.Update_Stats_FullImage_cyto([],[])
                self.plot_GPHistogramm([],[])
                self.plot_Cyto_GPHistogramm([],[])
                self.plot_GPPhasor([],[])
                self.plot_IntesitieDist([],[])
                self.plot_GPImage_Object([],[],[])
                self.plot_Cyto_GPImage_Object([],[],[])
                self.plot_GPHistogramm_Object([],[])
                self.plot_Cyto_GPHistogramm_Object([],[])
                self.plot_GPImageZoom_Object([],[])
                self.Update_Stats_oject_membrane([],[],[])
                self.plot_Membrane_Segment_Object([],[])
                self.plot_IntesitieDist_Object([],[])
                self.plot_Cyto_IntesitieDist_Object([],[])
                self.plot_GPPhasor_Object([],[],[])
                self.plot_Cyto_GPPhasor_Object([],[],[])
                self.plot_GProfile_Object([],[])
                self.plot_CytoObject([],[])
                self.Update_Stats_oject_cyto([],[])
                self.plot_CytoLineProfile([],[])
                self.tableWidget_2.clear()
        app.processEvents()

    def updatePlots_Objects(self):
        if self.tableWidget_2.currentRow() != -1:
            ObjectNr=self.tableWidget_2.item(self.tableWidget_2.currentRow(),0).text()
            if self.tableWidget.currentItem() is not None:
                filename=self.tableWidget.item(self.tableWidget.currentRow(),0).text()
                if len(self.key) != 0:
                    if self.key[filename] == "3dim":
                        if ObjectNr !=0:
                            self.plot_update_GPImage_Object(self.GPImage[filename],self.Object_Coordinates[filename],ObjectNr,self.key[filename])
                            self.plot_GPImageZoom_Object(self.GPImage_per_object[filename][int(ObjectNr)-1],self.key[filename])
                            self.Update_Stats_oject_membrane(self.Object_Parameters[filename][int(ObjectNr)-1],self.Object_Morphology[filename][int(ObjectNr)-1],self.key[filename])
                            self.plot_Membrane_Segment_Object(self.MembraneSegments[filename][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPHistogramm_Object(self.GPImage_per_object[filename][int(ObjectNr)-1],self.key[filename])
                            self.plot_IntesitieDist_Object(self.Intensities_per_object[filename][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPPhasor_Object(self.GPPhasor_polar_obj[filename],ObjectNr,self.key[filename])
                            if len(self.Profile) !=0:
                                if filename in self.Profile and self.Profile:
                                    self.plot_GProfile_Object(self.Profile[filename][int(ObjectNr)-1],self.key[filename])
                                else:
                                    self.plot_GProfile_Object([],[])
                            if len(self.Cyto_Image) != 0:
                                if filename in self.Cyto_Image:
                                    self.plot_update_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.Object_Coordinates[filename],ObjectNr,self.key[filename])
                                    self.horizontalScrollBar_5.setEnabled(True)
                                    self.horizontalScrollBar_5.setRange(0,self.dims[filename][len(self.dims[filename])-1]-1)
                                    self.plot_CytoObject(self.Cyto_Image[filename][int(ObjectNr)-1],self.key[filename])
                                    self.Update_Stats_oject_cyto(self.Object_Parameters_cyto[filename][int(ObjectNr)-1],self.key[filename])
                                    self.plot_CytoLineProfile(self.Cytoprof[filename][int(ObjectNr)-1],self.key[filename])
                                    self.plot_Cyto_GPHistogramm_Object(self.Cyto_Image[filename][int(ObjectNr)-1],self.key[filename])
                                    self.plot_Cyto_IntesitieDist_Object(self.Cyto_Intensities_per_object[filename][int(ObjectNr)-1],self.key[filename])
                                    self.plot_Cyto_GPPhasor_Object(self.Cyto_GPPhasor_polar_obj[filename],ObjectNr,self.key[filename])
                                else:
                                    self.plot_CytoObject([],[])
                                    self.Update_Stats_oject_cyto([],[])
                                    self.plot_Cyto_GPHistogramm_Object([],[])
                                    self.plot_Cyto_IntesitieDist_Object([],[])
                                    self.plot_Cyto_GPPhasor_Object([],[],[])
                                    self.plot_CytoLineProfile([],[])
            
                                
                    elif self.key[filename] == "Zstack":
                        if len(self.nobjects[filename]) != 0:
                            self.plot_update_GPImage_Object(self.GPImage[filename],self.Object_Coordinates[filename][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                            self.plot_GPHistogramm_Object(self.GPImage_per_object[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPImageZoom_Object(self.GPImage_per_object[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.Update_Stats_oject_membrane(self.Object_Parameters[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.Object_Morphology[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_Membrane_Segment_Object(self.MembraneSegments[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_IntesitieDist_Object(self.Intensities_per_object[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPPhasor_Object(self.GPPhasor_polar_obj[filename][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                            if len(self.Profile[filename]) !=0:
                                if filename in self.Profile:
                                    self.plot_GProfile_Object(self.Profile[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                else:
                                    self.plot_GProfile_Object([],[],[])
                                if len(self.Cyto_Image[filename]) != 0:
                                    if filename in self.Cyto_Image:
                                        self.plot_update_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.Object_Coordinates[filename][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.horizontalScrollBar_5.setEnabled(True)
                                        self.horizontalScrollBar_5.setRange(0,self.dims[filename][len(self.dims[filename])-1]-1)
                                        self.plot_CytoObject(self.Cyto_Image[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.Update_Stats_oject_cyto(self.Object_Parameters_cyto[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPHistogramm_Object(self.Cyto_Image[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_IntesitieDist_Object(self.Cyto_Intensities_per_object[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPPhasor_Object(self.Cyto_GPPhasor_polar_obj[filename][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.plot_CytoLineProfile(self.Cytoprof[filename][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                    else:
                                        self.plot_CytoObject([],[])
                                        self.Update_Stats_oject_cyto([],[])
                                        self.plot_Cyto_GPHistogramm_Object([],[])
                                        self.plot_Cyto_IntesitieDist_Object([],[])
                                        self.plot_Cyto_GPPhasor_Object([],[],[])
                                        self.plot_CytoLineProfile([],[])
            
                    elif self.key[filename] == "Tstack":
                        if len(self.nobjects[filename]) != 0:
                            self.plot_update_GPImage_Object(self.GPImage[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()],ObjectNr,self.key[filename])
                            self.plot_GPHistogramm_Object(self.GPImage_per_object[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPImageZoom_Object(self.GPImage_per_object[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.Update_Stats_oject_membrane(self.Object_Parameters[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.Object_Morphology[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_Membrane_Segment_Object(self.MembraneSegments[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_IntesitieDist_Object(self.Intensities_per_object[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPPhasor_Object(self.GPPhasor_polar_obj[filename][self.horizontalScrollBar_2.value()],ObjectNr,self.key[filename])
                            if len(self.Profile[filename]) !=0:
                                if filename in self.Profile:
                                    self.plot_GProfile_Object(self.Profile[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                else:
                                    self.plot_GProfile_Object([],[])
                                if len(self.Cyto_Image[filename]) != 0:
                                    if filename in self.Cyto_Image:
                                        self.plot_update_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.horizontalScrollBar_5.setEnabled(True)
                                        self.horizontalScrollBar_5.setRange(0,self.dims[filename][len(self.dims[filename])-1]-1)
                                        self.plot_CytoObject(self.Cyto_Image[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.Update_Stats_oject_cyto(self.Object_Parameters_cyto[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPHistogramm_Object(self.Cyto_Image[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_IntesitieDist_Object(self.Cyto_Intensities_per_object[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPPhasor_Object(self.Cyto_GPPhasor_polar_obj[filename][self.horizontalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.plot_CytoLineProfile(self.Cytoprof[filename][self.horizontalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                    else:
                                        self.plot_CytoObject([],[])
                                        self.Update_Stats_oject_cyto([],[])
                                        self.plot_Cyto_GPHistogramm_Object([],[])
                                        self.plot_Cyto_IntesitieDist_Object([],[])
                                        self.plot_Cyto_GPPhasor_Object([],[],[])
                                        self.plot_CytoLineProfile([],[])
            
                    elif self.key[filename] == "TZstack":
                        if len(self.nobjects[filename]) != 0:
                            self.plot_update_GPImage_Object(self.GPImage[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                            self.plot_GPHistogramm_Object(self.GPImage_per_object[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPImageZoom_Object(self.GPImage_per_object[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.Update_Stats_oject_membrane(self.Object_Parameters[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.Object_Morphology[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_Membrane_Segment_Object(self.MembraneSegments[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_IntesitieDist_Object(self.Intensities_per_object[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                            self.plot_GPPhasor_Object(self.GPPhasor_polar_obj[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
    
                            if len(self.Profile[filename]) !=0:
                                if filename in self.Profile:
                                    self.plot_GProfile_Object(self.Profile[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                else:
                                    self.plot_GProfile_Object([],[])
                                if len(self.Cyto_Image[filename][0]) != 0:
                                    if filename in self.Cyto_Image:
                                        self.plot_update_Cyto_GPImage_Object(self.Cyto_GPImage[filename],self.Object_Coordinates[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.horizontalScrollBar_5.setEnabled(True)
                                        self.horizontalScrollBar_5.setRange(0,self.dims[filename][len(self.dims[filename])-1]-1)
                                        self.plot_CytoObject(self.Cyto_Image[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.Update_Stats_oject_cyto(self.Object_Parameters_cyto[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPHistogramm_Object(self.Cyto_Image[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_IntesitieDist_Object(self.Cyto_Intensities_per_object[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                        self.plot_Cyto_GPPhasor_Object(self.Cyto_GPPhasor_polar_obj[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()],ObjectNr,self.key[filename])
                                        self.plot_CytoLineProfile(self.Cytoprof[filename][self.horizontalScrollBar_2.value()][self.verticalScrollBar_2.value()][int(ObjectNr)-1],self.key[filename])
                                    else:
                                        self.plot_CytoObject([],[])
                                        self.Update_Stats_oject_cyto([],[])
                                        self.plot_Cyto_GPHistogramm_Object([],[])
                                        self.plot_Cyto_IntesitieDist_Object([],[])
                                        self.plot_Cyto_GPPhasor_Object([],[],[])
                                        self.plot_CytoLineProfile([],[])
        app.processEvents()
        
    def activate_rectangle_selector(self):
        ax = self.matplotlibwidget.axis  # Assuming this is your Matplotlib axis
        self.rectangle_selector = RectangleSelector(ax, self.on_rectangle_select,
                                            useblit=True, button=[1],
                                            minspanx=5, minspany=5,
                                            spancoords='pixels', interactive=True)
        
        self.matplotlibwidget.canvas.draw_idle()
        
    def on_rectangle_select(self, eclick, erelease):
        if self.matplotlibwidget.axis.images:
            # Get the first (and presumably only) AxesImage
            ax_image = self.matplotlibwidget.axis.images[0]
            image_data = ax_image.get_array().data  # Get the numpy array of the image data

            # Extract coordinates from the event clicks
            x1, y1 = int(eclick.xdata), int(eclick.ydata)
            x2, y2 = int(erelease.xdata), int(erelease.ydata)

            # Ensure x1 < x2 and y1 < y2 for slicing
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            # Extract the selected region from the image data
            selected_region = image_data[y1:y2, x1:x2]

            # Calculate mean and standard deviation
            mean_val = np.round(np.mean(selected_region),2)
            median_val = np.round(np.median(selected_region),2)
            std_val = np.round(np.std(selected_region),2)
            min_val = np.round(np.min(selected_region),2)
            max_val = np.round(np.max(selected_region),2)
            
            self.label_84.setText(str(mean_val))
            self.doubleSpinBox_9.setValue(mean_val)
            self.doubleSpinBox_10.setValue(mean_val)
            self.label_86.setText(str(median_val))
            self.label_85.setText(str(std_val))
            self.doubleSpinBox_7.setValue(std_val)
            self.doubleSpinBox_20.setValue(std_val)
            self.label_87.setText(str(min_val))
            self.label_88.setText(str(max_val))
        else:
            print("No image found in the plot.")
            self.plainTextEdit_1.appendPlainText(time.asctime(time.localtime()))
            self.plainTextEdit_1.appendPlainText("No image found in the plot.")

    def plot_RawImage(self,img,key): #Raw Image
        self.matplotlibwidget.axis.clear()
        ax=self.matplotlibwidget.axis
        ax.clear()
        if key !=[]:
            if key == "Zstack":
                c=self.horizontalScrollBar_4.value()
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[z,:,:,c],ax=ax,cmap="gray",cbar=False,origin='upper')
                
            if key == "Tstack":
                c=self.horizontalScrollBar_4.value()
                t=self.horizontalScrollBar_3.value()
                isns.imgplot(img[t,:,:,c],ax=ax,cmap="gray",cbar=False,origin='upper')
                
            if key == "TZstack":
                c=self.horizontalScrollBar_4.value()
                t=self.horizontalScrollBar_3.value()
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[t,z,:,:,c],ax=ax,cmap="gray",cbar=False,origin='upper')
                
            if key == "3dim":
                n=self.horizontalScrollBar_4.value()
                isns.imgplot(img[:,:,n],ax=ax,cmap="gray",cbar=False,origin='upper')
                
            self.matplotlibwidget.canvas.draw_idle() 
        else:
            ax.clear()
            self.matplotlibwidget.canvas.draw_idle()
        
        
    def plot_Mask(self,img,key): #Mask Image
        self.matplotlibwidget_2.axis.clear()
        
        ax=self.matplotlibwidget_2.axis
        ax.clear()
        if key !=[]:
            if key == "Zstack":
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[z],ax=ax,cmap="binary",cbar=False,origin='upper')
                
            if key == "Tstack":
                t=self.horizontalScrollBar_3.value()
                isns.imgplot(img[t],ax=ax,cmap="binary",cbar=False,origin='upper')
                
            if key == "TZstack":
                t=self.horizontalScrollBar_3.value()
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[t][z],ax=ax,cmap="binary",cbar=False,origin='upper')
            if key == "3dim":
                isns.imgplot(img,ax=ax,cmap="binary",cbar=False,origin='upper')
            
            self.matplotlibwidget_2.canvas.draw_idle() 
        
        else:
            ax.clear()
            self.matplotlibwidget_2.canvas.draw_idle()
            
    def plot_Cyto_Mask(self,img,key): #Mask Image
        self.matplotlibwidget_18.axis.clear()
        
        ax=self.matplotlibwidget_18.axis
        ax.clear()
        if key !=[]  and ((isinstance(img, np.ndarray) and img.size > 0) or (isinstance(img, list) and len(img) > 0)):
            if key == "Zstack":
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[z],ax=ax,cmap="binary",cbar=False,origin='upper')
                
            if key == "Tstack":
                t=self.horizontalScrollBar_3.value()
                isns.imgplot(img[t],ax=ax,cmap="binary",cbar=False,origin='upper')
                
            if key == "TZstack":
                t=self.horizontalScrollBar_3.value()
                z=self.verticalScrollBar_3.value()
                isns.imgplot(img[t][z],ax=ax,cmap="binary",cbar=False,origin='upper')
            if key == "3dim":
                isns.imgplot(img,ax=ax,cmap="binary",cbar=False,origin='upper')
            
            self.matplotlibwidget_18.canvas.draw_idle() 
        
        else:
            ax.clear()
            self.matplotlibwidget_18.canvas.draw_idle()
    
    def Update_Stats_FullImage(self,params,key):

        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                self.label_76.setText(str(params[n][0])) # rejected pixels
                self.label_73.setText(str(params[n][1])) #median
                self.label_71.setText(str(params[n][2])) #std
                self.label_69.setText(str(params[n][3]))
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                self.label_76.setText(str(params[n][0])) # rejected pixels
                self.label_73.setText(str(params[n][1])) #median
                self.label_71.setText(str(params[n][2])) #std
                self.label_69.setText(str(params[n][3]))
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                self.label_76.setText(str(params[n][m][0])) # rejected pixels
                self.label_73.setText(str(params[n][m][1])) #median
                self.label_71.setText(str(params[n][m][2])) #std
                self.label_69.setText(str(params[n][m][3]))
            
            if key == "3dim":
                self.label_76.setText(str(params[0])) # rejected pixels
                self.label_73.setText(str(params[1])) #median
                self.label_71.setText(str(params[2])) #std
                self.label_69.setText(str(params[3])) # normal intens???

    def Update_Stats_FullImage_cyto(self,params,key):

        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                self.label_77.setText(str(params[n][0])) # rejected pixels
                self.label_75.setText(str(params[n][1])) #median
                self.label_78.setText(str(params[n][2])) #std
                self.label_79.setText(str(params[n][3]))
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                self.label_77.setText(str(params[n][0])) # rejected pixels
                self.label_75.setText(str(params[n][1])) #median
                self.label_78.setText(str(params[n][2])) #std
                self.label_79.setText(str(params[n][3]))
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                self.label_77.setText(str(params[n][m][0])) # rejected pixels
                self.label_75.setText(str(params[n][m][1])) #median
                self.label_78.setText(str(params[n][m][2])) #std
                self.label_79.setText(str(params[n][m][3]))
            
            if key == "3dim":
                self.label_77.setText(str(params[0])) # rejected pixels
                self.label_75.setText(str(params[1])) #median
                self.label_78.setText(str(params[2])) #std
                self.label_79.setText(str(params[3])) # normal intens???
    
    def Update_Stats_oject_membrane(self,params,morphology,key):
        if key !=[]:
            self.label_63.setText(str(params[0])) # rejected pixels
            self.label_60.setText(str(params[1])) #median
            self.label_62.setText(str(params[2])) #std
            self.label_64.setText(str(params[3]))
            
            self.label_66.setText(str(morphology[0]))
            self.label_67.setText(str(morphology[1]))
            self.label_90.setText(str(morphology[2]))
        else:
            self.label_63.setText(str("NaN")) # rejected pixels
            self.label_60.setText(str("NaN")) #median
            self.label_62.setText(str("NaN")) #std
            self.label_64.setText(str("NaN"))
            
            self.label_66.setText(str("NaN"))
            self.label_67.setText(str("NaN"))
            self.label_90.setText(str("NaN"))
            
                
    def Update_Stats_oject_cyto(self,params,key):
        if key !=[]:
            self.label_138.setText(str(params[0])) # rejected pixels
            self.label_140.setText(str(params[1])) #median
            self.label_139.setText(str(params[2])) #std
            self.label_137.setText(str(params[3]))
        else:
            self.label_138.setText(str("NaN")) # rejected pixels
            self.label_140.setText(str("NaN")) #median
            self.label_139.setText(str("NaN")) #std
            self.label_137.setText(str("NaN"))


    def plot_GPImage(self,img,key): # GP image
        self.matplotlibwidget_3.figure.clf()
        self.matplotlibwidget_3.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_3.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_3.axis = ax 
        ax=self.matplotlibwidget_3.axis
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
    
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=copy.deepcopy(img[n])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n][m])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            if key == "3dim":
                img1=copy.deepcopy(img)
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            fig=self.matplotlibwidget_3.figure
            fig.tight_layout()
            self.matplotlibwidget_3.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_3.figure.clf()
            self.matplotlibwidget_3.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_3.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_3.axis = ax 
            self.matplotlibwidget_3.canvas.draw_idle()

    def plot_Cyto_GPImage(self,img,key): # GP image
        
        self.matplotlibwidget_19.figure.clf()
        self.matplotlibwidget_19.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_19.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_19.axis = ax 
        ax=self.matplotlibwidget_19.axis
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
    
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=copy.deepcopy(img[n])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n][m])
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            if key == "3dim":
                img1=copy.deepcopy(img)
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            fig=self.matplotlibwidget_19.figure
            fig.tight_layout()
            self.matplotlibwidget_19.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_19.figure.clf()
            self.matplotlibwidget_19.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_19.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_19.axis = ax 
            self.matplotlibwidget_19.canvas.draw_idle()

    def plot_GPHistogramm(self,img,key): # GP Histogramm
        self.matplotlibwidget_4.axis.clear()
        
        ax=self.matplotlibwidget_4.axis
        ax.clear()
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n])
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=copy.deepcopy(img[n])
    
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

    
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n][m])
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

                
            if key == "3dim":
                img1=copy.deepcopy(img)
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})
            
            
            sns.histplot(data=df, x="GP-Value",ax=ax,bins=np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+self.doubleSpinBox_4.value(),self.doubleSpinBox_4.value()))
            ax.set_xlabel(r'$\beta$-Value')
            ax.set_ylabel('Counts')
            fig=self.matplotlibwidget_4.figure
            fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.2)
            fig.tight_layout()
            
            self.matplotlibwidget_4.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_4.canvas.draw_idle()
        
    def plot_Cyto_GPHistogramm(self,img,key): # GP Histogramm
        self.matplotlibwidget_20.axis.clear()
        
        ax=self.matplotlibwidget_20.axis
        ax.clear()
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n])
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=copy.deepcopy(img[n])
    
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

    
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=copy.deepcopy(img[n][m])
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})

                
            if key == "3dim":
                img1=copy.deepcopy(img)
                flattenedImage=img1.flatten()
                flattenedImage = flattenedImage[flattenedImage != 2]
                df = pd.DataFrame({"GP-Value": flattenedImage})
            
            
            sns.histplot(data=df, x="GP-Value",ax=ax,bins=np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+self.doubleSpinBox_19.value(),self.doubleSpinBox_19.value()))
            ax.set_xlabel(r'$\beta$-Value')
            ax.set_ylabel('Counts')
            
            fig=self.matplotlibwidget_20.figure
            fig.tight_layout()
            
            self.matplotlibwidget_20.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_4.canvas.draw_idle()
        
    def plot_GPPhasor(self,phase,key): # GP Phasor
        self.matplotlibwidget_6.axis.clear()
        ax=self.matplotlibwidget_6.axis
        ax.clear()
        
        if key !=[] and isinstance(phase[0], np.ndarray):
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                phase1=phase[n]
                
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                phase1=phase[n]
                
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                
                phase1=phase[n][m]
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "3dim":
                if phase[0].ndim == 2:
                    amp=phase[0][:,0]
                    ph=phase[1][:,0]
                
                if phase[0].ndim == 1:
                    amp=phase[0][:]
                    ph=phase[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                #df = pd.DataFrame({'amplitude': np.sqrt(np.square(x)+np.square(y)), 'phase': np.arctan(np.divide(y,x))})
    
            
            ax.grid(False)
            rbins = np.linspace(0,df["amplitude"].max(), 100)
            abins = np.linspace(0,2*np.pi, 360)    
            hist, _, _ = np.histogram2d(df["phase"], df["amplitude"], bins=(abins, rbins))
            A, R = np.meshgrid(abins, rbins)
            ax.pcolormesh(A, R, hist.T, cmap="YlOrRd")
            ax.grid(True)
            ax.set_rlabel_position(0)
            
            fig=self.matplotlibwidget_6.figure
            fig.tight_layout()
            
            self.matplotlibwidget_6.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_6.canvas.draw_idle()
            
    def plot_Cyto_GPPhasor(self,phase,key): # GP Phasor
        self.matplotlibwidget_22.axis.clear()
        ax=self.matplotlibwidget_22.axis
        ax.clear()
        
        if key !=[] and isinstance(phase[0], np.ndarray):
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                phase1=phase[n]
                
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                phase1=phase[n]
                
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                
                phase1=phase[n][m]
                if phase1[0].ndim == 2:
                    amp=phase1[0][:,0]
                    ph=phase1[1][:,0]
                
                if phase1[0].ndim == 1:
                    amp=phase1[0][:]
                    ph=phase1[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                
            if key == "3dim":
                if phase[0].ndim == 2:
                    amp=phase[0][:,0]
                    ph=phase[1][:,0]
                
                if phase[0].ndim == 1:
                    amp=phase[0][:]
                    ph=phase[1][:]
                ph=np.where(ph < 0, ph + 2*np.pi, ph)
                df = pd.DataFrame({'amplitude': amp, 'phase': ph})
                #df = pd.DataFrame({'amplitude': np.sqrt(np.square(x)+np.square(y)), 'phase': np.arctan(np.divide(y,x))})
    
            
            ax.grid(False)
            rbins = np.linspace(0,df["amplitude"].max(), 100)
            abins = np.linspace(0,2*np.pi, 360)    
            hist, _, _ = np.histogram2d(df["phase"], df["amplitude"], bins=(abins, rbins))
            A, R = np.meshgrid(abins, rbins)
            ax.pcolormesh(A, R, hist.T, cmap="YlOrRd")
            ax.grid(True)
            ax.set_rlabel_position(0)
            
            fig=self.matplotlibwidget_22.figure
            fig.tight_layout()
            
            self.matplotlibwidget_22.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_6.canvas.draw_idle()
        
    def plot_IntesitieDist(self,img,key): # GP Phasor
        self.matplotlibwidget_7.axis.clear()
        ax=self.matplotlibwidget_7.axis
        ax.clear()
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=img[n]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=img[n]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
                
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=img[n][m]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
            
            if key == "3dim":
                df = pd.DataFrame({"wavelength": img[0],"intensites":img[1]})
            
            sns.barplot(data=df, x="wavelength", y="intensites",hue="wavelength",ax=ax, palette="Reds",legend=False)
            ax.xaxis.set_major_locator(FixedLocator(ax.get_xticks()))
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            ax.set_xlabel('Channels')
            ax.set_ylabel('Normalized Intensities')
            fig=self.matplotlibwidget_7.figure
            fig.tight_layout()
            self.matplotlibwidget_7.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_7.canvas.draw_idle()
            
    def plot_Cyto_IntesitieDist(self,img,key): # GP Phasor
        self.matplotlibwidget_21.axis.clear()
        ax=self.matplotlibwidget_21.axis
        ax.clear()
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar.value()
                img1=img[n]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
                
            if key == "Tstack":
                n=self.horizontalScrollBar.value()
                img1=img[n]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
                
            if key == "TZstack":
                n=self.horizontalScrollBar.value()
                m=self.verticalScrollBar.value()
                img1=img[n][m]
                df = pd.DataFrame({"wavelength": img1[0],"intensites":img1[1]})
            
            if key == "3dim":
                df = pd.DataFrame({"wavelength": img[0],"intensites":img[1]})
            
            sns.barplot(data=df, x="wavelength", y="intensites",hue="wavelength",ax=ax, palette="Reds",legend=False)
            ax.xaxis.set_major_locator(FixedLocator(ax.get_xticks()))
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            ax.set_xlabel('Channels')
            ax.set_ylabel('Normalized Intesities')
            fig=self.matplotlibwidget_21.figure
            fig.tight_layout()
            self.matplotlibwidget_21.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_7.canvas.draw_idle()
        
    def plot_GPImage_Object(self,img,key,Object_Coordinates): # GP image
        self.matplotlibwidget_5.figure.clf()
        self.matplotlibwidget_5.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_5.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_5.axis = ax 
        ax=self.matplotlibwidget_5.axis
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            if key == "Tstack":
                n=self.horizontalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            if key == "TZstack":
                n=self.horizontalScrollBar_2.value()
                m=self.verticalScrollBar_2.value()
                img1=img[n][m]
                img1[img[n][m]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            if key == "3dim":
                img[img==2]=np.nan
                isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            i=1
            for n in Object_Coordinates:
                ax.text(n[1],n[0],i,verticalalignment='center',color="red")
                i=i+1
            
            fig=self.matplotlibwidget_5.figure
            fig.tight_layout()
            self.matplotlibwidget_5.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_5.figure.clf()
            self.matplotlibwidget_5.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_5.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_5.axis = ax 
            self.matplotlibwidget_5.canvas.draw_idle()

    def plot_Cyto_GPImage_Object(self,img,key,Object_Coordinates): # GP image
        self.matplotlibwidget_23.figure.clf()
        self.matplotlibwidget_23.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_23.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_23.axis = ax 
        ax=self.matplotlibwidget_23.axis
        
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            if key == "Tstack":
                n=self.horizontalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            if key == "TZstack":
                n=self.horizontalScrollBar_2.value()
                m=self.verticalScrollBar_2.value()
                img1=img[n][m]
                img1[img[n][m]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            if key == "3dim":
                img[img==2]=np.nan
                isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            i=1
            for n in Object_Coordinates:
                ax.text(n[1],n[0],i,verticalalignment='center',color="red")
                i=i+1
            
            fig=self.matplotlibwidget_23.figure
            fig.tight_layout()

            self.matplotlibwidget_23.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_23.figure.clf()
            self.matplotlibwidget_23.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_23.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_23.axis = ax 
            self.matplotlibwidget_23.canvas.draw_idle()
        
    def plot_update_GPImage_Object(self,img,Object_Coordinates,ObjectNr,key): # GP image
        self.matplotlibwidget_5.figure.clf()
        self.matplotlibwidget_5.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_5.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_5.axis = ax 
        ax=self.matplotlibwidget_5.axis
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            if key == "Tstack":
                n=self.horizontalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            if key == "TZstack":
                n=self.horizontalScrollBar_2.value()
                m=self.verticalScrollBar_2.value()
                img1=img[n][m]
                img1[img[n][m]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            if key == "3dim":
                img[img==2]=np.nan
                isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            
            i=1
            for n in Object_Coordinates:
                if i != int(ObjectNr):
                    ax.text(n[1],n[0],i,verticalalignment='center',color="red")
                    i=i+1
                else:
                     ax.text(n[1],n[0],i,verticalalignment='center',color="yellow")
                     i=i+1
                
            fig=self.matplotlibwidget_5.figure
            fig.tight_layout()

            self.matplotlibwidget_5.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_5.figure.clf()
            self.matplotlibwidget_5.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_5.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_5.axis = ax 
            self.matplotlibwidget_5.canvas.draw_idle()

    def plot_update_Cyto_GPImage_Object(self,img,Object_Coordinates,ObjectNr,key): # GP image
        ax=self.matplotlibwidget_23.axis
        self.matplotlibwidget_23.figure.clf()
        self.matplotlibwidget_23.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_23.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_23.axis = ax 
        ax=self.matplotlibwidget_23.axis
        if key !=[]:
            if key == "Zstack":
                n=self.verticalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            if key == "Tstack":
                n=self.horizontalScrollBar_2.value()
                img1=img[n]
                img1[img[n]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            if key == "TZstack":
                n=self.horizontalScrollBar_2.value()
                m=self.verticalScrollBar_2.value()
                img1=img[n][m]
                img1[img[n][m]==2]=np.nan
                isns.imgplot(img1,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            if key == "3dim":
                img[img==2]=np.nan
                isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            
            i=1
            for n in Object_Coordinates:
                if i != int(ObjectNr):
                    ax.text(n[1],n[0],i,verticalalignment='center',color="red")
                    i=i+1
                else:
                     ax.text(n[1],n[0],i,verticalalignment='center',color="yellow")
                     i=i+1
                
            fig=self.matplotlibwidget_23.figure
            fig.tight_layout()

            self.matplotlibwidget_23.canvas.draw_idle() 
            
        else:
            self.matplotlibwidget_23.figure.clf()
            self.matplotlibwidget_23.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_23.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_23.axis = ax 
            self.matplotlibwidget_23.canvas.draw_idle()
        
    def plot_GPImageZoom_Object(self,GPImage_per_object,key): # GP Histogramm object
        ax=self.matplotlibwidget_8.axis
        self.matplotlibwidget_8.figure.clf()
        self.matplotlibwidget_8.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_8.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_8.axis = ax 
        ax=self.matplotlibwidget_8.axis
        #GPImage_per_object
        if key !=[]:
            img=GPImage_per_object
            self.matplotlibwidget_8.axis.clear()
            ax.set_facecolor("#2D2D2D")
            isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_6.value(), vmin=self.doubleSpinBox_5.value(),cbar_ticks =np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8,abs(abs(self.doubleSpinBox_5.value())+abs(self.doubleSpinBox_6.value()))/8),origin='upper')
            fig=self.matplotlibwidget_8.figure
            fig.tight_layout()
            self.matplotlibwidget_8.canvas.draw_idle() 
        else:
            self.matplotlibwidget_8.figure.clf()
            self.matplotlibwidget_8.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_8.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_8.axis = ax 
            self.matplotlibwidget_8.canvas.draw_idle()
            
    def plot_Membrane_Segment_Object(self,SegmentImage,key): # GP Histogramm object
        ax=self.matplotlibwidget_24.axis
        self.matplotlibwidget_24.figure.clf()
        self.matplotlibwidget_24.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_24.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_24.axis = ax 
        ax=self.matplotlibwidget_24.axis
        
        if SegmentImage:
            if key !=[] and ((isinstance(SegmentImage[0], np.ndarray) and SegmentImage[0].size > 0) or (isinstance(SegmentImage[0], list) and len(SegmentImage[0]) > 0)):
                img=SegmentImage[0]
                
                unique_segments = np.unique(img)
                max_segment = unique_segments.max()
                # Create a list of colors for the colormap, one for each segment, adjusted for the offset in color_map
                colors = [color_map[(segment + 1) % len(color_map)] for segment in range(max_segment + 1)]
                custom_cmap = ListedColormap(colors)
                
                ax.set_facecolor("#2D2D2D")
                isns.imgplot(img,cmap=custom_cmap,ax=ax,cbar=False,interpolation='nearest')
                fig=self.matplotlibwidget_24.figure
                fig.tight_layout()
                self.matplotlibwidget_24.canvas.draw_idle() 
            else:
                self.matplotlibwidget_24.figure.clf()
                self.matplotlibwidget_24.figure.patch.set_facecolor('#434343')
                ax = self.matplotlibwidget_12.figure.add_subplot(111)
                ax.set_facecolor('#2D2D2D')
                self.matplotlibwidget_24.axis = ax 
                self.matplotlibwidget_24.canvas.draw_idle()
        else:
            self.matplotlibwidget_24.figure.clf()
            self.matplotlibwidget_24.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_12.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_24.axis = ax 
            self.matplotlibwidget_24.canvas.draw_idle()
        
    def plot_GPHistogramm_Object(self,GPImage_per_object,key): # GP Histogramm object
        ax=self.matplotlibwidget_9.axis
        if key !=[]:
            img=GPImage_per_object
            self.matplotlibwidget_9.axis.clear()
            flattenedImage=img.flatten()
            flattenedImage = flattenedImage[flattenedImage != 2]
            df = pd.DataFrame({"GP-Value": flattenedImage})
            sns.histplot(data=df, x="GP-Value",ax=ax,bins=np.arange(self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value()+self.doubleSpinBox_4.value(),self.doubleSpinBox_4.value()))
            ax.set_xlabel(r'$\beta$-Value')
            ax.set_ylabel('Counts')
            fig=self.matplotlibwidget_9.figure
            fig.tight_layout()
            self.matplotlibwidget_9.canvas.draw_idle() 
        else:
            ax.clear()
            self.matplotlibwidget_9.canvas.draw_idle()
        
    def plot_IntesitieDist_Object(self,intensites,key): # GP Phasor
        self.matplotlibwidget_10.axis.clear()
        ax=self.matplotlibwidget_10.axis
        if key !=[]:
            df = pd.DataFrame({"wavelength": intensites[0],"intensites":intensites[1]})
            sns.barplot(data=df, x="wavelength", y="intensites",hue="wavelength",ax=ax, palette="Reds",legend=False)
            ax.xaxis.set_major_locator(FixedLocator(ax.get_xticks()))
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            ax.set_xlabel('Channels')
            ax.set_ylabel('Normalized Intensites')
            fig=self.matplotlibwidget_10.figure
            fig.tight_layout()
            self.matplotlibwidget_10.canvas.draw_idle() 
        else:
            ax.clear()
            self.matplotlibwidget_10.canvas.draw_idle()
        
    def plot_GPPhasor_Object(self,phase,ObjectNr,key): # GP Phasor
        self.matplotlibwidget_11.axis.clear()
        ax=self.matplotlibwidget_11.axis
        ax.clear()
        if key !=[] and isinstance(phase[int(ObjectNr)-1][0], np.ndarray):
            ph=phase[int(ObjectNr)-1][1][:]
            ph=np.where(ph < 0, ph + 2*np.pi, ph)
            df = pd.DataFrame({'amplitude': phase[int(ObjectNr)-1][0][:], 'phase': ph})
            ax.grid(False)
            rbins = np.linspace(0,df["amplitude"].max(), 100)
            abins = np.linspace(0,2*np.pi, 360)    
            hist, _, _ = np.histogram2d(df["phase"], df["amplitude"], bins=(abins, rbins))
            A, R = np.meshgrid(abins, rbins)
            ax.pcolormesh(A, R, hist.T, cmap="YlOrRd")
            ax.grid(True)
            ax.set_rlabel_position(0)
            fig=self.matplotlibwidget_11.figure
            fig.tight_layout()
            self.matplotlibwidget_11.canvas.draw_idle() 
        else:
            ax.clear()
            self.matplotlibwidget_11.canvas.draw_idle()
        
    def plot_GProfile_Object(self,profile,key):
        self.matplotlibwidget_12.figure.clf()
        self.matplotlibwidget_12.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_12.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_12.axis = ax 
        ax=self.matplotlibwidget_12.axis
        if key !=[] and profile:
            if profile[0].shape[1] >= 5:
                
                df = pd.DataFrame({"x": profile[0][:,0],"P-Value":profile[0][:,3], "Segment": profile[0][:,4].astype(int)})
                sns.lineplot(data=df, x="x", y="P-Value",ax=ax,color=sns.color_palette("deep")[0])
                ax.set_ylabel(r'$\beta$-Value', color=sns.color_palette("deep")[0])
                
                for segment in np.unique(df['Segment']):
                    # Adjust segment by +1 for color mapping, loop back to 1 if it exceeds the length of the color_map
                    adjusted_segment = segment % len(color_map)+1
                    segment_indices = df[df['Segment'] == segment].index
                    if len(segment_indices) > 0:
                        ax.axvspan(df['x'].iloc[segment_indices[0]], df['x'].iloc[segment_indices[-1]], color=color_map[adjusted_segment], alpha=0.3)
                    
                if profile[0].shape[1] > 5:
                    df1 = pd.DataFrame({"x": profile[0][:,0],"Colocalization":profile[0][:,5]})
                    ax2 = ax.twinx()
                    sns.lineplot(data=df1, x="x", y="Colocalization",ax=ax2, color="red")
                    ax2.set_ylabel('Colocalization', color='red')
            else:
                df = pd.DataFrame({"x": profile[0][:,0],"Intensity":profile[0][:,2], "Segment": profile[0][:,3].astype(int)})
                sns.lineplot(data=df, x="x", y="Intensity",ax=ax,color=sns.color_palette("deep")[0])
                ax.set_ylabel('Intensity', color=sns.color_palette("deep")[0])
                
                for segment in np.unique(df['Segment']):
                    # Adjust segment by +1 for color mapping, loop back to 1 if it exceeds the length of the color_map
                    adjusted_segment = segment % len(color_map)+1
                    segment_indices = df[df['Segment'] == segment].index
                    if len(segment_indices) > 0:
                        ax.axvspan(df['x'].iloc[segment_indices[0]], df['x'].iloc[segment_indices[-1]], color=color_map[adjusted_segment], alpha=0.3)
                    
                if profile[0].shape[1] > 4:
                    df1 = pd.DataFrame({"x": profile[0][:,0],"Colocalization":profile[0][:,5]})
                    ax2 = ax.twinx()
                    sns.lineplot(data=df1, x="x", y="Colocalization",ax=ax2, color="red")
                    ax2.set_ylabel('Colocalization', color='red')


            
            ax.grid(which='both') 
            ax.set_xlim(left=0)
            fig=self.matplotlibwidget_12.figure
            fig.tight_layout()
            self.matplotlibwidget_12.canvas.draw_idle() 
        else:
            self.matplotlibwidget_12.figure.clf()
            self.matplotlibwidget_12.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_12.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_12.axis = ax 
            self.matplotlibwidget_12.canvas.draw_idle()
        
    def plot_CytoObject(self,img,key): # GP Histogramm object
        self.matplotlibwidget_14.figure.clf()
        self.matplotlibwidget_14.figure.patch.set_facecolor('#434343')
        ax = self.matplotlibwidget_14.figure.add_subplot(111)
        ax.set_facecolor('#2D2D2D')
        self.matplotlibwidget_14.axis = ax 
        ax=self.matplotlibwidget_14.axis
        if key != [] and ((isinstance(img, np.ndarray) and img.size > 0) or (isinstance(img, list) and len(img) > 0)):
            img=img
            ax.set_facecolor("#2D2D2D")
            #img[img==2]=np.nan
            isns.imgplot(img,ax=ax,cmap="viridis",cbar=True,vmax =self.doubleSpinBox_18.value(), vmin=self.doubleSpinBox_17.value(),cbar_ticks =np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8,abs(abs(self.doubleSpinBox_17.value())+abs(self.doubleSpinBox_18.value()))/8),origin='upper')
            fig=self.matplotlibwidget_14.figure
            fig.tight_layout()
            self.matplotlibwidget_14.canvas.draw_idle() 
        else:
            self.matplotlibwidget_14.figure.clf()
            self.matplotlibwidget_14.figure.patch.set_facecolor('#434343')
            ax = self.matplotlibwidget_14.figure.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            self.matplotlibwidget_14.axis = ax 
            self.matplotlibwidget_14.canvas.draw_idle()
        
    def plot_CytoLineProfile(self,Cytoprof,key): # GP Histogramm object
        ax=self.matplotlibwidget_13.axis
        if key !=[] and Cytoprof and Cytoprof != [[]]:
            img=Cytoprof[0][2][self.horizontalScrollBar_5.value(),:,:].T
            self.matplotlibwidget_13.axis.clear()
            ax.clear()
            ax.set_facecolor("black")
            isns.imgplot(img,ax=ax,cmap="YlGnBu_r",cbar=False) #origin='lower'
            ax.set_aspect("auto")
            fig=self.matplotlibwidget_13.figure
            fig.tight_layout()
            self.matplotlibwidget_13.canvas.draw_idle() 
        else:
            ax.clear()
            ax.set_facecolor("#2D2D2D")
            self.matplotlibwidget_13.canvas.draw_idle()
            
            
    def plot_Cyto_GPHistogramm_Object(self,GPImage_per_object,key): # GP Histogramm object
        ax=self.matplotlibwidget_17.axis
        if key !=[] and ((isinstance(GPImage_per_object, np.ndarray) and GPImage_per_object.size > 0) or (isinstance(GPImage_per_object, list) and len(GPImage_per_object) > 0)):
            img=GPImage_per_object
            self.matplotlibwidget_17.axis.clear()
            flattenedImage=img.flatten()
            flattenedImage = flattenedImage[flattenedImage != 2]
            df = pd.DataFrame({"GP-Value": flattenedImage})
            sns.histplot(data=df, x="GP-Value",ax=ax,bins=np.arange(self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value()+self.doubleSpinBox_19.value(),self.doubleSpinBox_19.value()))
            ax.set_xlabel(r'$\beta$-Value')
            ax.set_ylabel('Counts')
            fig=self.matplotlibwidget_17.figure
            fig.tight_layout()
            self.matplotlibwidget_17.canvas.draw_idle() 
        else:
            ax.clear()
            self.matplotlibwidget_17.canvas.draw_idle()
        
    def plot_Cyto_IntesitieDist_Object(self,intensites,key): 
        self.matplotlibwidget_15.axis.clear()
        ax=self.matplotlibwidget_15.axis
        
        if key !=[] and intensites:
            df = pd.DataFrame({"wavelength": intensites[0],"intensites":intensites[1]})
            sns.barplot(data=df, x="wavelength", y="intensites",hue="wavelength",ax=ax, palette="Reds",legend=False)
            ax.xaxis.set_major_locator(FixedLocator(ax.get_xticks()))
            ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
            ax.set_xlabel('Channels')
            ax.set_ylabel('Normalized Intensities')
            fig=self.matplotlibwidget_15.figure
            fig.tight_layout()
            self.matplotlibwidget_15.canvas.draw_idle() 
            
        else:
            ax.clear()
            self.matplotlibwidget_15.canvas.draw_idle()
        
    def plot_Cyto_GPPhasor_Object(self,phase,ObjectNr,key): # GP Phasor
        self.matplotlibwidget_16.axis.clear()
        ax=self.matplotlibwidget_16.axis
        ax.clear()
        if key !=[] and isinstance(phase[int(ObjectNr)-1][0], np.ndarray):
            ph=phase[int(ObjectNr)-1][1][:]
            ph=np.where(ph < 0, ph + 2*np.pi, ph)
            df = pd.DataFrame({'amplitude': phase[int(ObjectNr)-1][0][:], 'phase': ph})
            
            ax.grid(False)
            rbins = np.linspace(0,df["amplitude"].max(), 100)
            abins = np.linspace(0,2*np.pi, 360)    
            hist, _, _ = np.histogram2d(df["phase"], df["amplitude"], bins=(abins, rbins))
            A, R = np.meshgrid(abins, rbins)
            ax.pcolormesh(A, R, hist.T, cmap="YlOrRd")
            ax.grid(True)
            ax.set_rlabel_position(0)
            
            fig=self.matplotlibwidget_16.figure
            fig.tight_layout()
            self.matplotlibwidget_16.canvas.draw_idle() 
        
        else:
            ax.clear()
            self.matplotlibwidget_16.canvas.draw_idle()

        
    def autoCutOffEnable(self):
        pass
#         self.doubleSpinBox_3.setEnabled(self.checkBox_9.checkState())
        
    def singleImageEnable(self):    
        self.pushButton_3.setEnabled(self.checkBox.checkState()) 
        # remove singe image button 
        # check test if one or more are selecten than active 
        
    def profilerEnable(self):    
        self.comboBox_5.setEnabled(self.checkBox_8.checkState())
        self.spinBox_7.setEnabled(self.checkBox_8.checkState())
        self.spinBox_8.setEnabled(self.checkBox_8.checkState())
        self.checkBox_9.setEnabled(self.checkBox_8.checkState())
        self.checkBox_14.setEnabled(self.checkBox_8.checkState())
        self.doubleSpinBox_3.setEnabled(self.checkBox_8.checkState())
        if self.checkBox_8.checkState()==False:
            self.checkBox_9.setCheckState(self.checkBox_8.checkState())
            self.checkBox_14.setCheckState(self.checkBox_8.checkState())
        
    def cytoprofilerEnable(self):    
        if self.checkBox.checkState()==False:
            self.checkBox_9.setCheckState(self.checkBox.checkState())

        
    def removeClusterEnable(self):  
        self.comboBox_5.setEnabled(self.checkBox_8.checkState())
        self.doubleSpinBox_3.setEnabled(self.checkBox_8.checkState())
        self.spinBox_7.setEnabled(self.checkBox_8.checkState())
        self.spinBox_8.setEnabled(self.checkBox_8.checkState())

        
    


            
    def threholdEnable(self):  
        if self.comboBox_3.currentText() == 'Manual':
            self.spinBox.setEnabled(True) 

        elif self.comboBox_3.currentText() == 'Otsu':
            self.spinBox.setEnabled(False) 

    
    def threholdEnable_cyto(self):  
        if self.comboBox_21.currentText() == 'Manual':
            self.spinBox_15.setEnabled(True) 

            
        elif self.comboBox_21.currentText() == 'Otsu':
            self.spinBox_15.setEnabled(False) 

        
    def compressEnable(self):   
        self.doubleSpinBox.setEnabled(self.checkBox_3.checkState()) 
        
    def compressEnable_cyto(self):   
        self.doubleSpinBox_23.setEnabled(self.checkBox_32.checkState()) 
        
    def dilateEnable(self):   
        self.comboBox_4.setEnabled(self.checkBox_6.checkState())
        self.spinBox_4.setEnabled(self.checkBox_6.checkState()) 
        self.spinBox_5.setEnabled(self.checkBox_6.checkState()) 

    def dilateEnable_cyto(self):   
        self.comboBox_22.setEnabled(self.checkBox_37.checkState())
        self.spinBox_16.setEnabled(self.checkBox_37.checkState()) 
        self.spinBox_17.setEnabled(self.checkBox_37.checkState())
        
    def fillHolesEnable(self):   
        self.doubleSpinBox_13.setEnabled(self.checkBox_5.checkState()) 
        
    def fillHolesEnable_cyto(self):   
        self.doubleSpinBox_22.setEnabled(self.checkBox_35.checkState()) 
        
    def removeObjectsEnable(self):   
        self.spinBox_2.setEnabled(self.checkBox_4.checkState()) 

    def removeObjectsEnable_cyto(self):   
        self.spinBox_18.setEnabled(self.checkBox_34.checkState()) 
        
    def threholdChannelEnable(self):
        self.comboBox_18.setEnabled(self.checkBox_27.checkState())
            
    def threholdChannelEnable_cyto(self):
        self.comboBox_23.setEnabled(self.checkBox_36.checkState())
        
    def gaussEnable(self):
        self.doubleSpinBox_12.setEnabled(self.checkBox_26.checkState())
        
    def gaussEnable_cyto(self):
        self.doubleSpinBox_11.setEnabled(self.checkBox_33.checkState())


        
    def objectDetectionEnable(self):    
        self.checkBox_8.setEnabled(self.checkBox_2.checkState())
        self.comboBox_5.setEnabled(self.checkBox_8.checkState())
        self.doubleSpinBox_3.setEnabled(self.checkBox_8.checkState())
        self.spinBox_7.setEnabled(self.checkBox_8.checkState())
        self.spinBox_8.setEnabled(self.checkBox_8.checkState())
        self.checkBox_7.setEnabled(self.checkBox_2.checkState())

        
        if self.checkBox_2.checkState()==False:
            self.checkBox_8.setEnabled(self.checkBox_2.checkState())
            self.comboBox_5.setEnabled(self.checkBox_2.checkState())
            self.doubleSpinBox_3.setEnabled(self.checkBox_2.checkState())
            self.spinBox_7.setEnabled(self.checkBox_2.checkState())
            self.spinBox_8.setEnabled(self.checkBox_2.checkState())
            self.checkBox_8.setCheckState(False)
            self.checkBox_7.setCheckState(False)
            self.checkBox_8.setCheckState(False)
            self.checkBox_9.setCheckState(self.checkBox_8.checkState())   



    def SaveAllInJSON(self,filename,savepath):
        ui_settings = {
            "filenme":filename,
            "savepath":savepath,
            "Date":time.asctime(time.localtime()),
            "Metadata":self.Metadata[filename],
            "General Settings":{
                "Object Detection":self.checkBox_2.isChecked(),
                "Object Linearization":self.checkBox_7.isChecked()
                    },
            "Membrane Settings":{
                "Membrane Profiler":self.checkBox_8.isChecked(),
                "Colocalzation":self.checkBox_14.isChecked(),
                "Colocalzation Channel":(self.comboBox_8.currentText()),
                "Channel A": (self.comboBox.currentText()),
                "Channel B": (self.comboBox_2.currentText()),
                "Channel C": (self.comboBox_6.currentText()),
                "Channel D": (self.comboBox_7.currentText()),
                "Equation": self.plainTextEdit.toPlainText(),
                "Specific Channel for Masking":self.checkBox_27.isChecked(),
                "Specific Channel for Masking Value":"NaN" if not self.checkBox_27.isChecked() else ((self.comboBox_18.currentText())),
                "Thresholding Type":self.comboBox_3.currentText(),
                "Manual Cutoff Level":(self.spinBox.value()),
                "Signal to Noise Ratio":self.doubleSpinBox_8.value(),
                "Background Compensation": self.checkBox_15.isChecked(),
                "Background Mean": "NaN" if not self.checkBox_15.isChecked() else (self.doubleSpinBox_9.value()),
                "Background Standarddeviation": 1 if not self.checkBox_15.isChecked() else (self.doubleSpinBox_7.value()),
                "Compression": (self.checkBox_3.isChecked()),
                "Compression Value": (self.doubleSpinBox.value()),
                "Remove Object":(self.checkBox_4.isChecked()),
                "Remove Object Value":"NaN" if not self.checkBox_4.isChecked() else (self.spinBox_2.value()), #removeobjet size
                "Fill Holes":(self.checkBox_5.isChecked()),
                "Fill Holes Value":"NaN" if not self.checkBox_5.isChecked() else (self.doubleSpinBox_13.value()), #dilate hole size
                "Dilate": (self.checkBox_6.isChecked()),
                "Dilation Shape": self.comboBox_4.currentText(),
                "Dilation Dimmension 1":(self.spinBox_4.value()), #shpae dim1
                "Dilation Dimmension 2":(self.spinBox_5.value()), #shpae dim2
                "Gauss Filter":self.checkBox_26.isChecked(),
                "Gauss Filter Value":"NaN" if not self.checkBox_26.isChecked() else (self.doubleSpinBox_12.value()),
                "Binning Values [min,max,step]": [self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value(),self.doubleSpinBox_4.value()],
                "Global Slice Masking": self.checkBox_24.isChecked(),
                "Individual Slice MaskingSettings":self.Membrane_Maskdata[filename],
                    },
            "Cytosol Settings":{
                "Cytosol Measurement":self.checkBox.isChecked(),
                "Channel A": (self.comboBox_13.currentText()),
                "Channel B": (self.comboBox_14.currentText()),
                "Channel C": (self.comboBox_15.currentText()),
                "Channel D": (self.comboBox_16.currentText()),
                "Equation": self.plainTextEdit_2.toPlainText(),
                "Specific Channel for Masking":self.checkBox_36.isChecked(),
                "Specific Channel for Masking Value":"NaN" if not self.checkBox_36.isChecked() else ((self.comboBox_23.currentText())),
                "Thresholding Type":self.comboBox_21.currentText(),
                "Manual Cutoff Level":(self.spinBox_15.value()),
                "Signal to Noise Ratio":self.doubleSpinBox_21.value(),
                "Background Compensation": self.checkBox_16.isChecked(),
                "Background Mean": "NaN" if not self.checkBox_16.isChecked() else (self.doubleSpinBox_10.value()),
                "Background Standarddeviation": 1 if not self.checkBox_16.isChecked() else (self.doubleSpinBox_20.value()),
                "Compression": (self.checkBox_32.isChecked()),
                "Compression Value": (self.doubleSpinBox_23.value()),
                "Remove Object":(self.checkBox_34.isChecked()),
                "Remove Object Value":"NaN" if not self.checkBox_34.isChecked() else (self.spinBox_18.value()), #removeobjet size
                "Fill Holes":(self.checkBox_35.isChecked()),
                "Fill Holes Value":"NaN" if not self.checkBox_35.isChecked() else (self.doubleSpinBox_22.value()), #dilate hole size
                "Dilate": (self.checkBox_37.isChecked()),
                "Dilation Shape": self.comboBox_22.currentText(),
                "Dilation Dimmension 1":(self.spinBox_17.value()), #shpae dim1
                "Dilation Dimmension 2":(self.spinBox_16.value()), #shpae dim2
                "Gauss Filter":self.checkBox_33.isChecked(),
                "Gauss Filter Value":"NaN" if not self.checkBox_33.isChecked() else (self.doubleSpinBox_11.value()),
                "Binning Values [min,max,step]": [self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value(),self.doubleSpinBox_19.value()],
                "Global Slice Masking": self.checkBox_31.isChecked(),
                "Individual Slice MaskingSettings": self.Cyto_Maskdata[filename]
                    },
            "Advanced Settings":{
                "Skeleton Debranching":(self.spinBox_3.value()),
                "Tolerance Value 0":self.doubleSpinBox_2.value(),
                "Tolerance Value 1":(self.spinBox_6.value()),
                "Recentering":self.checkBox_10.isChecked(),
                "dim_line":self.spinBox_9.value(),
                "Integrating Element":self.comboBox_5.currentText(),
                "Integrating Element Dimmension 1":(self.spinBox_7.value()),
                "Integrating Element Dimmension 2":(self.spinBox_8.value()),
                "P-Value Threshold Auto Cut Off":self.checkBox_9.isChecked(),
                "P-Value Threshold CutOff-Value":self.doubleSpinBox_3.value()
                    },
            "Data Saving Settings":{
                "Save Cropped Membrane":self.checkBox_11.isChecked(),
                "Save Cropped Cytosl":self.checkBox_12.isChecked(),
                "Save Linearized Cytosol":self.checkBox_13.isChecked(),
                "Save Phasors":self.checkBox_17.isChecked(),
                "Save Settings":self.checkBox_18.isChecked(),
                "Save Results":self.checkBox_19.isChecked()
                    },
            "Results":self.Results[filename] if self.checkBox_19.isChecked() else []
                }

        # Specify the file path where you want to save the settings
        
        filename_ext=join(filename+".json")
        file_path = join(savepath,filename_ext)

        # Save the settings to a JSON file
        
        #ui_settings_serializable = self.convert_np_arrays_to_lists(ui_settings)
        with open(file_path, "w") as json_file:
            json.dump(ui_settings, json_file, cls=NumpyEncoder)
        
        print("Settings saved successfully.")

        
    def LoadFiles(self):
        self.ClearALL_andDissable() 
        self.path, _ = tuple(QFileDialog.getOpenFileNames(None, "Open Image File","","Images (*.lsm *.czi *.lif *.obf *.ome.tif)"))
        row=0
        pathn=0
        maxlen=0
        if len(self.path)!=0:
            for i in self.path:
                image,metadata=openfile(i)
                if isinstance(image, dict):
                    maxlen=maxlen+len(image)
                else:
                    maxlen+=1
            if maxlen > len(self.path):
                self.tableWidget.setRowCount(maxlen)
                for i in self.path:
                    image,metadata=openfile(i)
                    if isinstance(image, dict):
                        for n in range(len(image)):
                            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(self.path[pathn])+"_subimage_"+str(n+1)))
                            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(dirname(self.path[pathn])))
                            row+=1
                        pathn+=1
                    else:
                        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(self.path[pathn])))
                        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(dirname(self.path[pathn])))
                        pathn+=1
                        row=row+1
            else:
                self.tableWidget.setRowCount(len(self.path))
                for i in self.path:
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(self.path[row])))
                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(dirname(self.path[row])))
                    row=row+1
            if isinstance(image, dict):
                Lambdachannel=metadata[0]['ChannelColors']
            else:
                Lambdachannel=metadata['ChannelColors']
                
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_6.clear()
            self.comboBox_7.clear()
            self.comboBox_8.clear()
            self.comboBox_13.clear()
            self.comboBox_14.clear()
            self.comboBox_15.clear()
            self.comboBox_16.clear()
            self.comboBox_18.clear()
            self.comboBox_23.clear()
            
            self.comboBox.addItems(['NaN'])
            self.comboBox_2.addItems(['NaN'])
            self.comboBox_6.addItems(['NaN'])
            self.comboBox_7.addItems(['NaN'])
            self.comboBox_8.addItems(['NaN'])
            self.comboBox_13.addItems(['NaN'])
            self.comboBox_14.addItems(['NaN'])
            self.comboBox_15.addItems(['NaN'])
            self.comboBox_16.addItems(['NaN'])
            self.comboBox_18.addItems(['NaN'])
            self.comboBox_23.addItems(['NaN'])
            
            self.comboBox.addItems([str(x) for x in Lambdachannel])
            self.comboBox_2.addItems([str(x) for x in Lambdachannel])
            self.comboBox_6.addItems([str(x) for x in Lambdachannel])
            self.comboBox_7.addItems([str(x) for x in Lambdachannel])
            self.comboBox_8.addItems([str(x) for x in Lambdachannel])
            self.comboBox_13.addItems([str(x) for x in Lambdachannel])
            self.comboBox_14.addItems([str(x) for x in Lambdachannel])
            self.comboBox_15.addItems([str(x) for x in Lambdachannel])
            self.comboBox_16.addItems([str(x) for x in Lambdachannel])
            self.comboBox_23.addItems([str(x) for x in Lambdachannel])
            self.comboBox_18.addItems([str(x) for x in Lambdachannel])


            
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.comboBox_6.setEnabled(True)
            self.comboBox_7.setEnabled(True)
            self.checkBox_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.comboBox_3.setEnabled(True) 
            self.comboBox_13.setEnabled(True)
            self.comboBox_14.setEnabled(True)
            self.comboBox_15.setEnabled(True)
            self.comboBox_16.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True) 
            self.checkBox_5.setEnabled(True) 
            self.checkBox_6.setEnabled(True) 
            self.checkBox_24.setEnabled(True)
            self.checkBox_26.setEnabled(True)
            self.checkBox_27.setEnabled(True)
            self.checkBox_36.setEnabled(True)
            self.checkBox_16.setEnabled(True)
            self.checkBox_15.setEnabled(True)
            self.checkBox_32.setEnabled(True)
            self.checkBox_34.setEnabled(True)
            self.checkBox_35.setEnabled(True)
            self.checkBox_33.setEnabled(True)
            self.checkBox_37.setEnabled(True)
            self.checkBox_31.setEnabled(True)
            
            self.comboBox_21.setEnabled(True)
            self.doubleSpinBox_21.setEnabled(True)
            
            
            self.B_Run.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            
            self.doubleSpinBox_4.setEnabled(True)
            self.doubleSpinBox_5.setEnabled(True)
            self.doubleSpinBox_6.setEnabled(True)
            self.doubleSpinBox_8.setEnabled(True)
            self.doubleSpinBox_17.setEnabled(True)
            self.doubleSpinBox_18.setEnabled(True)
            self.doubleSpinBox_19.setEnabled(True)
            
            self.B_LoadFiles.setEnabled(True)
            self.B_LoadFolder.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.enablee_parts()

        else:
#             self.enablee_parts()
            self.B_LoadFiles.setEnabled(True)
            self.B_LoadFolder.setEnabled(True)



    def Select_Saving_Path(self):
        #self.savingpath= QFileDialog.getExistingDirectory(None, "Open Image Directory")
        self.DifferentSavingPath=QFileDialog.getExistingDirectory(None, "Open Image Directory")
        self.textBrowser.setText(self.DifferentSavingPath)
        
    def LoadFolder(self):
        self.ClearALL_andDissable() 
        self.path= QFileDialog.getExistingDirectory(None, "Open Image Directory")
        if len(self.path)!=0:
            allowed_extensions = ['.lsm', '.czi', '.lif', '.obf', '.ome.tif']
            self.Files = [f for f in listdir(self.path) if isfile(join(self.path, f)) and any(f.endswith(ext) for ext in allowed_extensions)]
            row=0
            pathn=0
            maxlen=0
            for i in self.Files:
                image,metadata=openfile(join(self.path, i))
                if isinstance(image, dict):
                    maxlen=maxlen+len(image)
                else:
                    maxlen+=1
            
            if maxlen> len(self.Files):
                self.tableWidget.setRowCount(maxlen)
                for i in self.Files:
                    image,metadata=openfile(join(self.path, i))
                    if isinstance(image, dict):
                        for n in range(len(image)):
                            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(i)+"_subimage_"+str(n+1)))
                            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem((self.path)))
                            row+=1
                        pathn+=1
                    else:
                        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(i)))
                        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem((self.path)))
                        pathn+=1
                        row=row+1
            else:
                self.tableWidget.setRowCount(len(self.Files))
                for i in self.Files:
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(basename(i)))
                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem((self.path)))
                    row=row+1
            row=0
            
            ## Lambda update

            if isinstance(image, dict):
                Lambdachannel=metadata[0]['ChannelColors']
            else:
                Lambdachannel=metadata['ChannelColors']
            
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_6.clear()
            self.comboBox_7.clear()
            self.comboBox_8.clear()
            self.comboBox_13.clear()
            self.comboBox_14.clear()
            self.comboBox_15.clear()
            self.comboBox_16.clear()
            self.comboBox_18.clear()
            self.comboBox_23.clear()
            
            self.comboBox.addItems(['NaN'])
            self.comboBox_2.addItems(['NaN'])
            self.comboBox_6.addItems(['NaN'])
            self.comboBox_7.addItems(['NaN'])
            self.comboBox_8.addItems(['NaN'])
            self.comboBox_13.addItems(['NaN'])
            self.comboBox_14.addItems(['NaN'])
            self.comboBox_15.addItems(['NaN'])
            self.comboBox_16.addItems(['NaN'])
            self.comboBox_18.addItems(['NaN'])
            self.comboBox_23.addItems(['NaN'])
            
            self.comboBox.addItems([str(x) for x in Lambdachannel])
            self.comboBox_2.addItems([str(x) for x in Lambdachannel])
            self.comboBox_6.addItems([str(x) for x in Lambdachannel])
            self.comboBox_7.addItems([str(x) for x in Lambdachannel])
            self.comboBox_8.addItems([str(x) for x in Lambdachannel])
            self.comboBox_13.addItems([str(x) for x in Lambdachannel])
            self.comboBox_14.addItems([str(x) for x in Lambdachannel])
            self.comboBox_15.addItems([str(x) for x in Lambdachannel])
            self.comboBox_16.addItems([str(x) for x in Lambdachannel])
            self.comboBox_23.addItems([str(x) for x in Lambdachannel])
            self.comboBox_18.addItems([str(x) for x in Lambdachannel])
            
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.comboBox_6.setEnabled(True)
            self.comboBox_7.setEnabled(True)
            self.checkBox_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.comboBox_3.setEnabled(True) 
            self.comboBox_13.setEnabled(True)
            self.comboBox_14.setEnabled(True)
            self.comboBox_15.setEnabled(True)
            self.comboBox_16.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True) 
            self.checkBox_5.setEnabled(True) 
            self.checkBox_6.setEnabled(True) 
            self.checkBox_24.setEnabled(True)
            self.checkBox_26.setEnabled(True)
            self.checkBox_27.setEnabled(True)
            self.checkBox_36.setEnabled(True)
            self.checkBox_16.setEnabled(True)
            self.checkBox_15.setEnabled(True)
            self.checkBox_32.setEnabled(True)
            self.checkBox_34.setEnabled(True)
            self.checkBox_35.setEnabled(True)
            self.checkBox_33.setEnabled(True)
            self.checkBox_37.setEnabled(True)
            self.checkBox_31.setEnabled(True)
            
            self.comboBox_21.setEnabled(True)
            self.doubleSpinBox_21.setEnabled(True)
            
            self.B_Run.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            
            self.doubleSpinBox_4.setEnabled(True)
            self.doubleSpinBox_5.setEnabled(True)
            self.doubleSpinBox_6.setEnabled(True)
            self.doubleSpinBox_8.setEnabled(True)
            self.doubleSpinBox_17.setEnabled(True)
            self.doubleSpinBox_18.setEnabled(True)
            self.doubleSpinBox_19.setEnabled(True)
            
            self.B_LoadFiles.setEnabled(True)
            self.B_LoadFolder.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.enablee_parts()

        else:
#             self.enablee_parts()
            self.B_LoadFiles.setEnabled(True)
            self.B_LoadFolder.setEnabled(True)

        
    def DeletEntry(self):
        if not len(self.tableWidget.selectionModel().selectedIndexes())==0:
            if not self.tableWidget.rowCount() == 0:
                if self.tableWidget.currentItem().isSelected():
                    counter=0
                    for i in  reversed(range(self.tableWidget.rowCount())):
                        if (self.tableWidget.item(i,0)).isSelected():
                            counter=counter+1
                            self.tableWidget.removeRow(i)
        if self.tableWidget.rowCount() == 0:
            self.ClearALL_andDissable()
            self.B_LoadFiles.setEnabled(True)
            self.B_LoadFolder.setEnabled(True)
        
    def ClearTable(self):
        self.tableWidget.setRowCount(0)
        self.ClearALL_andDissable()
        self.B_LoadFiles.setEnabled(True)
        self.B_LoadFolder.setEnabled(True)
        
    def ClearALL_andDissable(self):
        self.Results={}
        self.Membrane_Maskdata={} #[filename][t][z][key]
        self.Cyto_Maskdata={}
        self.previously_selected_file=[None]
        self.dims={}
        self.RawImages={}
        self.GPImage={}
        self.FullImage_Parameters={}
        self.Cyto_GPImage={}
        self.GPImage_per_object={}  
        self.GPPhasor={}     
        self.Cyto_GPPhasor={}     
        self.Masks={}
        self.Cyto_Masks={}
        self.Intensities={}
        self.Cyto_Intensities={}
        self.nobjects={}
        self.Object_Parameters={}
        self.Object_Morphology={}
        self.Object_Coordinates={}
        self.Mask_Object_Coordinates={}
        self.Intensities_per_object={}
        self.Channellamda={}
        self.phasex_object={}
        self.phasey_object={}
        self.GPPhasor_polar_all={}
        self.Cyto_GPPhasor_polar_all={}
        self.GPPhasor_polar_obj={}
        self.key={}
        self.ConnectSliders={}
        self.Profile={}
        self.MembraneSegments={}
        self.Cytoprof={}
        self.Cyto_Image={}
        self.FullImage_Parameters_cyto={}
        self.Object_Parameters_cyto={}
        self.Cyto_Intensities_per_object={}
        self.Cyto_GPPhasor_polar_obj={}
        self.savingpath=str([])
        
        self.disable_parts()
        
        
    def ClearSelection(self):
        self.tableWidget.selectionModel().clearSelection()
        self.tableWidget.setCurrentCell(-1,-1)
        
        
    def find_unique_valid_letters(self,equation_string, combo_A, combo_B, combo_C, combo_D):
        allowed_chars = {'A', 'B', 'C', 'D'}
        invalid_characters = {'E', 'I', 'N', 'O', 'Q', 'S'}
        invalid_char = next((char for char in equation_string if char in invalid_characters), None)
        if invalid_char:
            return False, f"Error: Invalid character '{invalid_char}' found in the text. ('E', 'I', 'N', 'O', 'Q', 'S' are reserved for mathematical operators)"
        try:
            expression = sympify(equation_string)
            variables = expression.free_symbols
    
            for var in variables:
                if str(var) not in allowed_chars:
                    return False, f"Invalid variable '{var}' found in the membrane equation. Only {', '.join(allowed_chars)} are allowed."
        except SympifyError as e:
            return False, f"Error: {e}"
        
        unique_letters = set()

        for char in equation_string:
            if char.isupper():
                if char not in allowed_chars:
                    return 1,unique_letters,f"Error: Invalid letter '{char}' found in the text."
                unique_letters.add(char)

        invalid_combos = []
        if 'A' in unique_letters and combo_A == 'NaN':
            invalid_combos.append("'A'")
        if 'B' in unique_letters and combo_B == 'NaN':
            invalid_combos.append("'B'")
        if 'C' in unique_letters and combo_C == 'NaN':
            invalid_combos.append("'C'")
        if 'D' in unique_letters and combo_D == 'NaN':
            invalid_combos.append("'D'")
        if self.checkBox_27.isChecked() and self.comboBox_18.currentText() == 'NaN':
            invalid_combos.append("'Specific Membrane Thresholding Channel'")
        if self.checkBox_14.isChecked() and self.comboBox_8.currentText() == 'NaN':
            invalid_combos.append("'Colocalization Channel'")

        if invalid_combos:
            return False,f"Error Membrane Settings: Letter(s) {', '.join(invalid_combos)} is/are in use (Equation), but corresponding ComboBox value(s) is/are NaN."

        return True,"All good"
            

    def find_unique_valid_letters_cyto(self,equation_string, combo_A, combo_B, combo_C, combo_D):
        allowed_chars = {'A', 'B', 'C', 'D'}
        invalid_characters = {'E', 'I', 'N', 'O', 'Q', 'S'}
        invalid_char = next((char for char in equation_string if char in invalid_characters), None)
        if invalid_char:
            return False, f"Error: Invalid character '{invalid_char}' found in the text. ('E', 'I', 'N', 'O', 'Q', 'S' are reserved for mathematical operators)"
        try:
            expression = sympify(equation_string)
            variables = expression.free_symbols
    
            for var in variables:
                if str(var) not in allowed_chars:
                    return False, f"Invalid variable '{var}' found in the membrane equation. Only {', '.join(allowed_chars)} are allowed."
        except SympifyError as e:
            return False, f"Error: {e}"
        
        unique_letters = set()

        for char in equation_string:
            if char.isupper():
                if char not in allowed_chars:
                    return 1,unique_letters,f"Error: Invalid letter '{char}' found in the text."
                unique_letters.add(char)

        invalid_combos = []
        if 'A' in unique_letters and combo_A == 'NaN':
            invalid_combos.append("'A'")
        if 'B' in unique_letters and combo_B == 'NaN':
            invalid_combos.append("'B'")
        if 'C' in unique_letters and combo_C == 'NaN':
            invalid_combos.append("'C'")
        if 'D' in unique_letters and combo_D == 'NaN':
            invalid_combos.append("'D'")
        if self.checkBox_36.isChecked() and self.comboBox_23.currentText() =='NaN':
            invalid_combos.append("'Specific Cytosol Thresholding Channel'")

        if invalid_combos:
            return False,f"Error Cytosol Settings: Letter(s) {', '.join(invalid_combos)} is/are in use (Equation), but corresponding ComboBox value(s) is/are NaN."

        return True,"All good"

            
    def testThresholding(self):
        global Resultstest
        if True: # Placehodler 
            if not self.tableWidget.rowCount() == 0:
                if self.tableWidget.currentItem() is not None:
                    if self.tableWidget.currentItem().isSelected():
                        for i in range(self.tableWidget.rowCount()):
                            if (self.tableWidget.item(i,0)).isSelected():
                                mode=0
                                filename=self.tableWidget.item(i,0).text()
                                path=self.tableWidget.item(i,1).text()
                                app.processEvents()
                                
                                if "_subimage_" in filename:
                                    modified_filename = filename.split("_subimage_")[0]
                                    image_dict,metadata_dict=openfile(join(path, modified_filename))
                                    image=image_dict[0]
                                    metadata=metadata_dict[0]
                                    Lambdachannel=metadata['ChannelColors']
                                    dims=metadata['Dimensions']
                                    
                                    Data_py=image

                                else:
                                    modified_filename = filename
                                    image,metadata=openfile(join(path, modified_filename))
                                    
                                    Lambdachannel=metadata['ChannelColors']
                                    dims=metadata['Dimensions']
                                    Data_py=image
                                # print("--------------------------------------")
                                # print("--------------------------------------")
                                # print("Pixelsize")
                                # print(type(Pixelsize))
                                # print(Pixelsize)
                                # print("Nchannels")
                                # print(type(Nchannels))
                                # print(Nchannels)
                                # print("Lambdachannel")
                                # print(type(Lambdachannel))
                                # print(Lambdachannel)
                                # print("dims")
                                # print(type(dims))
                                # print(dims)
                                # print("PixelDepth")
                                # print(type(PixelDepth))
                                # print(PixelDepth)
                                # print("image")
                                # print(type(Data_py))
                                # print(Data_py.shape)
                                # print("--------------------------------------")
                                # print("--------------------------------------")

                                
                                if self.checkBox_24.isChecked():
                                    self.update_toglobal_values_membrane()
                                if self.checkBox_31.isChecked():
                                    self.update_toglobal_values_cytosol()
                                    
                                    
                                
                                if self.savingpath:
                                    savepath=self.tableWidget.item(i,1).text()
                                else:
                                    savepath=self.savingpath

                                Result=RunAnalyser(    mode=mode,
                                                    filename=filename,
                                                    Lambdachannel=Lambdachannel,
                                                    image=Data_py,
                                                    dims=dims,
                                                    varlist=[int(self.comboBox.currentText()) if self.comboBox.currentText().lower().isdigit() else None,
                                                                int(self.comboBox_2.currentText()) if self.comboBox_2.currentText().isdigit() else None,
                                                                int(self.comboBox_6.currentText()) if self.comboBox_6.currentText().isdigit() else None,
                                                                int(self.comboBox_7.currentText()) if self.comboBox_7.currentText().isdigit() else None],
                                                    ObjectDetection=self.checkBox_2.isChecked(),
                                                    profiler=self.checkBox_8.isChecked(),
                                                    profilershape=self.comboBox_5.currentText(),
                                                    autoff=self.checkBox_9.isChecked(), #???
                                                    PDiamCutoff=self.doubleSpinBox_3.value(), #???
                                                    proDim1=self.spinBox_7.value(),
                                                    proDim2=self.spinBox_8.value(),
                                                    text=self.plainTextEdit.toPlainText(),
                                                    histpars=[self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value(),self.doubleSpinBox_4.value()], 
                                                    histpars_cyto=[self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value(),self.doubleSpinBox_19.value()],
                                                    text_cyto=self.plainTextEdit_2.toPlainText(),
                                                    profile_cyto=self.checkBox.isChecked(),
                                                    varlist_cyto=[int(self.comboBox_13.currentText()) if self.comboBox_13.currentText().isdigit() else None,
                                                                int(self.comboBox_14.currentText()) if self.comboBox_14.currentText().isdigit() else None,
                                                                int(self.comboBox_15.currentText()) if self.comboBox_15.currentText().isdigit() else None,
                                                                int(self.comboBox_16.currentText()) if self.comboBox_16.currentText().isdigit() else None], 
                                                    n_debranch=self.spinBox_3.value(), #NEW
                                                    tol0=self.doubleSpinBox_2.value(), #NEW
                                                    tol1=self.spinBox_6.value(), #NEW
                                                    savecroppedmembrane=self.checkBox_11.isChecked(), 
                                                    savecroppedcyto=self.checkBox_12.isChecked(),
                                                    savelinearized=self.checkBox_13.isChecked(), 
                                                    savepath=savepath, 
                                                    objlinear=self.checkBox_7.isChecked(), #NEW ???
                                                    recentering=False, #NEW ???
                                                    dim_line=self.spinBox_9.value(),  #NEW ???
                                                    MaskParams_mem=self.Membrane_Maskdata[filename], 
                                                    MaskParams_cyto=self.Cyto_Maskdata[filename], # NEW
                                                    Colocalization= int(self.comboBox_8.currentText()) if self.checkBox_14.isChecked() and self.comboBox_8.currentText().isdigit() else "NaN",
                                                    savephasors=self.checkBox_17.isChecked(),
                                                    tocut = 0, #???? WAS hab i ma dabei gedacht
                                                    radius = 'auto') #???? WAS hab i ma dabei gedacht
                                
                                Resultstest=Result
                                
                                if ((dims[0]!=1) != (dims[1]!=1)): #if Z or T 4D
                                    if dims[1]!=1: #Zstack 4D
                                        self.key[filename]="Zstack"
                                    else:
                                        self.key[filename]="Tstack"
                                    self.Masks[filename]=[]
                                    if ((isinstance(Result[0]["datamask"][8], np.ndarray) and Result[0]["datamask"][8].size > 0)
                                       or (isinstance(Result[0]["datamask"][8], list) and len(Result[0]["datamask"][8]) > 0)):
                                        self.Cyto_Masks[filename]=[]
                                    for Stack in Result:
                                        self.Masks[filename].append(Result[Stack]["datamask"][2])
                                        if ((isinstance(Result[Stack]["datamask"][8], np.ndarray) and Result[Stack]["datamask"][8].size > 0)
                                           or (isinstance(Result[Stack]["datamask"][8], list) and len(Result[Stack]["datamask"][8]) > 0)):
                                            self.Cyto_Masks[filename].append(Result[Stack]["datamask"][8])
                                        self.RawImages[filename]=Data_py
                                        
                                elif (dims[0]!=1 and dims[1]!=1): #if Z and T 5D
                                    self.Masks[filename]=[]
                                    if ((isinstance(Result[0][0]["datamask"][8], np.ndarray) and Result[0][0]["datamask"][8].size > 0)
                                       or (isinstance(Result[0][0]["datamask"][8], list) and len(Result[0][0]["datamask"][8]) > 0)):
                                        self.Cyto_Masks[filename]=[]
                                    self.key[filename]="TZstack"
                                    for T_Stack in Result:
                                        self.Masks[filename].append([])
                                        if ((isinstance(Result[T_Stack][0]["datamask"][8], np.ndarray) and Result[T_Stack][0]["datamask"][8].size > 0)
                                           or (isinstance(Result[T_Stack][0]["datamask"][8], list) and len(Result[T_Stack][0]["datamask"][8]) > 0)):
                                            self.Cyto_Masks[filename].append([])
                                        for Z_Stack in Result[T_Stack]:
                                            self.Masks[filename][T_Stack].append(Result[T_Stack][Z_Stack]["datamask"][2])
                                            if ((isinstance(Result[T_Stack][Z_Stack]["datamask"][8], np.ndarray) and Result[T_Stack][Z_Stack]["datamask"][8].size > 0)
                                               or (isinstance(Result[T_Stack][Z_Stack]["datamask"][8], list) and len(Result[T_Stack][Z_Stack]["datamask"][8]) > 0)): 
                                                self.Cyto_Masks[filename][T_Stack].append(Result[T_Stack][Z_Stack]["datamask"][8])
                                            self.RawImages[filename]=Data_py
                                else:
                                    self.key[filename]="3dim"
                                    if isinstance(Result, dict):
                                        self.Masks[filename]=Result["datamask"][2]
                                        self.Cyto_Masks[filename]=Result["datamask"][8]
                                        self.RawImages[filename]=Data_py
                                        
                else:
                    for i in range(self.tableWidget.rowCount()):
                        mode=0
                        filename=self.tableWidget.item(i,0).text()
                        path=self.tableWidget.item(i,1).text()
                        image,metadata=openfile(join(path, filename))
                        Lambdachannel=metadata['ChannelColors']
                        dims=metadata['Dimensions']
                        Data_py=image
                        
                        if self.savingpath:
                            savepath=self.tableWidget.item(i,1).text()
                        else:
                            savepath=self.savingpath
                        
                        if self.checkBox_24.isChecked():
                            self.update_toglobal_values_membrane(filename=filename, path=path)
                        if self.checkBox_31.isChecked():
                            self.update_toglobal_values_cytosol(filename=filename, path=path)
                            
                        Result=RunAnalyser(mode=mode,
                                            filename=filename,
                                            Lambdachannel=Lambdachannel,
                                            image=Data_py,
                                            dims=dims,
                                            varlist=[int(self.comboBox.currentText()) if self.comboBox.currentText().isdigit() else None,
                                                        int(self.comboBox_2.currentText()) if self.comboBox_2.currentText().isdigit() else None,
                                                        int(self.comboBox_6.currentText()) if self.comboBox_6.currentText().isdigit() else None,
                                                        int(self.comboBox_7.currentText()) if self.comboBox_7.currentText().isdigit() else None],
                                            ObjectDetection=self.checkBox_2.isChecked(),
                                            profiler=self.checkBox_8.isChecked(),
                                            profilershape=self.comboBox_5.currentText(),
                                            autoff=self.checkBox_9.isChecked(), #???
                                            PDiamCutoff=self.doubleSpinBox_3.value(), #???
                                            proDim1=self.spinBox_7.value(),
                                            proDim2=self.spinBox_8.value(),
                                            text=self.plainTextEdit.toPlainText(),
                                            histpars=[self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value(),self.doubleSpinBox_4.value()], 
                                            histpars_cyto=[self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value(),self.doubleSpinBox_19.value()],
                                            text_cyto=self.plainTextEdit_2.toPlainText(),
                                            profile_cyto=self.checkBox.isChecked(),
                                            varlist_cyto=[int(self.comboBox_13.currentText()) if self.comboBox_13.currentText().lower().isdigit() else None,
                                                        int(self.comboBox_14.currentText()) if self.comboBox_14.currentText().lower().isdigit() else None,
                                                        int(self.comboBox_15.currentText()) if self.comboBox_15.currentText().lower().isdigit() else None,
                                                        int(self.comboBox_16.currentText()) if self.comboBox_16.currentText().lower().isdigit() else None], 
                                            n_debranch=self.spinBox_3.value(), #NEW
                                            tol0=self.doubleSpinBox_2.value(), #NEW
                                            tol1=self.spinBox_6.value(), #NEW
                                            savecroppedmembrane=self.checkBox_11.isChecked(), 
                                            savecroppedcyto=self.checkBox_12.isChecked(),
                                            savelinearized=self.checkBox_13.isChecked(), 
                                            savepath=savepath, 
                                            objlinear=self.checkBox_7.isChecked(), #NEW ???
                                            recentering=False, #NEW ???
                                            dim_line=self.spinBox_9.value(),  #NEW ???
                                            MaskParams_mem=self.Membrane_Maskdata[filename], 
                                            MaskParams_cyto=self.Cyto_Maskdata[filename], # NEW
                                            Colocalization= int(self.comboBox_8.currentText()) if self.checkBox_14.isChecked() and self.comboBox_8.currentText().isdigit() else "NaN",
                                            savephasors=self.checkBox_17.isChecked(),
                                            tocut = 0, #???? WAS hab i ma dabei gedacht
                                            radius = 'auto') #???? WAS hab i ma dabei gedacht
                                            
                        Resultstest=Result
                        
                        if ((dims[0]!=1) != (dims[1]!=1)): #if Z or T 4D
                            if dims[1]!=1: #Zstack 4D
                                self.key[filename]="Zstack"
                            else:
                                self.key[filename]="Tstack"
                            self.Masks[filename]=[]
                            if ((isinstance(Result[0]["datamask"][8], np.ndarray) and Result[0]["datamask"][8].size > 0)
                               or (isinstance(Result[0]["datamask"][8], list) and len(Result[0]["datamask"][8]) > 0)):
                                self.Cyto_Masks[filename]=[]
                            for Stack in Result:
                                self.Masks[filename].append(Result[Stack]["datamask"][2])
                                if ((isinstance(Result[Stack]["datamask"][8], np.ndarray) and Result[Stack]["datamask"][8].size > 0)
                                   or (isinstance(Result[Stack]["datamask"][8], list) and len(Result[Stack]["datamask"][8]) > 0)):
                                    self.Cyto_Masks[filename].append(Result[Stack]["datamask"][8])
                                self.RawImages[filename]=Data_py
                                
                        elif (dims[0]!=1 and dims[1]!=1): #if Z and T 5D
                            self.Masks[filename]=[]
                            if ((isinstance(Result[0][0]["datamask"][8], np.ndarray) and Result[0][0]["datamask"][8].size > 0)
                               or (isinstance(Result[0][0]["datamask"][8], list) and len(Result[0][0]["datamask"][8]) > 0)):
                                self.Cyto_Masks[filename]=[]
                            self.key[filename]="TZstack"
                            for T_Stack in Result:
                                self.Masks[filename].append([])
                                if ((isinstance(Result[T_Stack][0]["datamask"][8], np.ndarray) and Result[T_Stack][0]["datamask"][8].size > 0)
                                   or (isinstance(Result[T_Stack][0]["datamask"][8], list) and len(Result[T_Stack][0]["datamask"][8]) > 0)):
                                    self.Cyto_Masks[filename].append([])
                                for Z_Stack in Result[T_Stack]:
                                    self.Masks[filename][T_Stack].append(Result[T_Stack][Z_Stack]["datamask"][2])
                                    if ((isinstance(Result[T_Stack][Z_Stack]["datamask"][8], np.ndarray) and Result[T_Stack][Z_Stack]["datamask"][8].size > 0)
                                       or (isinstance(Result[T_Stack][Z_Stack]["datamask"][8], list) and len(Result[T_Stack][Z_Stack]["datamask"][8]) > 0)): 
                                        self.Cyto_Masks[filename][T_Stack].append(Result[T_Stack][Z_Stack]["datamask"][8])
                                    self.RawImages[filename]=Data_py
                        else:
                            self.key[filename]="3dim"
                            if isinstance(Result, dict):
                                self.Masks[filename]=Result["datamask"][2]
                                self.Cyto_Masks[filename]=Result["datamask"][8]
                                self.RawImages[filename]=Data_py
                        
                            #                      
            else:   
                print("NO Data Loaded")
        else:
            pass


    def disable_parts(self):
        self.B_Run.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.B_LoadFiles.setEnabled(False)
        self.B_LoadFolder.setEnabled(False)
        self.B_ClearSelection.setEnabled(False)
        self.B_DeletEntry.setEnabled(False)
        self.B_ClearTable.setEnabled(False)

            
    def enablee_parts(self):
        self.B_Run.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.B_LoadFiles.setEnabled(True)
        self.B_LoadFolder.setEnabled(True)
        self.B_ClearSelection.setEnabled(True)
        self.B_DeletEntry.setEnabled(True)
        self.B_ClearTable.setEnabled(True)

        
                        
    def Run(self):
        global Resultstest
        if True:
            self.testThresholding() #Umändern
            if not self.tableWidget.rowCount() == 0:
                if self.tableWidget.currentItem() is not None:
                    if self.tableWidget.currentItem().isSelected():
                        print("only selected data used")
                        for i in range(self.tableWidget.rowCount()):
                            if (self.tableWidget.item(i,0)).isSelected():
                                filename=self.tableWidget.item(i,0).text()
                                self.ConnectSliders[filename]=True
                                path=self.tableWidget.item(i,1).text()
                                app.processEvents()
                                image,metadata=openfile(join(path, filename))
                                Lambdachannel=metadata['ChannelColors']
                                dims=metadata['Dimensions']
                                self.Metadata[filename]=metadata
                                Data_py=image
                                ## Run Analysis selected images
                                mode=1
                                if len(self.DifferentSavingPath)>2:
                                    print("YES")
                                    savepath=self.DifferentSavingPath
                                else:
                                    print("NO")
                                    savepath=self.tableWidget.item(i,1).text()
                                print(savepath)
                                if self.checkBox_24.isChecked():
                                    self.update_toglobal_values_membrane(filename=filename, path=path)
                                else:
                                    pass # here we need the fix for the detailed masking not prior selecte image issue
                                if self.checkBox_31.isChecked():
                                    self.update_toglobal_values_cytosol(filename=filename, path=path)
                                else:
                                    pass # here we need the fix for the detailed masking not prior selecte image issue
                                
                                Result=RunAnalyser(mode=mode,
                                                    filename=filename,
                                                    Lambdachannel=Lambdachannel,
                                                    image=Data_py,
                                                    dims=dims,
                                                    varlist=[int(self.comboBox.currentText()) if self.comboBox.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_2.currentText()) if self.comboBox_2.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_6.currentText()) if self.comboBox_6.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_7.currentText()) if self.comboBox_7.currentText().lower() != 'nan' else None],
                                                    ObjectDetection=self.checkBox_2.isChecked(),
                                                    profiler=self.checkBox_8.isChecked(),
                                                    profilershape=self.comboBox_5.currentText(),
                                                    autoff=self.checkBox_9.isChecked(), #???
                                                    PDiamCutoff=self.doubleSpinBox_3.value(), #???
                                                    proDim1=self.spinBox_7.value(),
                                                    proDim2=self.spinBox_8.value(),
                                                    text=self.plainTextEdit.toPlainText(),
                                                    histpars=[self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value(),self.doubleSpinBox_4.value()], 
                                                    histpars_cyto=[self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value(),self.doubleSpinBox_17.value()],
                                                    text_cyto=self.plainTextEdit_2.toPlainText(),
                                                    profile_cyto=self.checkBox.isChecked(),
                                                    varlist_cyto=[int(self.comboBox_13.currentText()) if self.comboBox_13.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_14.currentText()) if self.comboBox_14.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_15.currentText()) if self.comboBox_15.currentText().lower() != 'nan' else None,
                                                                int(self.comboBox_16.currentText()) if self.comboBox_16.currentText().lower() != 'nan' else None], 
                                                    n_debranch=self.spinBox_3.value(), #NEW
                                                    tol0=self.doubleSpinBox_2.value(), #NEW
                                                    tol1=self.spinBox_6.value(), #NEW
                                                    savecroppedmembrane=self.checkBox_11.isChecked(), 
                                                    savecroppedcyto=self.checkBox_12.isChecked(),
                                                    savelinearized=self.checkBox_13.isChecked(), 
                                                    savepath=savepath, 
                                                    objlinear=self.checkBox_7.isChecked(), #NEW ???
                                                    recentering=False, #NEW ???
                                                    dim_line=self.spinBox_9.value(),  #NEW ???
                                                    MaskParams_mem=self.Membrane_Maskdata[filename], 
                                                    MaskParams_cyto=self.Cyto_Maskdata[filename], # NEW
                                                    Colocalization= int(self.comboBox_8.currentText()) if self.checkBox_14.isChecked() and self.comboBox_8.currentText().isdigit() else "NaN",
                                                    savephasors=self.checkBox_17.isChecked(),
                                                    tocut = 0, #???? WAS hab i ma dabei gedacht
                                                    radius = 'auto') #???? WAS hab i ma dabei gedacht

                                Resultstest=Result
                                
                                self.Results[filename]=Result
                                self.dims[filename]=dims
                                app.processEvents()
                                
                                self.Poppulationg_Results (Result, dims, filename,Lambdachannel)
                                if self.checkBox_18.isChecked():
                                    self.SaveAllInJSON(filename,savepath)

                                        
                else: # without selection 
                    for i in range(self.tableWidget.rowCount()):
                        filename=self.tableWidget.item(i,0).text()
                        self.ConnectSliders[filename]=True
                        path=self.tableWidget.item(i,1).text()
                        app.processEvents()
                        image,metadata=openfile(join(path, filename))
                        Lambdachannel=metadata['ChannelColors']
                        dims=metadata['Dimensions']
                        self.Metadata[filename]=metadata
                        Data_py=image
                        mode=1
                        if len(self.DifferentSavingPath)>2:
                            print("YES")
                            savepath=self.DifferentSavingPath
                        else:
                            print("NO")
                            savepath=self.tableWidget.item(i,1).text()
                        print(savepath)
                        if self.checkBox_24.isChecked():
                            self.update_toglobal_values_membrane(filename=filename, path=path)
                        if self.checkBox_31.isChecked():
                            self.update_toglobal_values_cytosol(filename=filename, path=path)
                        
                        Result=RunAnalyser(mode=mode,
                                            filename=filename,
                                            Lambdachannel=Lambdachannel,
                                            image=Data_py,
                                            dims=dims,
                                            varlist=[int(self.comboBox.currentText()) if self.comboBox.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_2.currentText()) if self.comboBox_2.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_6.currentText()) if self.comboBox_6.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_7.currentText()) if self.comboBox_7.currentText().lower() != 'nan' else None],
                                            ObjectDetection=self.checkBox_2.isChecked(),
                                            profiler=self.checkBox_8.isChecked(),
                                            profilershape=self.comboBox_5.currentText(),
                                            autoff=self.checkBox_9.isChecked(), #???
                                            PDiamCutoff=self.doubleSpinBox_3.value(), #???
                                            proDim1=self.spinBox_7.value(),
                                            proDim2=self.spinBox_8.value(),
                                            text=self.plainTextEdit.toPlainText(),
                                            histpars=[self.doubleSpinBox_5.value(),self.doubleSpinBox_6.value(),self.doubleSpinBox_4.value()], 
                                            histpars_cyto=[self.doubleSpinBox_17.value(),self.doubleSpinBox_18.value(),self.doubleSpinBox_19.value()],
                                            text_cyto=self.plainTextEdit_2.toPlainText(),
                                            profile_cyto=self.checkBox.isChecked(),
                                            varlist_cyto=[int(self.comboBox_13.currentText()) if self.comboBox_13.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_14.currentText()) if self.comboBox_14.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_15.currentText()) if self.comboBox_15.currentText().lower() != 'nan' else None,
                                                        int(self.comboBox_16.currentText()) if self.comboBox_16.currentText().lower() != 'nan' else None], 
                                            n_debranch=self.spinBox_3.value(), #NEW
                                            tol0=self.doubleSpinBox_2.value(), #NEW
                                            tol1=self.spinBox_6.value(), #NEW
                                            savecroppedmembrane=self.checkBox_11.isChecked(), 
                                            savecroppedcyto=self.checkBox_12.isChecked(),
                                            savelinearized=self.checkBox_13.isChecked(), 
                                            savepath=savepath, 
                                            objlinear=self.checkBox_7.isChecked(), #NEW ???
                                            recentering=False, #NEW ???
                                            dim_line=self.spinBox_9.value(),  #NEW ???
                                            MaskParams_mem=self.Membrane_Maskdata[filename], 
                                            MaskParams_cyto=self.Cyto_Maskdata[filename], # NEW
                                            Colocalization= int(self.comboBox_8.currentText()) if self.checkBox_14.isChecked() and self.comboBox_8.currentText().isdigit() else "NaN",
                                            savephasors=self.checkBox_17.isChecked(),
                                            tocut = 0, #???? WAS hab i ma dabei gedacht
                                            radius = 'auto') #???? WAS hab i ma dabei gedacht

                        Resultstest=Result
                        self.Results[filename]=Result
                        self.dims[filename]=dims
                        app.processEvents()
                        
                        self.Poppulationg_Results (Result, dims, filename,Lambdachannel)
                        if self.checkBox_18.isChecked():
                            self.SaveAllInJSON(filename,savepath)
                        
            else:
                print("NO Data Loaded")
                
                
        else:
            pass


    def Poppulationg_Results (self, Result, dims, filename,Lambdachannel):
        if ((dims[0]!=1) != (dims[1]!=1)): #if Z or T 4D
            if dims[1]!=1: #Zstack 4D
                self.key[filename]="Zstack"
            else:
                self.key[filename]="Tstack"
            self.GPImage[filename]=[]
            self.FullImage_Parameters[filename]=[]
            self.GPPhasor[filename]=[]
            self.GPPhasor_polar_all[filename]=[]
            
            self.Intensities[filename]=[]
            
            self.nobjects[filename]=[]
            self.GPPhasor_polar_obj[filename]=[]
            self.Intensities_per_object[filename]=[]
            self.GPImage_per_object[filename]=[]
            self.Object_Parameters[filename]=[]
            self.Object_Morphology[filename]=[]
            self.Object_Coordinates[filename]=[]
            self.Channellamda[filename]=[]
            self.Profile[filename]=[]
            self.MembraneSegments[filename]=[]
            if Result[0]["analysis"]["results_whole_cyto"]:
                self.Cyto_GPPhasor_polar_all[filename]=[]
                self.Cyto_Intensities[filename]=[]
                self.Cyto_GPImage[filename]=[]
                self.FullImage_Parameters_cyto[filename]=[]
                self.Cyto_Intensities_per_object[filename]=[]
                self.Cyto_GPPhasor_polar_obj[filename]=[]
                self.Cytoprof[filename]=[]
                self.Cyto_Image[filename]=[]
                self.Object_Parameters_cyto[filename]=[]
        
            for Stack in Result:
                self.GPImage[filename].append(Result[Stack]["analysis"]["results_whole"][2])
                self.FullImage_Parameters[filename].append(Result[Stack]["analysis"]["results_whole"][0]["Parameters"])
                if Result[Stack]["analysis"]["results_whole_cyto"]: 
                    self.Cyto_GPImage[filename].append(Result[Stack]["analysis"]["results_whole_cyto"][2])
                    self.FullImage_Parameters_cyto[filename].append(Result[Stack]["analysis"]["results_whole_cyto"][0]["Parameters"])
                    self.Cyto_GPPhasor_polar_all[filename].append(Result[Stack]["analysis"]["results_whole"][3])
                    self.Cyto_Intensities[filename].append([])
                    self.Cyto_Intensities[filename][Stack].append(Result[Stack]["analysis"]["results_whole_cyto"][0]["Wavelengths (nm)"])
                    self.Cyto_Intensities[filename][Stack].append(Result[Stack]["analysis"]["results_whole_cyto"][0]["Norm. Intensity"])
                
                self.GPPhasor[filename].append(Result[Stack]["analysis"]["results_whole"][3])
                self.GPPhasor_polar_all[filename].append(Result[Stack]["analysis"]["results_whole"][3])
                self.Intensities[filename].append([])
                self.Intensities[filename][Stack].append(Result[Stack]["analysis"]["results_whole"][0]["Wavelengths (nm)"])
                self.Intensities[filename][Stack].append(Result[Stack]["analysis"]["results_whole"][0]["Norm. Intensity"])
                self.nobjects[filename].append(0)
        
                if len(Result[Stack]["analysis"]["results_obj"])!=0:
                    self.nobjects[filename][Stack]=len(Result[Stack]["analysis"]["results_obj"])
                    self.Channellamda[filename].append(Lambdachannel)
                    
                    self.GPPhasor_polar_obj[filename].append([])
                    self.GPImage_per_object[filename].append([])
                    self.Object_Parameters[filename].append([])
                    self.Object_Morphology[filename].append([])
                    self.Intensities_per_object[filename].append([])
                    self.Object_Coordinates[filename].append([])
                    self.Profile[filename].append([])
                    self.MembraneSegments[filename].append([])
                    if Result[0]["analysis"]["results_whole_cyto"]:
                        self.Cytoprof[filename].append([])
                        self.Cyto_Image[filename].append([])
                        self.Object_Parameters_cyto[filename].append([])
                        self.Cyto_Intensities_per_object[filename].append([])
                        self.Cyto_GPPhasor_polar_obj[filename].append([])
        
                    for objn in Resultstest[Stack]["analysis"]["results_obj"]:
                        self.GPPhasor_polar_obj[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][3])
                        self.GPImage_per_object[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][2])
                        self.Object_Parameters[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Parameters"])
                        self.Object_Morphology[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["morphology"][2:])
                        self.Intensities_per_object[filename][Stack].append([])
                        self.Intensities_per_object[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Wavelengths (nm)"])
                        self.Intensities_per_object[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Norm. Intensity"])
                        self.Object_Coordinates[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["morphology"][1])
                        if len(Resultstest[Stack]["analysis"]["results_obj"][objn]["profile"]) !=0:
                            self.Profile[filename][Stack].append([])
                            self.Profile[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["profile"][0])
                            self.MembraneSegments[filename][Stack].append([])
                            self.MembraneSegments[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["profile"][6])
                        else:
                            self.Profile[filename][Stack].append([])
                            self.MembraneSegments[filename][Stack].append([])
                        if len(Resultstest[Stack]["analysis"]["results_obj"][objn]["basiccyto"]) !=0:
                            self.Cytoprof[filename][Stack].append([])
                            self.Cytoprof[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["objlinearization"])
                            self.Cyto_Image[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basiccyto"][2])
                            self.Object_Parameters_cyto[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Parameters"])
                            self.Cyto_Intensities_per_object[filename][Stack].append([])
                            self.Cyto_Intensities_per_object[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Wavelengths (nm)"])
                            self.Cyto_Intensities_per_object[filename][Stack][int(objn)-1].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Norm. Intensity"])
                            self.Cyto_GPPhasor_polar_obj[filename][Stack].append(Resultstest[Stack]["analysis"]["results_obj"][objn]["basicmembrane"][3])
                        elif Result[0]["analysis"]["results_whole_cyto"]:
                            self.Cytoprof[filename][Stack].append([])
                            self.Cyto_Image[filename][Stack].append([])
                            self.Object_Parameters_cyto[filename][Stack].append([])
                            self.Cyto_Intensities_per_object[filename][Stack].append([])
                            self.Cyto_GPPhasor_polar_obj[filename][Stack].append([])
                    
        elif (dims[0]!=1 and dims[1]!=1): #if Z and T 5D
            self.key[filename]="TZstack"
            self.GPImage[filename]=[]
            self.FullImage_Parameters[filename]=[]
            self.GPPhasor[filename]=[]
            self.GPPhasor_polar_all[filename]=[]
            self.Intensities[filename]=[]
            self.nobjects[filename]=[]
            self.GPPhasor_polar_obj[filename]=[]
            self.Intensities_per_object[filename]=[]
            self.GPImage_per_object[filename]=[]
            self.Object_Parameters[filename]=[]
            self.Object_Morphology[filename]=[]
            self.Object_Coordinates[filename]=[]
            self.Channellamda[filename]=[]
            self.Profile[filename]=[]
            self.MembraneSegments[filename]=[]
            if Result[0][0]["analysis"]["results_whole_cyto"]: 
                self.Cyto_GPImage[filename]=[]
                self.FullImage_Parameters_cyto[filename]=[]
                self.Cyto_GPPhasor_polar_all[filename]=[]
                self.Cyto_Intensities[filename]=[]
                self.Cyto_Intensities_per_object[filename]=[]
                self.Cyto_GPPhasor_polar_obj[filename]=[]
                self.Cytoprof[filename]=[]
                self.Cyto_Image[filename]=[]
                self.Object_Parameters_cyto[filename]=[]
        
            for T_Stack in Result:
                self.GPImage[filename].append([])
                self.FullImage_Parameters[filename].append([])
                self.GPPhasor[filename].append([])
                self.GPPhasor_polar_all[filename].append([])
                self.Intensities[filename].append([])
                self.nobjects[filename].append([])
                self.GPPhasor_polar_obj[filename].append([])
                self.Intensities_per_object[filename].append([])
                self.GPImage_per_object[filename].append([])
                self.Object_Parameters[filename].append([])
                self.Object_Morphology[filename].append([])
                self.Object_Coordinates[filename].append([])
                self.Channellamda[filename].append([])
                self.Profile[filename].append([])
                self.MembraneSegments[filename].append([])
                if Result[0][0]["analysis"]["results_whole_cyto"]: 
                    self.Cyto_GPImage[filename].append([])
                    self.FullImage_Parameters_cyto[filename][T_Stack].append([])
                    self.Cyto_GPPhasor_polar_all[filename].append([])
                    self.Cyto_Intensities[filename].append([])
                    self.Cyto_Intensities_per_object[filename].append([])
                    self.Cyto_GPPhasor_polar_obj[filename].append([])
                    self.Cytoprof[filename].append([])
                    self.Cyto_Image[filename].append([])
                    self.Object_Parameters_cyto[filename].append([])
                for Z_Stack in Result[T_Stack]:
                    if Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"]: 
                        self.Cyto_Intensities[filename][T_Stack].append([])
                        self.Cyto_GPImage[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"][2])
                        self.FullImage_Parameters_cyto[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"][0]["Parameters"])
                        self.Cyto_GPPhasor_polar_all[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"][3])
                        self.Cyto_Intensities[filename][T_Stack][Z_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"][0]["Wavelengths (nm)"])
                        self.Cyto_Intensities[filename][T_Stack][Z_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole_cyto"][0]["Norm. Intensity"])
                    self.GPImage[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][2])
                    self.FullImage_Parameters[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][0]["Parameters"])
                    self.GPPhasor[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][3])
                    self.GPPhasor_polar_all[filename][T_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][3])
                    self.Intensities[filename][T_Stack].append([])
                    self.Intensities[filename][T_Stack][Z_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][0]["Wavelengths (nm)"])
                    self.Intensities[filename][T_Stack][Z_Stack].append(Result[T_Stack][Z_Stack]["analysis"]["results_whole"][0]["Norm. Intensity"])
                    
                    self.nobjects[filename][T_Stack].append(0)
                    self.Channellamda[filename][T_Stack].append([])
                    self.GPPhasor_polar_obj[filename][T_Stack].append([])
                    self.GPImage_per_object[filename][T_Stack].append([])
                    self.Object_Parameters[filename][T_Stack].append([])
                    self.Object_Morphology[filename][T_Stack].append([])
                    self.Intensities_per_object[filename][T_Stack].append([])
                    self.Object_Coordinates[filename][T_Stack].append([])
                    self.Profile[filename][T_Stack].append([])
                    self.MembraneSegments[filename][T_Stack].append([])
                    if Result[0][0]["analysis"]["results_whole_cyto"]: 
                        self.Cytoprof[filename][T_Stack].append([])
                        self.Cyto_Image[filename][T_Stack].append([])
                        self.Object_Parameters_cyto[filename][T_Stack].append([])
                        self.Cyto_Intensities_per_object[filename][T_Stack].append([])
                        self.Cyto_GPPhasor_polar_obj[filename][T_Stack].append([])
        
                    if len(Result[T_Stack][Z_Stack]["analysis"]["results_obj"])!=0:
                        self.nobjects[filename][T_Stack][Z_Stack]=len(Result[T_Stack][Z_Stack]["analysis"]["results_obj"])
                        self.Channellamda[filename][T_Stack][Z_Stack].append(Lambdachannel)
                        self.GPPhasor_polar_obj[filename][T_Stack][Z_Stack]=[]
                        self.GPImage_per_object[filename][T_Stack][Z_Stack]=[]
                        self.Object_Parameters[filename][T_Stack][Z_Stack]=[]
                        self.Object_Morphology[filename][T_Stack][Z_Stack]=[]
                        self.Intensities_per_object[filename][T_Stack][Z_Stack]=[]
                        self.Object_Coordinates[filename][T_Stack][Z_Stack]=[]
                        self.Profile[filename][T_Stack][Z_Stack]=[]
                        self.MembraneSegments[filename][T_Stack][Z_Stack]=[]
                        if Result[0][0]["analysis"]["results_whole_cyto"]: 
                            self.Cytoprof[filename][T_Stack][Z_Stack]=[]
                            self.Cyto_Image[filename][T_Stack][Z_Stack]=[]
                            self.Object_Parameters_cyto[filename][T_Stack][Z_Stack]=[]
                            self.Cyto_Intensities_per_object[filename][T_Stack][Z_Stack]=[]
                            self.Cyto_GPPhasor_polar_obj[filename][T_Stack][Z_Stack]=[]
                        
                        for objn in Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"]:
                            self.GPPhasor_polar_obj[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][3])
                            
                            self.GPImage_per_object[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][2])
                            self.Object_Parameters[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Parameters"])
                            self.Object_Morphology[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["morphology"][2:])
                            self.Intensities_per_object[filename][T_Stack][Z_Stack].append([])
                            self.Intensities_per_object[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Wavelengths (nm)"])
                            self.Intensities_per_object[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][0]["Norm. Intensity"])
                            self.Object_Coordinates[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["morphology"][1])
                            if len(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["profile"]) !=0:
                                self.Profile[filename][T_Stack][Z_Stack].append([])
                                self.Profile[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["profile"][0])
                                self.MembraneSegments[filename][T_Stack][Z_Stack].append([])
                                self.MembraneSegments[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["profile"][6])
                            else:
                                self.Profile[filename][T_Stack][Z_Stack].append([])
                                self.MembraneSegments[filename][T_Stack][Z_Stack].append([])
                            if len(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basiccyto"]) !=0:
                                self.Cytoprof[filename][T_Stack][Z_Stack].append([])
                                self.Cytoprof[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["objlinearization"])
                                self.Cyto_Image[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basiccyto"][2])
                                self.Object_Parameters_cyto[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Parameters"])
                                self.Cyto_Intensities_per_object[filename][T_Stack][Z_Stack].append([])
                                self.Cyto_Intensities_per_object[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Wavelengths (nm)"])
                                self.Cyto_Intensities_per_object[filename][T_Stack][Z_Stack][int(objn)-1].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basiccyto"][0]["Norm. Intensity"])
                                self.Cyto_GPPhasor_polar_obj[filename][T_Stack][Z_Stack].append(Resultstest[T_Stack][Z_Stack]["analysis"]["results_obj"][objn]["basicmembrane"][3])
                            elif Result[0][0]["analysis"]["results_whole_cyto"]:
                                self.Cytoprof[filename][T_Stack][Z_Stack].append([])
                                self.Cyto_Image[filename][T_Stack][Z_Stack].append([])
                                self.Object_Parameters_cyto[filename][T_Stack][Z_Stack].append([])
                                self.Cyto_Intensities_per_object[filename][T_Stack][Z_Stack].append([])
                                self.Cyto_GPPhasor_polar_obj[filename][T_Stack][Z_Stack].append([])
        else:
            self.key[filename]="3dim"
            if isinstance(Result, dict):                            
                if Result["analysis"]["results_whole_cyto"]:
                    self.Cyto_Intensities[filename]=[]
                    self.Cyto_GPImage[filename]=Result["analysis"]["results_whole_cyto"][2] # GPImage
                    self.FullImage_Parameters_cyto[filename]=Result["analysis"]["results_whole_cyto"][0]["Parameters"]
                    self.Cyto_GPPhasor_polar_all[filename]=Result["analysis"]["results_whole_cyto"][3] #GPPhasor
                    self.Cyto_Intensities[filename].append(Result["analysis"]["results_whole_cyto"][0]["Wavelengths (nm)"])
                    self.Cyto_Intensities[filename].append(Result["analysis"]["results_whole_cyto"][0]["Norm. Intensity"]) #Intensity per channel
                self.GPImage[filename]=Result["analysis"]["results_whole"][2] # GPImage
                self.FullImage_Parameters[filename]=Result["analysis"]["results_whole"][0]["Parameters"] # GPImage
                self.GPPhasor[filename]=Result["analysis"]["results_whole"][3] #???
                self.GPPhasor_polar_all[filename]=Result["analysis"]["results_whole"][3] #GPPhasor
                self.Intensities[filename]=[]
                self.Intensities[filename].append(Result["analysis"]["results_whole"][0]["Wavelengths (nm)"])
                self.Intensities[filename].append(Result["analysis"]["results_whole"][0]["Norm. Intensity"])
                self.nobjects[filename]=0
            if len(Result["analysis"]["results_obj"])!=0:                           
                self.nobjects[filename]=len(Resultstest["analysis"]["results_obj"])
                self.Object_Parameters[filename]=[]
                self.Object_Morphology[filename]=[]
                self.GPPhasor_polar_obj[filename]=[]
                self.Intensities_per_object[filename]=[]
                self.GPImage_per_object[filename]=[]
                self.Object_Coordinates[filename]=[]
                self.Channellamda[filename]=[]
                self.Channellamda[filename]=Lambdachannel
                self.Profile[filename]=[]
                self.MembraneSegments[filename]=[]
                if Result["analysis"]["results_whole_cyto"]: 
                    self.Cyto_Intensities_per_object[filename]=[]
                    self.Cyto_GPPhasor_polar_obj[filename]=[]
                    self.Cytoprof[filename]=[]
                    self.Cyto_Image[filename]=[]
                    self.Object_Parameters_cyto[filename]=[]
                for objn in Resultstest["analysis"]["results_obj"]:
                    self.GPPhasor_polar_obj[filename].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][3])
                    self.GPImage_per_object[filename].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][2])
                    self.Object_Parameters[filename].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][0]["Parameters"])
                    self.Object_Morphology[filename].append(Resultstest["analysis"]["results_obj"][objn]["morphology"][2:])
                    self.Intensities_per_object[filename].append([])
                    self.Intensities_per_object[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][0]["Wavelengths (nm)"])
                    self.Intensities_per_object[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][0]["Norm. Intensity"])
                    self.Object_Coordinates[filename].append(Resultstest["analysis"]["results_obj"][objn]["morphology"][1])
                    if len(Resultstest["analysis"]["results_obj"][objn]["profile"]) !=0:
                        self.Profile[filename].append([])
                        self.Profile[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["profile"][0])
                        self.MembraneSegments[filename].append([])
                        self.MembraneSegments[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["profile"][6])
                    else:
                        self.Profile[filename].append([])
                        self.MembraneSegments[filename].append([])
                    if len(Resultstest["analysis"]["results_obj"][objn]["basiccyto"]) !=0 :
                        self.Cytoprof[filename].append([])
                        self.Cytoprof[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["objlinearization"])
                        self.Cyto_Image[filename].append(Resultstest["analysis"]["results_obj"][objn]["basiccyto"][2])
                        self.Object_Parameters_cyto[filename].append(Resultstest["analysis"]["results_obj"][objn]["basiccyto"][0]["Parameters"])
                        self.Cyto_Intensities_per_object[filename].append([])
                        self.Cyto_Intensities_per_object[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["basiccyto"][0]["Wavelengths (nm)"])
                        self.Cyto_Intensities_per_object[filename][int(objn)-1].append(Resultstest["analysis"]["results_obj"][objn]["basiccyto"][0]["Norm. Intensity"])
                        self.Cyto_GPPhasor_polar_obj[filename].append(Resultstest["analysis"]["results_obj"][objn]["basicmembrane"][3])
                    elif Result["analysis"]["results_whole_cyto"]:
                        self.Cytoprof[filename].append([])
                        self.Cyto_Intensities_per_object[filename].append([])
                        self.Cyto_GPPhasor_polar_obj[filename].append([])


def exception_hook(exctype, value, traceback_obj):
    # Define the format of your log message
    log_message = f"{'='*80}\n"  # Separator line
    log_message += f"Timestamp: {time.asctime(time.localtime())}\n"  # Timestamp
    log_message += f"Exception type: {exctype.__name__}\n"  # Exception type
    log_message += f"Exception message: {value}\n"  # Exception message
    log_message += "".join(traceback.format_tb(traceback_obj))  # Stack trace
    
    # Define the path to your log file
    if getattr(sys, 'frozen', False):
        # For standalone executables
        current_directory =dirname(sys.executable)
    else:
        # For running as a script
#                 current_directory = dirname(abspath(__file__))
        # or 
        current_directory = getcwd()
    log_file_path = join(current_directory, 'global_error_log.txt')
    
    # Write the log message to the file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)
    
    """Custom exception hook."""
    QMessageBox.critical(None, "An exception was raised", f"Exception type: {exctype.__name__}\n{value}")
    sys.exit(1)

sys.excepthook = exception_hook

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_dark_palette(app)
    window = MainWindow()
    #pyi_splash.close()
    app.processEvents() 
    window.showMaximized()
    sys.exit(app.exec_())
    #app.exec_()
