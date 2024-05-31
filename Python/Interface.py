
import AllFunctions as F
import Analyzer_V1_0_0 as analyze
from Packages import np, plt, tfl, time

def openformat(Filename):
    if Filename.lower().endswith('.lsm'):
        image = tfl.imread(Filename)
        meta = tfl.TiffFile(Filename).lsm_metadata
        Pixelsize = meta['VoxelSizeX']
        Nchannels = meta['DimensionChannels']
        # Lambdachannel = np.array(meta['ChannelColors']['ColorNames'], dtype='int')
        Lambdachannel = np.array(meta['ChannelColors']['ColorNames'])
        rowMax = meta['DimensionY']
        colMax = meta['DimensionX']
        dimT = meta['DimensionTime']
        dimZ = meta['DimensionZ']

        return Pixelsize, Nchannels, Lambdachannel, image, [dimT, dimZ, Nchannels, rowMax, colMax], meta



path = 'C:/Users/luca.andronico/Desktop/multidim/1.lsm'
savepath = "C:/Users/luca.andronico/Desktop/multidim"
pathsave = path
Filename = path
filename = "1.lsm"

Pixelsize, Nchannels, Lambdachannel, imageR, dims, metat = openformat(path)
Lambdachannel = list(map(str, Lambdachannel))

print(Lambdachannel)
print(Pixelsize)

# imageRr = np.zeros((imageR.shape[0], imageR.shape[2], imageR.shape[2], imageR.shape[1]))
# for b in range(0, imageR.shape[0]):
#     for a in range(0, imageR.shape[1]):
#         imageRr[b, :, :, a] = imageR[b, a, :, :]
print(imageR.shape)
imageRr = np.zeros((imageR.shape[1], imageR.shape[2], imageR.shape[0]))
for a in range(0, imageR.shape[0]):
    imageRr[:, :, a] = imageR[a, :, :]
imageR = imageRr  # IMPORTANT !!!!!!

# Variables -------------------------------------------------- !!!!!

mode = 1
image = imageR

PixelDepth = 8
stddev = 1
S_N = 5
bgmean = 'NaN'
bgmean_cyto = 'NaN'

filter_type = 'Gaussian'
filter_val = 1

filter_typecyto = 'NaN'
filter_valcyto = 2

lambdaThr = ['423', '494']
text = '(A - B) / (A + B)'
varlist = ['423', '494', 'NaN', 'NaN']
ObjectDetection = True
n_debranch = 1                              # n_debranch = how many cycles of debranching (maybe >1 for adherent cells)
tol0 = 1                                    # tol0 = how much to retract from skeleton
tol1 = 5                                    # this is to set the tolerance in segmenting the skel and membrane

profiler = True
profilershape = "square"  # from GUI
autoff = True  # from GUI #Auto Cut off in Profiler
PDiamCutoff = 0.1  # from GUI
proDim1 = 5  # from GUI
proDim2 = 5  # from GUI
Profpars = [profilershape, (proDim1, proDim2), PDiamCutoff]
recentering = False
dim_line = 10  # line for recentering

profile_cyto = False
lambdaThr_cyto = []
text_cyto = 'B / A'
varlist_cyto = ['Ch1-T1', 'Ch2-T1', 'NaN', 'NaN']

objlinear = True
radius = 'auto'

colocalization = []

savecroppedmembrane = True
savecroppedcyto = True
savelinearized = True
savecroppedpath = savepath
savephasors = False

Dict = {'datamask': [], 'analysis': []}

histpars = [-1, 1, 0.05]
histpars_cyto = [0, 10, 0.05]

MaskParams_mem = {'Ttype': 'Otsu', 'ValManual': 40, 'compress': False, 'Kvalue': 0.1, 'objSize': 'NaN',
              'holesSize': 2,
              'pxlSize': Pixelsize, 'dilate': False, 'shape': 'disk', 'dim1': 1, 'dim2': 3, 'PixelDepth': PixelDepth,
              'filter_type': filter_type, 'filter_val': filter_val, 'stddev': stddev, 'S_N': S_N, 'bgmean': bgmean,
                  'lambdaThr': lambdaThr}

MaskParams_cyto = {'Ttype': 'Otsu', 'ValManual': 30, 'compress': False, 'Kvalue': 0.5, 'objSize': 'NaN',
              'holesSize': 'NaN',
              'pxlSize': Pixelsize, 'dilate': False, 'shape': 'disk', 'dim1': 1, 'dim2': 3, 'PixelDepth': PixelDepth,
              'filter_type': filter_typecyto, 'filter_val': filter_valcyto, 'stddev': stddev, 'S_N': S_N, 'bgmean': bgmean_cyto,
                   'lambdaThr': lambdaThr_cyto}


dict_results = analyze.GP_Analyser(mode, filename, Lambdachannel, image, dims, varlist, ObjectDetection, profiler,
                profilershape, autoff, PDiamCutoff, proDim1, proDim2, text, histpars, histpars_cyto,
                text_cyto, profile_cyto, varlist_cyto, n_debranch, tol0, tol1, savecroppedmembrane, savecroppedcyto,
                savelinearized, savepath, objlinear, recentering, dim_line, MaskParams_mem, MaskParams_cyto,
                colocalization, savephasors, radius)


# for g in range(0, len(dict_results['analysis']['results_obj'])):
#     print(dict_results['analysis']['results_obj'][g+1]['basicmembrane'][0]['Parameters'][1])

plt.figure(1)
plt.imshow(dict_results['datamask'][2])
plt.show()
# plt.imshow(dict_results['datamask'][8])
# plt.subplot(223)
# plt.imshow(dict_results['analysis']['results_obj'][2]['morphology'][0])
# plt.subplot(224)
plt.figure(2)
cmap3 = plt.cm.get_cmap('viridis')
cmap3.set_bad('k')
plt.imshow(dict_results['analysis']['results_whole'][2], cmap=cmap3)
plt.colorbar()
plt.show()
