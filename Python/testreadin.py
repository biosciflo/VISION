# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:24:02 2024

@author: P41650
"""

import numpy as np
import tifffile as lsm
import czifile
from readlif.reader import LifFile
import xmltodict
#%%

path=("G:/My Drive/Arbeiten/Projekte/GP_Analyzer_LUCA_FLO/Bugs/Lucas int str bug/")
filename=("JC-1+Pro12A_1.lsm")
# filename=("2channels_16bit.lsm")
fullpath=path+"/"+filename


#def load_and_process_lsm(fullpath):
#for spectral ana multi chanell
metadata = {
"Pixelsize": None,
"Nchannels": None,
"ChannelColors": None,
"Dimensions": None,
"BitDepth": None,
"PixelsizeUnit": None
}
DimensionTime = DimensionZ = DimensionX = DimensionY = DimensionChannels = 1

with lsm.TiffFile(fullpath) as tif:
    if hasattr(tif, 'lsm_metadata'):
        lsm_metadata = tif.lsm_metadata

    metadata['Pixelsize'] = lsm_metadata.get("VoxelSizeX", None)
    DimensionChannels = lsm_metadata.get("DimensionChannels", 1)
    metadata['Nchannels'] = DimensionChannels
    
    if "ChannelColors" in lsm_metadata and all(item.isdigit() for item in lsm_metadata["ChannelColors"]["ColorNames"]):
        metadata['ChannelColors'] = [str(int(item)) for item in lsm_metadata["ChannelColors"]["ColorNames"]]
    else:
        metadata['ChannelColors'] = [str(int((value))) for value in (np.mean(lsm_metadata["ChannelWavelength"], axis=1) * 1e9)]
    
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
    
    
    #return data, metadata
    
    
    
    
#%%


path=("G:/My Drive/Arbeiten/Projekte/GP_Analyzer_LUCA_FLO/TESTCASE_IMAGES/ome.tiff/LSM/")
filename=("hdl beads Image 34_lsm.ome.tif")
# filename=("2channels_16bit.lsm")
fullpath=path+"/"+filename


# def load_and_process_ometiff(fullpath):
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
                    if channels["@Name"]:
                        metadata['ChannelColors'].append((channels["@Name"]))
                        i+=1
                else:
                    metadata['ChannelColors'].append(str(i))
                    i+=1
        else:
            metadata['ChannelColors'].append(str(i))
            
        metadata['ChannelColors']=np.array(metadata['ChannelColors']).tolist()
        
        DimensionChannels=int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeC"])
        DimensionTime = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeT"])
        DimensionZ = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeZ"])
        DimensionX = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeX"])
        DimensionY = int(ometiff_metadata["OME"]["Image"]["Pixels"]["@SizeY"])
        
        metadata['Dimensions']=[DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]
        
        metadata['BitDepth'] = ometiff_metadata["OME"]["Image"]["Pixels"]["@Type"]
        digits = [char for char in metadata['BitDepth'] if char.isdigit()]
        metadata['BitDepth'] = int(''.join(digits))
        metadata['PixelsizeUnit'] = ometiff_metadata["OME"]["Image"]["Pixels"]["@PhysicalSizeXUnit"]
        
        data = tif.asarray()
        
        if metadata['PixelsizeUnit'] == 'µm':
            metadata['Pixelsize'] = metadata['Pixelsize'] * 1E-6
        elif metadata['PixelsizeUnit'] == 'nm':
            metadata['Pixelsize'] = metadata['Pixelsize'] * 1E-9
        elif metadata['PixelsizeUnit'] == 'mm':
            metadata['Pixelsize'] = metadata['Pixelsize'] * 1E-3
        
        if metadata['Nchannels'] >1:
            if data.ndim == 3:
                data = np.transpose(data, (1, 2, 0))
            elif data.ndim == 4:
                data = np.transpose(data, (0, 2, 3, 1))
            elif data.ndim == 5:
                data = np.transpose(data, (0, 1, 3, 4, 2))
        else:
            data = np.expand_dims(data, axis=-1)
            
#return data,metadata

        
#%%


path=("D:/Google Drive/Arbeiten/Projekte/GP_Analyzer_LUCA_FLO/TESTCASE_IMAGES/CZI/")
filename=("t_Image 14.czi")
fullpath=path+"/"+filename
#for spectral ana multi chanell
metadata = {
    "Pixelsize": None,
    "Nchannels": None,
    "ChannelColors": [],
    "Dimensions": None,
    "BitDepth": None,
    "PixelsizeUnit": None
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
    i=1
    for subdict in czi_metadata["ImageDocument"]["Metadata"]["Information"]["Image"]["Dimensions"]["Channels"]["Channel"]:
        if subdict ["@Name"].isdigit():
            metadata['ChannelColors'].append((subdict["@Name"]))
        elif "EmissionWavelength" in subdict:
            metadata['ChannelColors'].append(str(int(float(subdict["EmissionWavelength"]))))
        else:
            metadata['ChannelColors'].append(subdict ["@Name"]) #if needed we can add the names here but than we have to change in lucas codes somewere something or i have to translate the names into integers again so it works seemlessly for him
            #metadata['ChannelColors'].append(int(i))
            i+=1
    
    metadata['ChannelColors']=np.array(metadata['ChannelColors']).tolist()

image=czifile.imread(fullpath)
if len(image.shape) < 8:
    data = np.squeeze(np.transpose(czifile.imread(fullpath)[0, 0, :, :, :, :, 0], (1, 2, 3, 0))) # wenn hier eins mit T oder Z kommt dann gibts probleme denn ich weis nicht was was ist
else:
    data = np.squeeze(np.transpose(czifile.imread(fullpath)[0, 0, :, :, :, :, :, 0], (1, 2, 3, 4, 0)))


#%%

path=("D:/Google Drive/Arbeiten/Projekte/GP_Analyzer_LUCA_FLO/VISION_V1.0.2/")
filename=("Example 1 Ishikawa BODIPY FSH 10nM 24h.lif")
fullpath=path+"/"+filename

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
    "BitDepth": [],
    "PixelsizeUnit": None
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
    
    metadata[i]['ChannelColors']=np.array(metadata[i]['ChannelColors']).tolist()
    metadata[i]['Dimensions']=[DimensionTime, DimensionZ, DimensionX, DimensionY, DimensionChannels]

    i+=1