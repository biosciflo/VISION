from Packages import np, skmM, skmF, ndi, slC, skM, imgIO, pd, os, sys, skcanny, tfl, plt, ndi


def abovenoise(image, varidxs, S_N, stddev, bgmean, idx_col):
    if len(varidxs) == 1:
        if bgmean == 'NaN':
            N_medianA = np.median(image[:, :, varidxs[0]])
        else:
            N_medianA = bgmean
        Thr_A = S_N * stddev + N_medianA  # this is how to select pixels in each channel
        mask_varA = image[:, :, varidxs[0]] >= Thr_A

        Thr_abovenoise = [Thr_A]
        mask = mask_varA

    if len(varidxs) == 2:
        if bgmean == 'NaN':
            N_medianA = np.median(image[:, :, varidxs[0]])
            N_medianB = np.median(image[:, :, varidxs[1]])
        else:
            N_medianA = bgmean
            N_medianB = bgmean

        Thr_A = S_N * stddev + N_medianA  # this is how to select pixels in each channel
        mask_varA = image[:, :, varidxs[0]] >= Thr_A

        Thr_B = S_N * stddev + N_medianB  # this is how to select pixels in each channel
        mask_varB = image[:, :, varidxs[1]] >= Thr_B

        Thr_abovenoise = [Thr_A, Thr_B]
        mask = np.logical_and(mask_varA, mask_varB)

    if len(varidxs) == 3:
        if bgmean == 'NaN':
            N_medianA = np.median(image[:, :, varidxs[0]])
            N_medianB = np.median(image[:, :, varidxs[1]])
            N_medianC = np.median(image[:, :, varidxs[2]])
        else:
            N_medianA = bgmean
            N_medianB = bgmean
            N_medianC = bgmean

        Thr_A = S_N * stddev + N_medianA  # this is how to select pixels in each channel
        mask_varA = image[:, :, varidxs[0]] >= Thr_A

        Thr_B = S_N * stddev + N_medianB  # this is how to select pixels in each channel
        mask_varB = image[:, :, varidxs[1]] >= Thr_B

        Thr_C = S_N * stddev + N_medianC  # this is how to select pixels in each channel
        mask_varC = image[:, :, varidxs[2]] >= Thr_C
        Thr_abovenoise = [Thr_A, Thr_B, Thr_C]

        mask = np.logical_and.reduce((mask_varA, mask_varB, mask_varC))

    if len(varidxs) == 4:
        if bgmean == 'NaN':
            N_medianA = np.median(image[:, :, varidxs[0]])
            N_medianB = np.median(image[:, :, varidxs[1]])
            N_medianC = np.median(image[:, :, varidxs[2]])
            N_medianD = np.median(image[:, :, varidxs[3]])
        else:
            N_medianA = bgmean
            N_medianB = bgmean
            N_medianC = bgmean
            N_medianD = bgmean

        Thr_A = S_N * stddev + N_medianA  # this is how to select pixels in each channel
        mask_varA = image[:, :, varidxs[0]] >= Thr_A

        Thr_B = S_N * stddev + N_medianB  # this is how to select pixels in each channel
        mask_varB = image[:, :, varidxs[1]] >= Thr_B

        Thr_C = S_N * stddev + N_medianC  # this is how to select pixels in each channel
        mask_varC = image[:, :, varidxs[2]] >= Thr_C

        Thr_D = S_N * stddev + N_medianD  # this is how to select pixels in each channel
        mask_varD = image[:, :, varidxs[3]] >= Thr_D
        Thr_abovenoise = [Thr_A, Thr_B, Thr_C, Thr_D]

        mask = np.logical_and.reduce((mask_varA, mask_varB, mask_varC, mask_varD))
    if ~np.isnan(idx_col[0]):
        if bgmean == 'NaN':
            N_median_col = np.median(image[:, :, idx_col])
        else:
            N_median_col = bgmean
        Thr_col = S_N * stddev + N_median_col

        Thr_abovenoise.append(Thr_col)

    return mask, Thr_abovenoise


def nosaturated(image, notnoisemask, varidxs, depth):
    if depth == 8:
        satThr = 2 ** 8 - 1
    if depth == 12:
        satThr = 2 ** 12 - 1
    if depth == 16:
        satThr = 2 ** 16 - 1

    if len(varidxs) == 1:
        notsat_A = image[:, :, varidxs[0]] < satThr
        combinemask = np.logical_and.reduce((notnoisemask, notsat_A))

    if len(varidxs) == 2:
        notsat_A = image[:, :, varidxs[0]] < satThr
        notsat_B = image[:, :, varidxs[1]] < satThr
        combinemask = np.logical_and.reduce((notnoisemask, notsat_A, notsat_B))

    if len(varidxs) == 3:
        notsat_A = image[:, :, varidxs[0]] < satThr
        notsat_B = image[:, :, varidxs[1]] < satThr
        notsat_C = image[:, :, varidxs[2]] < satThr
        combinemask = np.logical_and.reduce((notnoisemask, notsat_A, notsat_B, notsat_C))

    if len(varidxs) == 4:
        notsat_A = image[:, :, varidxs[0]] < satThr
        notsat_B = image[:, :, varidxs[1]] < satThr
        notsat_C = image[:, :, varidxs[2]] < satThr
        notsat_D = image[:, :, varidxs[3]] < satThr
        combinemask = np.logical_and.reduce((notnoisemask, notsat_A, notsat_B, notsat_C, notsat_D))

    satperc = (np.sum(notnoisemask) - np.sum(combinemask)) / np.sum(notnoisemask) * 100

    return combinemask, satperc


def spectrum(img, combinedmask):
    IntSum = []
    for a in range(0, img.shape[-1]):
        slice = img[:, :, a]
        IntSum.append(np.sum(slice[combinedmask]))
    IntSum = np.asarray(IntSum)
    IntSum = IntSum / np.max(IntSum) * 100

    return IntSum


def thresholding(img, sigma, varidsx, depth, combinedmask, idxThr, which, value=1, compression=False, k=0.1):
    if sigma != 'NaN':
        img = np.round(skmF.gaussian(img, sigma=sigma, preserve_range=True))

    if depth == 8:
        maxVal = 2 ** 8 - 1
    if depth == 12:
        maxVal = 2 ** 12 - 1
    if depth == 16:
        maxVal = 2 ** 16 - 1

    if len(varidsx) == 1:
        slice_A = img[:, :, varidsx[0]]
        brightnesses = [np.sum(slice_A[combinedmask]) / np.sum(combinedmask)]

    if len(varidsx) == 2:
        slice_A = img[:, :, varidsx[0]]  # take only the mask within the selected channel !!!!!!!!!!!!
        slice_B = img[:, :, varidsx[1]]
        brightnesses = [np.sum(slice_A[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_B[combinedmask]) / np.sum(combinedmask)]

    if len(varidsx) == 3:
        slice_A = img[:, :, varidsx[0]]
        slice_B = img[:, :, varidsx[1]]
        slice_C = img[:, :, varidsx[2]]
        brightnesses = [np.sum(slice_A[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_B[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_C[combinedmask]) / np.sum(combinedmask)]

    if len(varidsx) == 4:
        slice_A = img[:, :, varidsx[0]]
        slice_B = img[:, :, varidsx[1]]
        slice_C = img[:, :, varidsx[2]]
        slice_D = img[:, :, varidsx[3]]
        brightnesses = [np.sum(slice_A[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_B[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_C[combinedmask]) / np.sum(combinedmask),
                        np.sum(slice_D[combinedmask]) / np.sum(combinedmask)]

    if idxThr != 'NaN':
        slice_Thr = img[:, :, idxThr]
        idx2 = idxThr
    else:
        dim_idx = np.argmin(brightnesses)
        slice_Thr = img[:, :, varidsx[dim_idx]]
        idx2 = varidsx[dim_idx]

    slice_Thr[~combinedmask] = 0  # this sets all the pixels which are below S/N and/or saturated to 0

    if compression:
        slice_Thr = np.round(maxVal - maxVal * np.exp(- k ** 3 * slice_Thr ** 3)).astype(int)
        thr = skmF.threshold_otsu(slice_Thr)
        maskThr = slice_Thr > thr

        return thr, maskThr, slice_Thr, idx2

    else:
        if which == 'Otsu':
            thr = skmF.threshold_otsu(slice_Thr)
            maskThr = slice_Thr > thr

            return thr, maskThr, slice_Thr, idx2

        else:
            thr = value
            maskThr = slice_Thr > thr

            return thr, maskThr, slice_Thr, idx2


def maskprep(mask, objsize, sizeholes, pixelsize, dilation=False, shape='square', d1=1, d2=1):
    if dilation:
        if shape == 'square':
            selem = skmM.square(d1)
        elif shape == 'disk':
            selem = skmM.disk(d1)
        elif shape == 'octagon':
            selem = skmM.octagon(d1, d2)
        RecMask = skmM.binary_dilation(mask, selem)
    else:
        RecMask = mask

    if objsize != 'NaN':
        RecMask = skmM.remove_small_objects(RecMask, min_size=int((objsize) ** 2 / (pixelsize * 10 ** 6) ** 2))

    if sizeholes != 'NaN':
        RecMask = skmM.remove_small_holes(RecMask, area_threshold=int(sizeholes ** 2 / (pixelsize * 10 ** 6) ** 2))

    coords = np.transpose(np.nonzero(RecMask))

    return RecMask, coords


def normhist(par, data):
    binhist = np.arange(par[0], par[1], par[2])  # par = [min, max, step]

    try:
        hist = (np.histogram(data, bins=binhist))[0]
        histnorm = hist / np.sum(hist) * 100

        return binhist[:-1], histnorm  # slice until the second last

    except:
        raise Exception("Check bin range for histogram")


def cart2pol(coor):
    if coor.ndim == 1:
        rho = np.sqrt(coor[1] ** 2 + coor[0] ** 2)  # coor are in the form y, x
        phi = np.arctan2(coor[0], coor[1])
    else:
        rho = np.sqrt(coor[:, 1] ** 2 + coor[:, 0] ** 2)  # coor are in the form y, x
        phi = np.arctan2(coor[:, 0], coor[:, 1])
    return rho, phi


def basicmeasure(img, reccoor, meta, varidxs, text, histpars):
    letters = []
    for i in text:
        if i.isalpha():
            letters.append(i)
    letters.sort()
    letters = list(set(letters))

    if len(varidxs) == 1:
        varA = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[0]], (-1, 1)).astype('int')

        GPlist = eval(text, {'np': np, letters[0]: varA})

    if len(varidxs) == 2:
        varA = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[0]], (-1, 1)).astype('int')
        varB = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[1]], (-1, 1)).astype('int')

        GPlist = eval(text, {'np': np, letters[0]: varA, letters[1]: varB})

    if len(varidxs) == 3:
        varA = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[0]], (-1, 1)).astype('int')
        varB = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[1]], (-1, 1)).astype('int')
        varC = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[2]], (-1, 1)).astype('int')

        GPlist = eval(text, {'np': np, letters[0]: varA, letters[1]: varB, letters[2]: varC})

    elif len(varidxs) == 4:
        varA = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[0]], (-1, 1)).astype('int')
        varB = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[1]], (-1, 1)).astype('int')
        varC = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[2]], (-1, 1)).astype('int')
        varD = np.reshape(img[reccoor[:, 0], reccoor[:, 1], varidxs[3]], (-1, 1)).astype('int')

        GPlist = eval(text, {'np': np, letters[0]: varA, letters[1]: varB, letters[2]: varC, letters[3]: varD})

    if len(GPlist) == 0:  # this is to avoid crashing
        print('No points above threshold for P value measurement')
        return []
    else:
        idxPosGP = np.isnan(GPlist)  # Removes NAN GPs values (when both Lo and Ld = 0)
        GPs = np.round(GPlist[~idxPosGP], 2)  # Filtered GP values
        filtercoor = reccoor[~idxPosGP[:, 0], :]  # Filtered coordinates (no NAN)
        # -----------------------------------------------------------------------------------------------------------
        Rejected = np.round((len(GPlist) - len(GPs)) / len(GPlist) * 100, 1)
        GPmedian = np.round(np.median(GPs), 2)  # whole img GPs median
        GPstDev = np.round(np.std(GPs), 2)  # whole img GPs std. dev.
        histBin, GPhistNorm = normhist(histpars, GPs)  # histogram of GPs on whole img
        GPhistNorm = np.round(GPhistNorm, 3)
        IntFrameNorm = np.round(
            np.sum(img[filtercoor[:, 0], filtercoor[:, 1], meta[3][0]]) / len(filtercoor))  # counts only pixels with
        # GP ~NaN on either Ld or Lo channel (the dimmer) img
        # -----------------------------------------------------------------------------------------------------------
        imgGPs = np.full_like(img[:, :, meta[3][0]], np.nan, dtype=float)
        imgGPs[filtercoor[:, 0], filtercoor[:, 1]] = GPs  # to create GP-color coded img0
        # -----------------------------------------------------------------------------------------------------------
        Int_array = img[filtercoor[:, 0], filtercoor[:, 1], :].T
        IntSum = np.sum(Int_array, axis=1).reshape(-1, 1)
        IntSumNorm = IntSum / np.max(IntSum)

        if len(varidxs) != 1:
            n = 1  # harmonic
            COS = np.cos(2 * n * np.pi * ((meta[0] - meta[0][0]) / (np.max(meta[0]) - np.min(meta[0])))).reshape(-1,
                                                                                                                 1)  # FOR PHASOR PLOT
            SIN = np.sin(2 * n * np.pi * ((meta[0] - meta[0][0]) / (np.max(meta[0]) - np.min(meta[0])))).reshape(-1, 1)
            PhasorX = np.sum(img[filtercoor[:, 0], filtercoor[:, 1], :].T * COS, axis=0).reshape(1, -1) / \
                      np.sum(Int_array, axis=0).reshape(1, -1)
            PhasorY = np.sum(img[filtercoor[:, 0], filtercoor[:, 1], :].T * SIN, axis=0).reshape(1, -1) / \
                      np.sum(Int_array, axis=0).reshape(1, -1)
            PhasorX = PhasorX.reshape(-1, 1)
            PhasorY = PhasorY.reshape(-1, 1)
            Finalcoor = np.concatenate((PhasorY, PhasorX), axis=1)
            Rho, Phi = cart2pol(Finalcoor)
            PhasorCor = np.concatenate((PhasorX, PhasorY), axis=1)
        else:
            PhasorCor = []
            Rho, Phi = [], []

        dict_for_saving = {'Parameters': [Rejected, GPmedian, GPstDev, IntFrameNorm],
                           'Wavelengths (nm)': meta[0].tolist(), 'Norm. Intensity': IntSumNorm[:, 0].tolist(),
                           'Bin': histBin.tolist(), 'Frequency (%)': GPhistNorm.tolist()}

        return [dict_for_saving, PhasorCor, imgGPs, [Rho, Phi]]


def clockwisebox(squareBox):  # this orient the coordinates clockwise
    angles = []
    lenvectors = []
    for i in range(len(squareBox)):
        lenvector, angle = cart2pol(squareBox[i, :])
        angles.append(angle)
        lenvectors.append(lenvector)
    sortedCoors = np.array([x for _, x in sorted(zip(zip(angles, lenvectors), squareBox))])  # clockwise sorted coords

    return sortedCoors


def structure(shape, size, hole=True):  # hole in the middle
    if shape == 'square':
        box = np.ones((size[0], size[1])).astype(int)
        centroid = np.array(ndi.center_of_mass(box)).astype(int)
        boxCoor = np.transpose(np.nonzero(box))
        boxCoor = boxCoor - centroid
        idxmed = np.median(np.arange(1, len(boxCoor))).astype(int)
        if hole:
            boxCoor = np.delete(boxCoor, idxmed, axis=0)
            return boxCoor
        return boxCoor
    elif shape == 'octagon':
        box = skmM.octagon(size[0], size[1])
        centroid = np.array(ndi.center_of_mass(box)).astype(int)
        boxCoor = np.transpose(np.nonzero(box))
        boxCoor = boxCoor - centroid
        idxmed = np.median(np.arange(1, len(boxCoor))).astype(int)
        if hole:
            boxCoor = np.delete(boxCoor, idxmed, axis=0)
            return boxCoor
        return boxCoor


def findedges(skel, coors):
    squareBox1 = structure('square', (3, 3), hole=True)  # THIS IS TO REMOVE BRANCHES IN THE SKELETON
    sortedCoors = clockwisebox(squareBox1)  # these are the coor sorted clockwise
    coors = coors.T
    sortedCoors = sortedCoors.T
    array_logic = np.zeros((sortedCoors.shape[1], coors.shape[1]), dtype=int)
    array_checkS = coors[:, :, np.newaxis] + sortedCoors[:, np.newaxis, :].astype(int)  # shape (2, n, 8)

    array_idx = np.arange(0, coors.shape[1]).astype(int)  # create the logic array of shape (2, n)
    array_logic[:, array_idx] = skel[array_checkS[0, array_idx, :], array_checkS[1, array_idx, :]].T
    array_logic = array_logic.astype(bool)

    first_non_zero_indices = np.argmax(array_logic != 0, axis=0)  # this is to roll all columns according to the shift
    shifts_for_rolling = np.where(np.any(array_logic != 0, axis=0), first_non_zero_indices, 0)
    idx_to_roll = np.tile(np.arange(0, 8, dtype='int').reshape(-1, 1), (1, len(first_non_zero_indices)))
    rolled_matrix = idx_to_roll - shifts_for_rolling
    minus_shift_logic = rolled_matrix < 0
    to_replace = rolled_matrix + sortedCoors.shape[1]
    rolled_matrix[minus_shift_logic] = to_replace[minus_shift_logic]

    sorted_indices = np.argsort(rolled_matrix, axis=0)
    array_newlogic = array_logic[sorted_indices, np.arange(array_logic.shape[1])]

    idx_row, idx_col = np.nonzero(array_newlogic == 0)
    idxs_newlogic = np.full(array_newlogic.shape, np.nan)
    idxs_newlogic[idx_row, idx_col] = idx_row

    index = np.argsort(np.isnan(idxs_newlogic), axis=0)
    idx_newlogic_sorted = np.take_along_axis(idxs_newlogic, index, axis=0)

    array_diff = np.diff(idx_newlogic_sorted, axis=0)
    array_diff_nonan = np.nan_to_num(array_diff, nan=1)

    array_result = np.all(array_diff_nonan == 1, axis=0).astype(int)

    idxs_edges = array_result == 1
    edges = coors[:, idxs_edges]

    return edges.T, array_checkS, array_logic, array_newlogic  # array (n, 2) where edges[:, 0] are the y coordinates


def tshape_corners(skel, newcoors):
    squareBox1 = structure('square', (3, 3), hole=True)  # THIS IS TO REMOVE BRANCHES IN THE SKELETON
    sortedCoors = clockwisebox(squareBox1)  # these are the coor sorted clockwise
    newcoors = newcoors.T
    sortedCoors = sortedCoors.T
    array_logic = np.zeros((sortedCoors.shape[1], newcoors.shape[1]), dtype=int)
    array_checkS = newcoors[:, :, np.newaxis] + sortedCoors[:, np.newaxis, :].astype(int)  # shape (2, n, 8)

    array_idx = np.arange(0, newcoors.shape[1]).astype(int)  # create the logic array of shape (2, n)
    array_logic[:, array_idx] = skel[array_checkS[0, array_idx, :], array_checkS[1, array_idx, :]].T
    array_logic = array_logic.astype(bool)

    first_non_zero_indices = np.argmax(array_logic != 0, axis=0)  # this is to roll all columns according to the shift
    shifts_for_rolling = np.where(np.any(array_logic != 0, axis=0), first_non_zero_indices, 0)
    idx_to_roll = np.tile(np.arange(0, 8, dtype='int').reshape(-1, 1), (1, len(first_non_zero_indices)))
    rolled_matrix = idx_to_roll - shifts_for_rolling
    minus_shift_logic = rolled_matrix < 0
    to_replace = rolled_matrix + sortedCoors.shape[1]
    rolled_matrix[minus_shift_logic] = to_replace[minus_shift_logic]

    sorted_indices = np.argsort(rolled_matrix, axis=0)
    array_newlogic = array_logic[sorted_indices, np.arange(array_logic.shape[1])]

    array_sum = np.sum(array_logic, axis=0)

    # ------------------------------------------------------------------------------ TO REMOVE CORNERS
    idx_points2 = np.where(array_sum == 2)[0]  # shape (l,) of original indices

    if len(idx_points2) != 0:
        subarray_newlogic2 = array_newlogic[:, idx_points2]
        array_1pixeldist = np.argmax(np.where(subarray_newlogic2,
                                              np.arange(subarray_newlogic2.shape[0]).reshape(-1, 1), -1), axis=0)
        idx_dist1 = np.where(np.logical_or(array_1pixeldist == 2, array_1pixeldist == 6))[0]  # shape (l1,)
        idx_points2_dist1 = idx_points2[idx_dist1]

        if len(idx_points2_dist1) != 0:
            filtered_array_check2 = array_checkS[:, idx_points2_dist1, :]
            filtered_array_logic2 = array_logic[:, idx_points2_dist1].T
            filtered_array_logic2 = filtered_array_logic2[np.newaxis, :, :]
            filtered_array_logic2 = np.concatenate((filtered_array_logic2, filtered_array_logic2), axis=0)

            shrunk_filtered_array_check2 = filtered_array_check2[filtered_array_logic2].reshape(2,
                                                                                                len(idx_points2_dist1),
                                                                                                -1)
            cond_1 = shrunk_filtered_array_check2[0, :, 0] != shrunk_filtered_array_check2[0, :, 1]  # dims 1: (y, x)
            cond_2 = shrunk_filtered_array_check2[1, :, 0] != shrunk_filtered_array_check2[1, :, 1]

            subidx_corners = np.logical_and(cond_1, cond_2)  # booleans of shape (l1,)
            idx_corners = idx_points2_dist1[subidx_corners]

            if len(idx_corners) != 0:
                skel[newcoors[0, idx_corners], newcoors[1, idx_corners]] = False

    # ------------------------------------------------------------------------------ TO REMOVE T-shapes_3
    idx_points3 = np.where(array_sum == 3)[0]

    if len(idx_points3) != 0:
        subarray_check3 = array_checkS[:, idx_points3, :]

        subarray_logic3 = array_logic[:, idx_points3].T
        subarray_logic3 = subarray_logic3[np.newaxis, :, :]
        subarray_logic3 = np.concatenate((subarray_logic3, subarray_logic3), axis=0)

        shrunk_subarray_check3 = subarray_check3[subarray_logic3].reshape(2, subarray_check3.shape[1], -1)
        sub_newcoors_3 = newcoors[:, idx_points3, np.newaxis]

        array_distarray = np.linalg.norm(sub_newcoors_3 - shrunk_subarray_check3, axis=0)
        distance = np.around(np.sum(array_distarray, axis=1), decimals=1)

        idx_tshape = distance == 3

        if np.sum(idx_tshape) != 0:
            skel[sub_newcoors_3[0, idx_tshape, 0], sub_newcoors_3[1, idx_tshape, 0]] = False

        # ------------------------------------------------------------------------------ TO REMOVE other points
        # this is to check if point are type 5 sum=3.4

        extended_subarray_check3 = np.concatenate(
            [shrunk_subarray_check3, shrunk_subarray_check3[:, :, 0, np.newaxis]],
            axis=2)
        ext_subarray_check3diff = np.diff(extended_subarray_check3, axis=2)
        ext_subarray_check3diff_log = np.any(ext_subarray_check3diff == 0, axis=2)

        idx_3_4 = distance == 3.4  # these are the filters
        idx_type5 = np.sum(ext_subarray_check3diff_log, axis=0) == 1
        idx_3_4_type5 = np.logical_and(idx_3_4, idx_type5)

        sub_sub_newcoors_3 = sub_newcoors_3[:, idx_3_4_type5, 0].T

        skel_doubles = np.full((skel.shape), np.nan)
        skel_doubles[sub_newcoors_3[0, idx_3_4_type5, 0], sub_newcoors_3[1, idx_3_4_type5, 0]] = 1
        skel_doubles_diff_row = np.diff(skel_doubles, axis=1)
        skel_doubles_diff_col = np.diff(skel_doubles, axis=0)

        coors_no_doubles_row = np.transpose(np.nonzero(skel_doubles_diff_row == 0))
        coors_no_doubles_col = np.transpose(np.nonzero(skel_doubles_diff_col == 0))

        if len(coors_no_doubles_col) != 0:
            skel[coors_no_doubles_row[:, 0], coors_no_doubles_row[:, 1]] = False
            skel[coors_no_doubles_col[:, 0], coors_no_doubles_col[:, 1]] = False

        coors_double = np.concatenate((coors_no_doubles_row, coors_no_doubles_col), axis=0)
        include_col = ~np.isin(sub_sub_newcoors_3[:, 0], coors_double[:, 0])
        include_row = ~np.isin(sub_sub_newcoors_3[:, 1], coors_double[:, 1])
        idx_3_4_type5_nodouble = np.logical_and(include_col, include_row)
        coors_3_4_type5_nodouble = sub_sub_newcoors_3[idx_3_4_type5_nodouble, :]

        if len(coors_3_4_type5_nodouble) != 0:
            skel[coors_3_4_type5_nodouble[:, 0], coors_3_4_type5_nodouble[:, 1]] = False

    # ------------------------------------------------------------------------------ TO REMOVE tshape_4
    if np.sum(array_sum == 4) != 0:
        coors_point4 = np.transpose(np.nonzero(skel)).T
        array_check_4 = coors_point4[:, :, np.newaxis] + sortedCoors[:, np.newaxis, :].astype(int)  # shape (2, n, 8)

        array_logic_4 = np.zeros((sortedCoors.shape[1], coors_point4.shape[1]), dtype=int)
        array_idx_4 = np.arange(0, coors_point4.shape[1]).astype(int)  # create the logic array of shape (2, n)
        array_logic_4[:, array_idx_4] = skel[array_check_4[0, array_idx_4, :], array_check_4[1, array_idx_4, :]].T
        array_logic_4 = array_logic_4.astype(bool)
        array_sum_4 = np.sum(array_logic_4, axis=0)

        idx_points4 = np.where(array_sum_4 == 4)[0]

        if len(idx_points4) != 0:
            subarray_check4 = array_check_4[:, idx_points4, :]

            subarray_logic4 = array_logic_4[:, idx_points4].T
            subarray_logic4 = subarray_logic4[np.newaxis, :, :]
            subarray_logic4 = np.concatenate((subarray_logic4, subarray_logic4), axis=0)

            shrunk_subarray_check4 = subarray_check4[subarray_logic4].reshape(2, subarray_check4.shape[1], -1)
            sub_newcoors_4 = coors_point4[:, idx_points4, np.newaxis]

            array_distarray_4 = np.linalg.norm(sub_newcoors_4 - shrunk_subarray_check4, axis=0)
            distance_4 = np.around(np.sum(array_distarray_4, axis=1), decimals=1)

            idx_tshape_4 = distance_4 == 4.4

            if np.sum(idx_tshape_4) != 0:
                skel[sub_newcoors_4[0, idx_tshape_4, 0], sub_newcoors_4[1, idx_tshape_4, 0]] = False

    newcoors = np.transpose(np.nonzero(skel))

    return skel, newcoors


def skel_recons(skel, coors, debranch=False, remove=False):
    if debranch:
        edges, array_checkS, array_logic, array_newlogic = findedges(skel, coors)

        stilledges = len(edges) != 0
        while stilledges:
            skel[edges[:, 0], edges[:, 1]] = False
            edges = np.transpose(np.nonzero(skel))
            nextedges = findedges(skel, edges)[0]

            if len(nextedges) != 0:
                edges = nextedges
            else:
                stilledges = False

    newcoors = np.transpose(np.nonzero(skel))

    if remove:
        skel, newcoors = tshape_corners(skel, newcoors)

    return skel, newcoors


def labelobj(mask, skel, tol, eps=0.5, minsamp=20):
    negmask = np.ones_like(mask)
    negmask[skel] = 0
    floodmask = skmM.flood(skel, (1, 1), connectivity=1)  # to avoid labelling of external
    negmask[floodmask] = 0
    distmask = ndi.distance_transform_edt(negmask)
    logdistmask = distmask > tol
    coorobj = np.transpose(np.nonzero(logdistmask))
    k = slC.DBSCAN(eps=eps, min_samples=minsamp,
                   n_jobs=-2)  # it uses DBSCAN for clustering and find the only one TRUE node
    k.fit(coorobj)
    labels = (k.labels_ + 1).reshape(-1, 1)
    labelmask = np.full((skel.shape[0], skel.shape[0]), np.nan)
    labelmask[coorobj[:, 0], coorobj[:, 1]] = labels[:, 0]
    coorlabels = np.concatenate((coorobj, labels), axis=1)

    return labelmask, coorlabels


def objmorphology(maskskel, coorcyto, pixelsize):
    centroid = np.array([np.round(np.sum(coorcyto[:, 0]) / coorcyto.shape[0]).astype(int),
                         np.round(np.sum(coorcyto[:, 1]) / coorcyto.shape[0]).astype(int)]).reshape(-1, 2)[0]
    floodmask = skmM.flood(maskskel, (centroid[0], centroid[1]), connectivity=1)
    InTEigs = skM.inertia_tensor_eigvals(floodmask)  # Eigenvalues of the Inertia T.
    ecc = np.round(np.sqrt(1 - InTEigs[1] / InTEigs[0]), 2)  # Calculated from the Eigenvalues of the Inertia T.
    perim = np.around(skM.perimeter(floodmask) * pixelsize * 10 ** 6, decimals=1)  # perimeter in um
    area = np.around(np.sum(floodmask) * (pixelsize * 10 ** 6) ** 2, decimals=1)  # area in um^2

    return centroid, ecc, perim, area


def findnodes(skel, newcoors):
    squareBox1 = structure('square', (3, 3), hole=True)  # THIS IS TO REMOVE BRANCHES IN THE SKELETON
    sortedCoors = clockwisebox(squareBox1)  # these are the coor sorted clockwise
    newcoors = newcoors.T
    sortedCoors = sortedCoors.T
    array_logic = np.zeros((sortedCoors.shape[1], newcoors.shape[1]), dtype=int)
    array_checkS = newcoors[:, :, np.newaxis] + sortedCoors[:, np.newaxis, :].astype(int)  # shape (2, n, 8)

    array_idx = np.arange(0, newcoors.shape[1]).astype(int)  # create the logic array of shape (2, n)
    array_logic[:, array_idx] = skel[array_checkS[0, array_idx, :], array_checkS[1, array_idx, :]].T
    array_logic = array_logic.astype(bool)
    array_sum = np.sum(array_logic, axis=0)

    idx_points3 = np.where(array_sum == 3)[0]
    idx_points4 = np.where(array_sum == 4)[0]

    if len(idx_points3) != 0:
        subarray_check3 = array_checkS[:, idx_points3, :]

        subarray_logic3 = array_logic[:, idx_points3].T
        subarray_logic3 = subarray_logic3[np.newaxis, :, :]
        subarray_logic3 = np.concatenate((subarray_logic3, subarray_logic3), axis=0)

        shrunk_subarray_check3 = subarray_check3[subarray_logic3].reshape(2, subarray_check3.shape[1], -1)
        sub_newcoors_3 = newcoors[:, idx_points3, np.newaxis]

        extended_subarray_check3 = np.concatenate([shrunk_subarray_check3, shrunk_subarray_check3[:, :, 0, np.newaxis]],
                                                  axis=2)
        ext_subarray_check3diff = np.diff(extended_subarray_check3, axis=2)

        ext_subarray_check3diff_log = np.any(ext_subarray_check3diff == 0, axis=2)

        idx_type4 = np.sum(ext_subarray_check3diff_log, axis=0) == 2
        idx_type5 = np.sum(ext_subarray_check3diff_log, axis=0) == 1
        idx_type6 = np.sum(ext_subarray_check3diff_log, axis=0) == 0

        if len(idx_type4) != 0:
            sub_shrunk_check3_type4 = shrunk_subarray_check3[:, idx_type4, :]
            sub_necoors_3_type4 = sub_newcoors_3[:, idx_type4, :]

            array_distance_type4 = np.linalg.norm(sub_necoors_3_type4 - sub_shrunk_check3_type4, axis=0)
            distance_4 = np.around(np.sum(array_distance_type4, axis=1), decimals=1)
            idx_type4_4_2 = distance_4 == 4.2

            if len(idx_type4_4_2) != 0:
                nodes_type4_4_2 = sub_necoors_3_type4[:, idx_type4_4_2, 0].T
            else:
                nodes_type4_4_2 = np.full((1, 2), np.nan)
        else:
            nodes_type4_4_2 = np.full((1, 2), np.nan)

        if len(idx_type5) != 0:
            sub_shrunk_check3_type5 = shrunk_subarray_check3[:, idx_type5, :]
            sub_necoors_3_type5 = sub_newcoors_3[:, idx_type5, :]

            array_distance_type5 = np.linalg.norm(sub_necoors_3_type5 - sub_shrunk_check3_type5, axis=0)
            distance_5 = np.around(np.sum(array_distance_type5, axis=1), decimals=1)
            idx_type5_3_8 = distance_5 == 3.8

            arraybool_dist_1_4 = np.round(array_distance_type5, decimals=1) == 1.4
            arraybool_dist_1_4 = np.concatenate(
                (arraybool_dist_1_4[np.newaxis, :, :], arraybool_dist_1_4[np.newaxis, :, :]), axis=0)
            sub_shrunk_check3_type5_dist1_4 = sub_shrunk_check3_type5[arraybool_dist_1_4].reshape(2, -1, 2)

            ext_subarray_check3_type5_dist1_4 = np.concatenate([sub_shrunk_check3_type5_dist1_4,
                                                                sub_shrunk_check3_type5_dist1_4[:, :, 0, np.newaxis]],
                                                               axis=2)

            ext_check3_type5_dist1_4_diff = np.diff(ext_subarray_check3_type5_dist1_4, axis=2)
            ext_check3_type5_dist1_4_diff_log = np.any(ext_check3_type5_dist1_4_diff == 0, axis=2)
            idx_3_8_aligned = np.sum(ext_check3_type5_dist1_4_diff_log, axis=0) == 1

            idx_type5_3_8_aligned = np.logical_and(idx_type5_3_8, idx_3_8_aligned)

            if len(idx_type5_3_8_aligned) != 0:
                nodes_type5_3_8_aligned = sub_necoors_3_type5[:, idx_type5_3_8_aligned, 0].T
            else:
                nodes_type5_3_8_aligned = np.full((1, 2), np.nan)
        else:
            nodes_type5_3_8_aligned = np.full((1, 2), np.nan)

        if len(idx_type6) != 0:
            nodes_type6 = sub_newcoors_3[:, idx_type6, 0].T
        else:
            nodes_type6 = np.full((1, 2), np.nan)

        pre_nodes_point3 = np.concatenate((nodes_type4_4_2, nodes_type5_3_8_aligned, nodes_type6), axis=0)
    else:
        pre_nodes_point3 = np.full((1, 2), np.nan)

    if len(idx_points4) != 0:
        pre_nodes_point4 = newcoors[:, idx_points4].T
    else:
        pre_nodes_point4 = np.full((1, 2), np.nan)

    nodes = np.concatenate((pre_nodes_point3, pre_nodes_point4), axis=0)
    nodes = nodes[~np.isnan(nodes[:, 0]), :]

    return nodes


def indexing(skel):  # this is to order the coords progressively
    returnskel = np.zeros_like(skel, dtype=bool)
    returnskel[skel] = True
    squareBox = structure('square', (3, 3), hole=True)  # THIS IS TO ORDER THE COORD PROGRESSIVELY
    coor = np.transpose(np.nonzero(skel))
    start = np.argmin(coor[:, 0], axis=0)
    ORDcoors = np.zeros_like(coor)
    ORDcoors[0, :] = coor[start]
    i = 0
    while i < len(coor) - 1:
        check = squareBox + ORDcoors[i, :]
        idx = np.nonzero(skel[check[:, 0], check[:, 1]] == 1)
        if np.sum(skel[check[:, 0], check[:, 1]] == 1) == 1:
            skel[ORDcoors[i, 0], ORDcoors[i, 1]] = 0
            i += 1
            ORDcoors[i, :] = check[idx, :]
        else:
            points = check[idx, :][0]
            distance = np.linalg.norm(points - ORDcoors[i, :], axis=1)
            idxmin = np.argmin(distance)
            skel[ORDcoors[i, 0], ORDcoors[i, 1]] = 0
            i += 1
            ORDcoors[i, :] = points[idxmin, :]

    segs_length = np.array([np.sum(returnskel)])

    labels = np.ones((ORDcoors.shape[0], 1))
    ORDcoors = np.concatenate((ORDcoors, labels), axis=1)

    return ORDcoors.astype(int), coor[start], segs_length, returnskel


def indexing2(skel, truenodes):  # this is to order the coords progressively
    squareBox = structure('square', (3, 3), hole=True)  # THIS IS TO ORDER THE COORD PROGRESSIVELY
    truenodes = truenodes.astype(int)
    checknodes = skel[truenodes[:, 0], truenodes[:, 1]]
    falseidx = np.where(checknodes == False)[0]

    if falseidx:
        for i in falseidx:
            checknextnode = truenodes[i, :] + squareBox
            logicnext = skel[checknextnode[:, 0], checknextnode[:, 1]]
            idxfirstnextnode = np.where(logicnext == True)[0][0]
            truenodes[falseidx, :] = checknextnode[idxfirstnextnode, :]

    returnskel = np.zeros_like(skel, dtype=bool)
    returnskel[skel] = True
    copyskel = np.zeros_like(skel, dtype=bool)
    coor = np.transpose(np.nonzero(skel))
    copyskel = np.logical_or(copyskel, skel)

    centroid = np.array([np.round(np.sum(truenodes[:, 0]) / truenodes.shape[0]).astype(int),  # centroid
                         np.round(np.sum(truenodes[:, 1]) / truenodes.shape[0]).astype(int)]).reshape(-1, 2)

    shift = np.zeros_like(truenodes, dtype=int)  # these lines are to order the truenodes clockwise
    shift[:, 0] = truenodes[:, 0] - centroid[0, 0]
    shift[:, 1] = truenodes[:, 1] - centroid[0, 1]
    shiftoriented = clockwisebox(shift)
    oriented = np.zeros_like(shiftoriented)
    oriented[:, 0] = shiftoriented[:, 0] + centroid[0, 0]
    oriented[:, 1] = shiftoriented[:, 1] + centroid[0, 1]  # generated clockwise ordered list of nodes !!

    ORDcoors = np.zeros_like(coor)
    ORDcoors[0, :] = oriented[0, :]  # the starting point is the first node
    labels = np.zeros((len(coor), 1))
    i = 0
    seg_label = 0
    while i < len(coor) - 1:

        if np.sum(np.sum(np.equal(ORDcoors[i, :], oriented), axis=1) == 2) == 1:  # this means it is a node
            seg_label += 1

        labels[i] = seg_label

        check = squareBox + ORDcoors[i, :]
        idx = np.nonzero(copyskel[check[:, 0], check[:, 1]] == 1)
        if np.sum(copyskel[check[:, 0], check[:, 1]] == 1) == 1:
            copyskel[ORDcoors[i, 0], ORDcoors[i, 1]] = 0
            i += 1
            ORDcoors[i, :] = check[idx, :]

        else:
            points = check[idx, :][0]
            distance = np.linalg.norm(points - ORDcoors[i, :], axis=1)
            idxmin = np.argmin(distance)
            copyskel[ORDcoors[i, 0], ORDcoors[i, 1]] = 0
            i += 1
            ORDcoors[i, :] = points[idxmin, :]

    labels[-1] = seg_label  # this is for the last point
    labelordcoor = np.concatenate((ORDcoors, labels), axis=1)

    segs_length = np.zeros((len(np.unique(labelordcoor[:, 2]))))
    for j in range(0, len(np.unique(labelordcoor[:, 2]))):
        segs_length[j] = np.sum(labelordcoor[:, 2] == j + 1)

    return labelordcoor.astype(int), oriented[0, :], segs_length, returnskel


def segmentation(Recmask, n_debranch=1, tol0=1, debranch=False, remove=False):
    Recmask[:, 0:3] = 0
    Recmask[0:3, :] = 0
    Recmask[:, Recmask.shape[0] - 3:Recmask.shape[0]] = 0
    Recmask[Recmask.shape[0] - 3:Recmask.shape[0], :] = 0
    skelrecmask = skmM.skeletonize(Recmask)
    skelrecmaskcoor = np.transpose(np.nonzero(skelrecmask))

    step = 1
    while step <= n_debranch:
        skelrecmask, skelrecmaskcoor = skel_recons(skelrecmask, skelrecmaskcoor, debranch, remove)  # DE-BRANCHING
        step += 1
    labelmask, coorlabels = labelobj(Recmask, skelrecmask, tol=tol0, eps=3,
                                     minsamp=20)  # to create labelled objs, mask and labels
    # tol tells how much to retract from contours, eps and minsamp for DBSCAN

    return labelmask, coorlabels, skelrecmask


def boundingbox(coor):  # it creates a box with the obj at the center
    try:
        rowmin = np.min(coor[:, 0])
        rowmax = np.max(coor[:, 0])
        colmin = np.min(coor[:, 1])
        colmax = np.max(coor[:, 1])
        lrow = 2 * (rowmax - rowmin)
        lcol = 2 * (colmax - colmin)
        box = np.zeros((lrow, lcol), dtype='int')

        return box, lrow, lcol

    except:
        print('Adjust tolerance values')


def boundingbox_small(coor):  # it creates a box with the obj at the center
    try:
        rowmin = np.min(coor[:, 0])
        rowmax = np.max(coor[:, 0])
        colmin = np.min(coor[:, 1])
        colmax = np.max(coor[:, 1])
        lrow = int((rowmax - rowmin) + 0.2 * (rowmax - rowmin))  # 20% increase
        lcol = int((colmax - colmin) + 0.2 * (colmax - colmin))
        box = np.zeros((lrow, lcol), dtype='int')

        return box, lrow, lcol

    except:
        print('Adjust tolerance values')


def shiftcoor(coor, centroid, lrow, lcol):
    shiftcentroid = np.array([np.round(lrow / 2).astype(int), np.round(lcol / 2).astype(int)])
    newcoors = np.zeros_like(coor)
    deltarow = centroid[0] - shiftcentroid[0]
    deltacol = centroid[1] - shiftcentroid[1]
    newcoors[:, 0] = coor[:, 0] - deltarow
    newcoors[:, 1] = coor[:, 1] - deltacol

    return newcoors, shiftcentroid


def croppingmorpho(imageR, Recmask_mem, Recmask_cyto, skelrecmask, coorlabels, tol1, i, pixelsize, profile_cyto,
                   img_Pcoded, img_Pcoded_cyto):
    recon = np.zeros_like(Recmask_mem, dtype=bool)
    recon[coorlabels[coorlabels[:, 2] == i, 0], coorlabels[coorlabels[:, 2] == i, 1]] = True
    selem = skmM.disk(tol1)  # GET THE CROPPED SKEL OF INDIVIDUAL CELLS
    dilated = skmM.binary_dilation(recon, selem)

    croppedskel = np.logical_and(dilated, skelrecmask)
    croppedskelcoor = np.transpose(np.nonzero(croppedskel))
    centroid, ecc, perim, area = objmorphology(croppedskel, croppedskelcoor, pixelsize)
    dilated2 = skmM.binary_dilation(croppedskel, selem)

    croppedmask = np.logical_and(dilated2, Recmask_mem)
    croppedmaskcoor = np.transpose(np.nonzero(croppedmask))
    croppedcyto = np.zeros_like(Recmask_mem, dtype=bool)  # GET THE CROPPED CYTO MASK OF IND. CELLS
    croppedcyto[recon] = True
    croppedcyto[croppedmask] = False
    croppedcytocoor = np.transpose(np.nonzero(croppedcyto))

    if profile_cyto:
        croppedcytomasked = np.logical_and(croppedcyto,
                                           Recmask_cyto)  # GET THE MASKED CROPPED CYTO MASK OF IND. CELLS, masked based on cyto mask
    else:
        croppedcytomasked = np.logical_and(croppedcyto, Recmask_mem)
    croppedcytomaskedcorr = np.transpose(np.nonzero(croppedcytomasked))

    box, lrow, lcol = boundingbox(croppedmaskcoor)  # GENERATES BOXES
    newcoors_skel, shiftcentroid = shiftcoor(croppedskelcoor, centroid, lrow, lcol)
    newcoors_mask = shiftcoor(croppedmaskcoor, centroid, lrow, lcol)[0]
    newcoors_cyto = shiftcoor(croppedcytocoor, centroid, lrow, lcol)[0]
    newcoors_cytomasked = shiftcoor(croppedcytomaskedcorr, centroid, lrow, lcol)[0]

    cropped_Pcoded = np.full_like(box, np.nan, dtype=float)
    cropped_Pcoded_cyto = np.full_like(box, np.nan, dtype=float)
    cropped_Pcoded[newcoors_mask[:, 0], newcoors_mask[:, 1]] = img_Pcoded[croppedmaskcoor[:, 0], croppedmaskcoor[:, 1]]

    if np.any(~np.isnan(img_Pcoded_cyto)):
        cropped_Pcoded_cyto[newcoors_cytomasked[:, 0], newcoors_cytomasked[:, 1]] = img_Pcoded_cyto[
            croppedcytomaskedcorr[:, 0], croppedcytomaskedcorr[:, 1]]
    else:
        cropped_Pcoded_cyto = []

    newcropped_skel = np.zeros_like(box, dtype=bool)
    newcropped_skel[newcoors_skel[:, 0], newcoors_skel[:, 1]] = True
    rawcroppedmask = np.zeros((box.shape[0], box.shape[1], imageR.shape[2]))
    rawcroppedcyto = np.zeros((box.shape[0], box.shape[1], imageR.shape[2]))
    rawcroppedboth = np.zeros((box.shape[0], box.shape[1], imageR.shape[2]))

    rawcroppedmask[newcoors_mask[:, 0], newcoors_mask[:, 1], :] = imageR[croppedmaskcoor[:, 0], croppedmaskcoor[:, 1],
                                                                  :]
    rawcroppedcyto[newcoors_cyto[:, 0], newcoors_cyto[:, 1], :] = imageR[croppedcytocoor[:, 0], croppedcytocoor[:, 1],
                                                                  :]
    rawcroppedboth[newcoors_mask[:, 0], newcoors_mask[:, 1], :] = imageR[croppedmaskcoor[:, 0], croppedmaskcoor[:, 1],
                                                                  :]
    rawcroppedboth[newcoors_cyto[:, 0], newcoors_cyto[:, 1], :] = imageR[croppedcytocoor[:, 0], croppedcytocoor[:, 1],
                                                                  :]

    return newcoors_skel, newcoors_mask, newcoors_cyto, newcoors_cytomasked, newcropped_skel, \
           rawcroppedmask, rawcroppedcyto, rawcroppedboth, centroid, ecc, perim, area, shiftcentroid, \
           cropped_Pcoded, cropped_Pcoded_cyto


def findvaridx(Lambdachannel, varlist):
    numeric_values = [x for x in varlist if isinstance(x, (int, float))]

    if len(numeric_values) != 0:
        if len(Lambdachannel) == 1:
            varidxs = [0]
        else:
            varidxs = []
            for i in numeric_values:
                varidxs.append(np.where(Lambdachannel == i)[0][0])

        return varidxs

    else:
        print('Double check variables')


def lineprofile(shrunk_array, coors, num):
    shrunk_array_flip = np.flip(shrunk_array, axis=0)  # I feed point (y, x) but then I work with point (x, y)
    coors_flip = np.flip(coors, axis=0)
    min = np.floor(num / 2)
    max = np.ceil(num / 2)
    plus = np.arange(-min, max, 1)
    array_lines = np.zeros((2, coors.shape[1], len(plus)), dtype=int)

    idx_same_x = shrunk_array_flip[0, :, 0] == shrunk_array_flip[0, :, 1]
    array_samex_x = plus[:, np.newaxis] + coors_flip[np.newaxis, 0, idx_same_x]
    array_samex_y = np.tile(coors_flip[np.newaxis, 1, idx_same_x], (num, 1))
    array_lines[0, idx_same_x, :] = array_samex_x.T
    array_lines[1, idx_same_x, :] = array_samex_y.T

    idx_same_y = shrunk_array_flip[1, :, 0] == shrunk_array_flip[1, :, 1]
    array_samey_x = np.tile(coors_flip[np.newaxis, 0, idx_same_y], (num, 1))
    array_samey_y = plus[:, np.newaxis] + coors_flip[np.newaxis, 1, idx_same_y]
    array_lines[0, idx_same_y, :] = array_samey_x.T
    array_lines[1, idx_same_y, :] = array_samey_y.T

    idx_nosamexy = np.logical_not(np.logical_or(idx_same_x, idx_same_y))
    array_slopes = (shrunk_array_flip[0, idx_nosamexy, 1] - shrunk_array_flip[0, idx_nosamexy, 0]) / \
                   (shrunk_array_flip[1, idx_nosamexy, 1] - shrunk_array_flip[1, idx_nosamexy, 0])

    array_nosamexy_x = plus[:, np.newaxis] + coors_flip[np.newaxis, 0, idx_nosamexy]
    array_nosamexy_y = array_slopes[np.newaxis, :] * (array_nosamexy_x - coors_flip[np.newaxis, 0, idx_nosamexy]) + \
                       coors_flip[np.newaxis, 1, idx_nosamexy]
    array_lines[0, idx_nosamexy, :] = array_nosamexy_x.T
    array_lines[1, idx_nosamexy, :] = array_nosamexy_y.T

    array_lines = np.flip(array_lines, axis=0)

    return array_lines


def objprofiler(newcropped_skel, ordcoor, varidxs, pars, rawcroppedmask, autoff, pixeldepth, Thr_abovenoise,
                cropped_Pcoded, idx_col):
    global array_int_varD, filtered_array_int_varD, filtered_array_int_varC, array_int_varC, logic_both_col
    coors = ordcoor[:, :2].T

    if pars[0] == 'line':
        box = structure('square', (3, 3), hole=True).T
        array_screen = coors[:, :, np.newaxis] + box[:, np.newaxis, :].astype(int)

        array_idx = np.arange(0, coors.shape[1]).astype(int)  # create the logic array of shape (2, n)
        array_logic = np.zeros_like(array_screen, dtype=bool)
        array_logic[0, array_idx, :] = newcropped_skel[array_screen[0, array_idx, :], array_screen[1, array_idx, :]]
        array_logic[1, array_idx, :] = newcropped_skel[array_screen[0, array_idx, :], array_screen[1, array_idx, :]]
        shrunk_array_screen = array_screen[array_logic].reshape(2, len(array_idx), -1)
        array_integration = lineprofile(shrunk_array_screen, coors, pars[1][0])

    else:
        box = structure(pars[0], pars[1], hole=False).T
        array_integration = coors[:, :, np.newaxis] + box[:, np.newaxis, :].astype(int)

    array_idx = np.arange(0, coors.shape[1]).astype(int)  # create the logic array of shape (1, n)

    if len(varidxs) == 1:
        logic_abovenoise_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[0]] >= Thr_abovenoise[0])
        logic_notsat_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[0]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varA = np.logical_and(logic_abovenoise_varA, logic_notsat_varA)
        array_int_varA = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[0]])

        logic_allVar = logic_both_varA

        filtered_array_int_varA = np.zeros_like(array_int_varA, dtype=int)

    if len(varidxs) == 2:
        logic_abovenoise_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[0]] >= Thr_abovenoise[0])
        logic_notsat_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[0]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varA = np.logical_and(logic_abovenoise_varA, logic_notsat_varA)
        array_int_varA = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[0]])

        logic_abovenoise_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[1]] >= Thr_abovenoise[1])
        logic_notsat_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[1]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varB = np.logical_and(logic_abovenoise_varB, logic_notsat_varB)
        array_int_varB = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[1]])

        logic_allVar = np.logical_and(logic_both_varA, logic_both_varB)

        filtered_array_int_varA = np.zeros_like(array_int_varA, dtype=int)
        filtered_array_int_varB = np.zeros_like(array_int_varB, dtype=int)

    if len(varidxs) == 3:
        logic_abovenoise_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[0]] >= Thr_abovenoise[0])
        logic_notsat_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[0]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varA = np.logical_and(logic_abovenoise_varA, logic_notsat_varA)
        array_int_varA = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[0]])

        logic_abovenoise_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[1]] >= Thr_abovenoise[1])
        logic_notsat_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[1]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varB = np.logical_and(logic_abovenoise_varB, logic_notsat_varB)
        array_int_varB = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[1]])

        logic_allVar = np.logical_and(logic_both_varA, logic_both_varB)

        filtered_array_int_varA = np.zeros_like(array_int_varA, dtype=int)
        filtered_array_int_varB = np.zeros_like(array_int_varB, dtype=int)

        logic_abovenoise_varC = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varC = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varC[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[2]] >= Thr_abovenoise[2])
        logic_notsat_varC[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[2]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varC = np.logical_and(logic_abovenoise_varC, logic_notsat_varC)

        logic_allVar = np.logical_and(logic_allVar, logic_both_varC)

        array_int_varC = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[2]])
        filtered_array_int_varC = np.zeros_like(array_int_varC, dtype=int)

    if len(varidxs) == 4:
        logic_abovenoise_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varA = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[0]] >= Thr_abovenoise[0])
        logic_notsat_varA[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[0]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varA = np.logical_and(logic_abovenoise_varA, logic_notsat_varA)
        array_int_varA = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[0]])

        logic_abovenoise_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varB = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[1]] >= Thr_abovenoise[1])
        logic_notsat_varB[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[1]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varB = np.logical_and(logic_abovenoise_varB, logic_notsat_varB)
        array_int_varB = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[1]])

        logic_allVar = np.logical_and(logic_both_varA, logic_both_varB)

        filtered_array_int_varA = np.zeros_like(array_int_varA, dtype=int)
        filtered_array_int_varB = np.zeros_like(array_int_varB, dtype=int)

        logic_abovenoise_varC = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varC = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varC[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[2]] >= Thr_abovenoise[2])
        logic_notsat_varC[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[2]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varC = np.logical_and(logic_abovenoise_varC, logic_notsat_varC)

        logic_allVar = np.logical_and(logic_allVar, logic_both_varC)

        array_int_varC = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[2]])
        filtered_array_int_varC = np.zeros_like(array_int_varC, dtype=int)

        logic_abovenoise_varD = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_varD = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_varD[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                          array_integration[1, array_idx, :],
                                                                          varidxs[3]] >= Thr_abovenoise[3])
        logic_notsat_varD[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                      array_integration[1, array_idx, :], varidxs[
                                                                          3]] <
                                                       (2 ** pixeldepth - 1))
        logic_both_varD = np.logical_and(logic_abovenoise_varD, logic_notsat_varD)

        logic_allVar = np.logical_and(logic_allVar, logic_both_varD)

        array_int_varD = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           varidxs[3]])
        filtered_array_int_varD = np.zeros_like(array_int_varD, dtype=int)

    if ~np.isnan(idx_col[0]):
        logic_abovenoise_col = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_notsat_col = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=bool)
        logic_abovenoise_col[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                         array_integration[1, array_idx, :],
                                                                         idx_col] >= Thr_abovenoise[-1])
        logic_notsat_col[:, array_idx] = np.transpose(rawcroppedmask[array_integration[0, array_idx, :],
                                                                     array_integration[1, array_idx, :], idx_col] <
                                                      (2 ** pixeldepth - 1))

        logic_both_col = np.logical_and(logic_abovenoise_col, logic_notsat_col)

        array_int_col = np.transpose(
            rawcroppedmask[array_integration[0, array_idx, :], array_integration[1, array_idx, :],
                           idx_col])

        logic_allVar = np.logical_and(logic_allVar, logic_both_col)

        filtered_array_int_col = np.zeros((array_integration.shape[2], array_integration.shape[1]), dtype=int)

    if len(varidxs) == 1:
        filtered_array_int_varA[logic_allVar] = array_int_varA[logic_allVar]
        profiled_varA = np.sum(filtered_array_int_varA, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varA = profiled_varA[:, np.newaxis].astype(float)

        Intensities = profiled_varA

    if len(varidxs) == 2:
        filtered_array_int_varA[logic_allVar] = array_int_varA[logic_allVar]
        profiled_varA = np.sum(filtered_array_int_varA, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varA = profiled_varA[:, np.newaxis].astype(float)

        filtered_array_int_varB[logic_allVar] = array_int_varB[logic_allVar]
        profiled_varB = np.sum(filtered_array_int_varB, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varB = profiled_varB[:, np.newaxis].astype(float)

        Intensities = np.concatenate((profiled_varA, profiled_varB), axis=1)

    if len(varidxs) == 3:
        filtered_array_int_varA[logic_allVar] = array_int_varA[logic_allVar]
        profiled_varA = np.sum(filtered_array_int_varA, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varA = profiled_varA[:, np.newaxis].astype(float)

        filtered_array_int_varB[logic_allVar] = array_int_varB[logic_allVar]
        profiled_varB = np.sum(filtered_array_int_varB, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varB = profiled_varB[:, np.newaxis].astype(float)

        filtered_array_int_varC[logic_allVar] = array_int_varC[logic_allVar]
        profiled_varC = np.sum(filtered_array_int_varC, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varC = profiled_varC[:, np.newaxis].astype(float)

        Intensities = np.concatenate((profiled_varA, profiled_varB, profiled_varC), axis=1)

    if len(varidxs) == 4:
        filtered_array_int_varA[logic_allVar] = array_int_varA[logic_allVar]
        profiled_varA = np.sum(filtered_array_int_varA, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varA = profiled_varA[:, np.newaxis].astype(float)

        filtered_array_int_varB[logic_allVar] = array_int_varB[logic_allVar]
        profiled_varB = np.sum(filtered_array_int_varB, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varB = profiled_varB[:, np.newaxis].astype(float)

        filtered_array_int_varC[logic_allVar] = array_int_varC[logic_allVar]
        profiled_varC = np.sum(filtered_array_int_varC, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varC = profiled_varC[:, np.newaxis].astype(float)

        filtered_array_int_varD[logic_allVar] = array_int_varD[logic_allVar]
        profiled_varD = np.sum(filtered_array_int_varD, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_varD = profiled_varD[:, np.newaxis].astype(float)

        Intensities = np.concatenate((profiled_varA, profiled_varB, profiled_varC, profiled_varD), axis=1)

    array_Pvalue = np.transpose(cropped_Pcoded[array_integration[0, array_idx, :], array_integration[1, array_idx, :]])
    filtered_array_Pvalue = np.full_like(array_Pvalue, np.nan, dtype=float)
    filtered_array_Pvalue[logic_allVar] = array_Pvalue[logic_allVar]
    profiled_Pvalue = np.round(np.nansum(filtered_array_Pvalue, axis=0) / np.sum(logic_allVar, axis=0), decimals=2)
    profiled_Pvalue = profiled_Pvalue[:, np.newaxis].astype(float)

    Intensities_Pvalue = np.concatenate((array_idx[:, np.newaxis], Intensities, profiled_Pvalue), axis=1)
    Int_Pvalue_labels = np.concatenate((Intensities_Pvalue, ordcoor[:, 2, np.newaxis]), axis=1)

    if ~np.isnan(idx_col[0]):
        filtered_array_int_col[logic_allVar] = array_int_col[logic_allVar]
        profiled_col = np.sum(filtered_array_int_col, axis=0) / np.sum(logic_allVar, axis=0)
        profiled_col = profiled_col[:, np.newaxis].astype(float)

        Int_Pvalue_labels = np.concatenate((Int_Pvalue_labels, profiled_col), axis=1)

    if autoff:
        cutoff = np.round((np.max(profiled_Pvalue) - np.min(profiled_Pvalue)) / 2 + np.min(profiled_Pvalue), 2)
    else:
        cutoff = np.round(pars[2], 2)
    idxup = profiled_Pvalue > cutoff
    idxlow = profiled_Pvalue <= cutoff
    percentage_up = np.round(np.sum(idxup) / len(profiled_Pvalue) * 100, 1)

    if np.sum(idxlow) == 0:
        Pmedian_below = 'NaN'
    else:
        Pmedian_below = np.round(np.median(profiled_Pvalue[idxlow]), 2)

    if np.sum(idxup) == 0:
        Pmedian_above = 'NaN'
    else:
        Pmedian_above = np.round(np.median(profiled_Pvalue[idxup]), 2)

    if np.isnan(cutoff) or np.isinf(cutoff):
        cutoff = 'NaN'
        Pmedian_below = 'NaN'
        Pmedian_above = 'NaN'

    return Int_Pvalue_labels, Pmedian_below, Pmedian_above, cutoff, percentage_up


def objlinearization(rawcroppedboth, newcropped_skel, newcoors_mask, newcoors_cyto, radius, centroid):
    masktolinear = np.zeros_like(newcropped_skel, dtype=bool)
    masktolinear[newcoors_mask[:, 0], newcoors_mask[:, 1]] = True
    masktolinear[newcoors_cyto[:, 0], newcoors_cyto[:, 1]] = True
    masktolinear = skmM.remove_small_holes(masktolinear, area_threshold=3)  # to fill potential holes from the overlap

    if radius == 'auto' or radius > newcropped_skel.shape[1] - centroid[1] \
            or radius > newcropped_skel.shape[0] - centroid[0]:  # this is to calculate automatically how much to cut
        cent_to_maxx = newcropped_skel.shape[1] - centroid[1]
        cent_to_maxy = newcropped_skel.shape[0] - centroid[0]
        radius = min([centroid[0], centroid[1], cent_to_maxx, cent_to_maxy]) - 1  # 1 pixels far from edge

    cannyimg = skcanny.canny(masktolinear)  # detect the outer edge of cytosol
    skelouter = skmM.skeletonize(cannyimg)  # to remove overlapping point
    coorord = indexing(skelouter)[0]  # to index the pixels properly
    precors = np.linspace(0, radius, num=radius, dtype=int)

    corX3D = np.zeros((rawcroppedboth.shape[2], coorord.shape[0], len(precors)))
    corY3D = np.zeros((rawcroppedboth.shape[2], coorord.shape[0], len(precors)))
    Int3D = np.zeros((rawcroppedboth.shape[2], coorord.shape[0], len(precors)))
    for k in range(0, rawcroppedboth.shape[2]):
        totcorX = []
        totcorY = []
        totInt = []
        lengs = []
        for i in range(0, coorord.shape[0]):  # i keep the number of points constant in the integration (i.e. radius)
            a = np.array([centroid[1] + 1, centroid[0]])
            b = np.array([centroid[1], centroid[0]])
            c = np.array([coorord[i, 1], coorord[i, 0]])
            ba = a - b
            bc = c - b
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)  # calculate the angle to estimate x and Y

            if coorord[i, 1] >= centroid[1] and coorord[i, 0] < centroid[0]:  # first quad
                Xcors = centroid[1] + np.rint(precors * np.cos(angle)).astype(int)
                Ycors = centroid[0] - np.rint(precors * np.sin(angle)).astype(int)
            elif coorord[i, 1] >= centroid[1] and coorord[i, 0] >= centroid[0]:  # second quad
                Xcors = centroid[1] + np.rint(precors * np.cos(angle)).astype(int)
                Ycors = centroid[0] + np.rint(precors * np.sin(angle)).astype(int)
            elif coorord[i, 1] < centroid[1] and coorord[i, 0] >= centroid[0]:  # third quad
                Xcors = centroid[1] + np.rint(precors * np.cos(angle)).astype(int)
                Ycors = centroid[0] + np.rint(precors * np.sin(angle)).astype(int)
            else:
                Xcors = centroid[1] + np.rint(precors * np.cos(angle)).astype(int)
                Ycors = centroid[0] - np.rint(precors * np.sin(angle)).astype(int)

            lengs.append(len(Xcors))
            totcorX.append(Xcors)
            totcorY.append(Ycors)

            try:
                totInt.append(rawcroppedboth[Ycors, Xcors, k])

            except:
                raise Exception("Integration line out of image boundaries")

        corX3D[k, :, :] = np.asarray(totcorX)
        corY3D[k, :, :] = np.asarray(totcorY)
        Int3D[k, :, :] = np.asarray(totInt)

    return [corX3D, corY3D, Int3D]


def makemask(imageR, Lambdachannel, varlist, MaskParams, colocalization):
    varidxs = findvaridx(Lambdachannel, varlist)

    if colocalization != 'NaN':
        idx_col = np.where(Lambdachannel == colocalization)[0]
    else:
        idx_col = [np.nan]

    notnoisemask, Thr_abovenoise = abovenoise(imageR, varidxs, MaskParams['S_N'], MaskParams['stddev'],
                                              MaskParams['bgmean'], idx_col)

    combinedmask, satperc = nosaturated(imageR, notnoisemask, varidxs, MaskParams['PixelDepth'])  # > S/N + no sat

    IntSum = spectrum(imageR, combinedmask)

    if MaskParams['lambdaThr'] != 'NaN' and len(Lambdachannel) != 1:
        idxThr = np.where(Lambdachannel == MaskParams['lambdaThr'])[0][0]
    else:
        idxThr = 'NaN'

    Threshold, maskThr, slice_Thr, idx2 = thresholding(imageR, MaskParams['GaussianS'], varidxs,
                                                       MaskParams['PixelDepth'], combinedmask, idxThr,
                                                       MaskParams['Ttype'], value=MaskParams['ValManual'],
                                                       compression=MaskParams['compress'], k=MaskParams['Kvalue'])

    Recmask, Reccoors = maskprep(maskThr, objsize=MaskParams['objSize'], sizeholes=MaskParams['holesSize'],
                                 pixelsize=MaskParams['pxlSize'], dilation=MaskParams['dilate'],
                                 shape=MaskParams['shape'],
                                 d1=MaskParams['dim1'], d2=MaskParams['dim2'])  # MASK PREP

    Meta = [Lambdachannel, idx2, np.round(Threshold, 2), varidxs, [satperc, satperc]]  # META DATA

    return slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, len(Reccoors) != 0, varidxs, Thr_abovenoise
    # len(coor1) != 0  the last is to get index of empty imgs


def measuremask(imageR, Reccoors, Reccoors_cyto, Meta, varidxs, varidxs_cyto, text, histpars, ObjDetection, Recmask_mem,
                Recmask_cyto, n_debranch, tol0, tol1,
                Lambdachannel, profile_cyto, varlist_cyto, text_cyto, savecroppedmembrane, savecroppedcyto, savepath,
                profiler,
                Profpars, autoff, objlinear, radius, savelinearized, histpars_cyto, recenter, pixelsize, pixeldepth,
                Thr_abovenoise, dim_line, colocalization, savephasors):
    results_whole = basicmeasure(imageR, Reccoors, Meta, varidxs, text, histpars)

    if colocalization != 'NaN':
        idx_col = np.where(Lambdachannel == colocalization)[0]
    else:
        idx_col = [np.nan]

    if profile_cyto:
        results_whole_cyto = basicmeasure(imageR, Reccoors_cyto, Meta, varidxs_cyto, text_cyto, histpars_cyto)
        Pvalue_coded_cyto = results_whole_cyto[2]
    else:
        results_whole_cyto = []
        Pvalue_coded_cyto = []

    if ObjDetection:  # THIS IS FOR THE SINGLE OBJ DETECTION
        labelmask, coorlabels, skelrecmask = segmentation(Recmask_mem, n_debranch, tol0, debranch=True, remove=True)

        results_obj = {}
        for i in range(1, np.max(coorlabels[:, 2]) + 1):
            print('Object n{0}'.format(i))
            results_obj[i] = {'morphology': [], 'basicmembrane': [], 'basiccyto': [], 'profile': [],
                              'objlinearization': []}

            newcoors_skel, newcoors_mask, newcoors_cyto, newcoors_cytomasked, newcropped_skel, rawcroppedmask, \
            rawcroppedcyto, rawcroppedboth, centroid, ecc, perim, area, shiftcentroid, cropped_Pcoded, cropped_Pcoded_cyto = \
                croppingmorpho(imageR, Recmask_mem, Recmask_cyto, skelrecmask, coorlabels, tol1, i, pixelsize,
                               profile_cyto,
                               results_whole[2], Pvalue_coded_cyto)

            results_obj[i].update({'morphology': [labelmask, centroid, ecc, perim, area]})

            basicmembrane = basicmeasure(rawcroppedmask, newcoors_mask, Meta, varidxs, text, histpars)
            results_obj[i].update({'basicmembrane': basicmembrane})

            if profile_cyto:  # measurements on masked cytosol
                varidxs_cyto = findvaridx(Lambdachannel, varlist_cyto)
                basiccyto = basicmeasure(rawcroppedcyto, newcoors_cytomasked, Meta, varidxs_cyto, text_cyto,
                                         histpars_cyto)
                results_obj[i].update({'basiccyto': basiccyto})

            if savecroppedmembrane:
                directory_membrane = savepath + '/' + 'Cropped Membranes'
                if not os.path.exists(directory_membrane):
                    os.makedirs(directory_membrane)
                tfl.imsave(directory_membrane + '/' + 'Obj{0}.tiff'.format(i),
                           np.asarray(np.moveaxis(rawcroppedmask, -1, 0)))

            if savecroppedcyto:
                directory_cytosol = savepath + '/' + 'Cropped Cytosols'
                if not os.path.exists(directory_cytosol):
                    os.makedirs(directory_cytosol)
                tfl.imsave(directory_membrane + '/' + 'Obj{0}.tiff'.format(i),
                           np.asarray(np.moveaxis(rawcroppedcyto, -1, 0)))

            if profiler:  # THIS GENERATES THE ORDERED COORDINATES
                # try:
                if recenter:
                    newcropped_skel, newcoors_skel = skel_recons(newcropped_skel, newcoors_skel, debranch=True,
                                                                 remove=True)
                    newcropped_skel, newcoors_skel = recentering(newcropped_skel, newcoors_skel, shiftcentroid,
                                                                 rawcroppedboth,
                                                                 varidxs, dim_line, shape='octagon', dims=(7, 5))

                nodes = findnodes(newcropped_skel, newcoors_skel)  # to find the nodes

                newcropped_skel, newcoors_skel = skel_recons(newcropped_skel, newcoors_skel, debranch=True, remove=True)

                if len(nodes) == 0:  # this deal with non cluster
                    ordcoor, start, seg_lengths_pxl, newcropped_skel = indexing(newcropped_skel)

                else:
                    ordcoor, start, seg_lengths_pxl, newcropped_skel = indexing2(newcropped_skel,
                                                                                 nodes)  # returns ordered coors with labels and seg

                seglabelled_mask = np.zeros_like(newcropped_skel, dtype=int)
                seglabelled_mask[ordcoor[:, 0], ordcoor[:, 1]] = ordcoor[:, 2]

                INTs_GP, Pmedian_below, Pmedian_above, cutoff, percentage_up = objprofiler(newcropped_skel, ordcoor,
                                                                                           varidxs,
                                                                                           Profpars,
                                                                                           rawcroppedmask, autoff,
                                                                                           pixeldepth, Thr_abovenoise,
                                                                                           cropped_Pcoded, idx_col)

                results_obj[i].update(
                    {'profile': [INTs_GP, Pmedian_below, Pmedian_above, cutoff, percentage_up, seg_lengths_pxl,
                                 seglabelled_mask]})

                # except:
                #     results_obj[i].update({'profile': []})
                #     print('Membrane not profiled')

            if objlinear:
                try:
                    res = objlinearization(rawcroppedboth, newcropped_skel, newcoors_mask, newcoors_cyto, radius,
                                           shiftcentroid)
                    results_obj[i].update({'objlinearization': res})

                    if savelinearized:
                        directory_linear = savepath + '/' + 'Linearization'
                        if not os.path.exists(directory_linear):
                            os.makedirs(directory_linear)
                        imgIO.mimwrite(directory_linear + '/' + 'Obj{0}.tiff'.format(i), res[2])

                except:
                    results_obj[i].update({'objlinearization': []})
                    print('Object not linearized')
    else:
        results_obj = []

    results = {'results_whole': results_whole, 'results_whole_cyto': results_whole_cyto, 'results_obj': results_obj}

    frames = allframes(results, ObjDetection, profile_cyto, profiler, varidxs, idx_col,
                       savephasors)  # to generate data frame

    return results, frames


def allframes(results, ObjDetection, profile_cyto, profiler, varidxs, idx_col, savephasors):
    global df_morphology, df_summary, df_emiss, df_summarycyto, df_hist, df_emiss_cyto, \
        df_hist_cyto, df_profiler_medians, df_space1, df_space2, df_headcyto, df_space0, df_prof_allobjs, \
        i, list_df_summary_cyto, list_df_emission_cyto, list_df_hist_cyto, list_nobjs_cyto, df_bins_cyto, \
        df_headers_cyto, df_head_par_cyto, df_wavelengths_cyto, nan_to_append_sum, list_nan_summary, list_df_summary_prof, \
        list1, pd_nan_hspace, list_df_prof_obj, list_df_segments, list_headers_seg, df_space_sum_objs_prof, df_all_profile2, \
        df_space_objs_prof_seg, df_all_segments, nan_emiss, nan_hist, nan_summary_cyto

    df_0 = pd.DataFrame(['% Rejected pixels', 'P_median', 'P_sd', 'Norm. Int.'])
    df_1 = pd.DataFrame([results['results_whole'][0]['Parameters'][0], results['results_whole'][0]['Parameters'][1],
                         results['results_whole'][0]['Parameters'][2],
                         results['results_whole'][0]['Parameters'][3]])
    df_2 = pd.DataFrame(
        [results['results_whole'][0]['Wavelengths (nm)'], results['results_whole'][0]['Norm. Intensity']]).transpose()
    df_3 = pd.DataFrame([results['results_whole'][0]['Bin'], results['results_whole'][0]['Frequency (%)']]).transpose()
    df_4 = pd.concat([df_0, df_1, df_2, df_3], axis=1, ignore_index=True)
    df_4_headers = pd.DataFrame([np.nan, 'Summary', 'Wavelength (nm)', 'Intensity',
                                 'Bin histogram', 'Frequency (%)']).transpose()
    df_4 = pd.concat([df_4_headers, df_4], axis=0, ignore_index=True)

    df_empty_whole = pd.DataFrame(np.nan, index=range(2), columns=range(6))
    df_empty_whole.at[1, 0] = 'Whole analysis cysotol'

    if profile_cyto:
        df_1_cyto = pd.DataFrame(
            [results['results_whole_cyto'][0]['Parameters'][0], results['results_whole_cyto'][0]['Parameters'][1],
             results['results_whole_cyto'][0]['Parameters'][2],
             results['results_whole_cyto'][0]['Parameters'][3]])
        df_2_cyto = pd.DataFrame([results['results_whole_cyto'][0]['Wavelengths (nm)'],
                                  results['results_whole_cyto'][0]['Norm. Intensity']]).transpose()
        df_3_cyto = pd.DataFrame(
            [results['results_whole_cyto'][0]['Bin'], results['results_whole_cyto'][0]['Frequency (%)']]).transpose()
        df_4_cyto = pd.concat([df_0, df_1_cyto, df_2_cyto, df_3_cyto], axis=1, ignore_index=True)
        df_4_cyto = pd.concat([df_4_headers, df_4_cyto], axis=0, ignore_index=True)

        frames_whole = pd.concat([df_4, df_4_cyto], axis=0, ignore_index=True)

    else:
        frames_whole = df_4

    df_space_whole_sum_objs = pd.DataFrame([np.nan] * len(frames_whole))

    if ObjDetection:
        df_headers = pd.DataFrame(['Eccentricity', 'Perimeter', 'Area', '% Pixel rejected', 'P_median', 'P_stddev',
                                   'Norm. Pixel Intensity'], columns=['Parameters'])

        list_df_morphology = []
        list_df_summary = []
        list_df_emission = []
        list_df_hist = []
        list_nobjs = []
        list_hspace_nobjs = []

        df_head_par = pd.DataFrame(['Parameters'], columns=['Parameters'])
        df_wavelengths = pd.DataFrame(results['results_whole'][0]['Wavelengths (nm)'],
                                      columns=['Parameters'])
        df_bins = pd.DataFrame(results['results_whole'][0]['Bin'], columns=['Parameters'])
        df_hspace_onecell = pd.DataFrame([np.nan], columns=['Parameters'])
        df_header_emission = pd.DataFrame(['Wavelengths (nm)'], columns=['Parameters'])
        df_header_hist = pd.DataFrame(['Bin histogram'], columns=['Parameters'])

        if profile_cyto:
            df_head_par_cyto = pd.DataFrame(['Parameters cytosol'], columns=['Parameters'])
            df_headers_cyto = pd.DataFrame(['% Pixel rejected', 'P_median', 'P_stddev', 'Norm. Pixel Intensity'],
                                           columns=['Parameters'])

            df_wavelengths_cyto = pd.DataFrame(results['results_whole_cyto'][0]['Wavelengths (nm)'],
                                               columns=['Parameters'])

            df_bins_cyto = pd.DataFrame(results['results_whole_cyto'][0]['Bin'], columns=['Parameters'])

            nan_summary_cyto = nan_emiss = list(np.full((len(df_headers_cyto), 1), np.nan))
            nan_emiss = list(np.full((len(results['results_whole_cyto'][0]['Wavelengths (nm)']), 1), np.nan))
            nan_hist = list(np.full((len(results['results_whole_cyto'][0]['Bin']), 1), np.nan))

            list_df_summary_cyto = []
            list_df_emission_cyto = []
            list_df_hist_cyto = []
            list_nobjs_cyto = []

        if profiler:
            list_df_prof_obj = []
            list_nan_summary = np.full((3, len(varidxs)), np.nan)

            if ~np.isnan(idx_col[0]):
                pd_nan_hspace = pd.DataFrame([[np.nan] * (len(varidxs) + 4)])
            else:
                pd_nan_hspace = pd.DataFrame([[np.nan] * (len(varidxs) + 3)])

            list_df_segments = []
            list_headers_seg = []

        for i in list(results['results_obj'].keys()):

            list_df_morphology.append(pd.DataFrame(
                [results['results_obj'][i]['morphology'][2], results['results_obj'][i]['morphology'][3],
                 results['results_obj'][i]['morphology'][4]], columns=['Obj #{0}'.format(i)]))

            list_df_summary.append(pd.DataFrame([results['results_obj'][i]['basicmembrane'][0]['Parameters'][0],
                                                 results['results_obj'][i]['basicmembrane'][0]['Parameters'][1],
                                                 results['results_obj'][i]['basicmembrane'][0]['Parameters'][2],
                                                 results['results_obj'][i]['basicmembrane'][0]['Parameters'][3]],
                                                columns=['Obj #{0}'.format(i)]))

            list_df_emission.append(pd.DataFrame(results['results_obj'][i]['basicmembrane'][0]['Norm. Intensity'],
                                                 columns=['Obj #{0}'.format(i)]))

            list_df_hist.append(pd.DataFrame(results['results_obj'][i]['basicmembrane'][0]['Frequency (%)'],
                                             columns=['Obj #{0}'.format(i)]))

            list_nobjs.append(pd.DataFrame(['Obj #{0}'.format(i)], columns=['Obj #{0}'.format(i)]))

            list_hspace_nobjs.append(pd.DataFrame([np.nan], columns=['Obj #{0}'.format(i)]))

            if profile_cyto:
                if results['results_obj'][i]['basiccyto']:
                    list_df_summary_cyto.append(
                        pd.DataFrame([results['results_obj'][i]['basiccyto'][0]['Parameters'][0],
                                      results['results_obj'][i]['basiccyto'][0]['Parameters'][1],
                                      results['results_obj'][i]['basiccyto'][0]['Parameters'][2],
                                      results['results_obj'][i]['basiccyto'][0]['Parameters'][3]],
                                     columns=['Obj #{0}'.format(i)]))

                    list_df_emission_cyto.append(
                        pd.DataFrame(results['results_obj'][i]['basiccyto'][0]['Norm. Intensity'],
                                     columns=['Obj #{0}'.format(i)]))

                    list_df_hist_cyto.append(pd.DataFrame(results['results_obj'][i]['basiccyto'][0]['Frequency (%)'],
                                                          columns=['Obj #{0}'.format(i)]))

                else:
                    list_df_summary_cyto.append(pd.DataFrame(nan_summary_cyto, columns=['Obj #{0}'.format(i)]))

                    list_df_emission_cyto.append(pd.DataFrame(nan_emiss, columns=['Obj #{0}'.format(i)]))

                    list_df_hist_cyto.append(pd.DataFrame(nan_hist, columns=['Obj #{0}'.format(i)]))

            if profiler and results['results_obj'][i]['profile']:

                if len(varidxs) == 1:
                    list1 = ['Obj #{0}_DeltaX'.format(i), 'VarA', 'P median', 'Seg. labels']
                elif len(varidxs) == 2:
                    list1 = ['Obj #{0}_DeltaX'.format(i), 'VarA', 'VarB', 'P median', 'Seg. labels']
                elif len(varidxs) == 3:
                    list1 = ['Obj #{0}_DeltaX'.format(i), 'VarA', 'VarB', 'VarC', 'P median', 'Seg. labels']
                elif len(varidxs) == 4:
                    list1 = ['Obj #{0}_DeltaX'.format(i), 'VarA', 'VarB', 'VarC', 'VarD', 'P median', 'Seg. labels']

                list2 = ['Obj #{0}'.format(i)] * (len(varidxs) + 3)

                if ~np.isnan(idx_col[0]):
                    list1.append('Coloc. channel')
                    list2.append('Obj #{0}'.format(i))

                col_names = [x + y for x, y in zip(list1, list2)]

                pd_headers_profile = pd.DataFrame([list1], columns=col_names)

                pd_sum_prof = pd.DataFrame([['Pmedian_below', 'Pmedian_above', 'cutoff', '%_above'],
                                            [results['results_obj'][i]['profile'][1],
                                             results['results_obj'][i]['profile'][2],
                                             results['results_obj'][i]['profile'][3],
                                             results['results_obj'][i]['profile'][4]]])

                pd_nan_sum = pd.DataFrame(list_nan_summary).T
                combined_pds = pd.concat([pd_sum_prof, pd_nan_sum], axis=0, ignore_index=True).T
                combined_pds_space = pd.concat([combined_pds, pd_nan_hspace], axis=0)
                combined_pds_space.columns = col_names

                df_traj_prof = pd.DataFrame(results['results_obj'][i]['profile'][0].tolist(), columns=col_names)

                df_full_prof_obj = pd.concat([combined_pds_space, pd_headers_profile, df_traj_prof], axis=0,
                                             ignore_index=True)

                list_df_prof_obj.append(df_full_prof_obj)

                list_headers_seg.append(pd.DataFrame(['Segments_obj #{0}'.format(i)]))
                list_df_segments.append(pd.DataFrame(results['results_obj'][i]['profile'][5].tolist(), columns=[i - 1]))

        df_morphology2 = pd.concat(list_df_morphology, axis=1)
        df_summary2 = pd.concat(list_df_summary, axis=1)
        df_emission2 = pd.concat(list_df_emission, axis=1)
        df_hist2 = pd.concat(list_df_hist, axis=1)
        df_hspace_nobjs = pd.concat(list_hspace_nobjs, axis=1)
        df_headers_objs = pd.concat(list_nobjs, axis=1)

        df_summary_data = pd.concat([df_headers_objs, df_morphology2, df_summary2, df_hspace_nobjs, df_headers_objs,
                                     df_emission2, df_hspace_nobjs, df_headers_objs, df_hist2], ignore_index=True)

        df_summary_parameters = pd.concat([df_head_par, df_headers, df_hspace_onecell, df_header_emission,
                                           df_wavelengths, df_hspace_onecell, df_header_hist, df_bins], axis=0,
                                          ignore_index=True)

        df_summary = pd.concat([df_summary_parameters, df_summary_data], axis=1, ignore_index=True)

        if profile_cyto:
            df_summary_cyto2 = pd.concat(list_df_summary_cyto, axis=1)
            df_emission_cyto2 = pd.concat(list_df_emission_cyto, axis=1)
            df_hist_cyto2 = pd.concat(list_df_hist_cyto, axis=1)

            df_summary_data = pd.concat(
                [df_summary_data, df_hspace_nobjs, df_headers_objs, df_summary_cyto2, df_hspace_nobjs,
                 df_headers_objs, df_emission_cyto2, df_hspace_nobjs, df_headers_objs, df_hist_cyto2],
                ignore_index=True)

            df_summary_parameters = pd.concat(
                [df_summary_parameters, df_hspace_onecell, df_head_par_cyto, df_headers_cyto,
                 df_hspace_onecell, df_header_emission, df_wavelengths_cyto, df_hspace_onecell,
                 df_header_hist, df_bins_cyto], axis=0, ignore_index=True)

            df_summary = pd.concat([df_summary_parameters, df_summary_data], axis=1, ignore_index=True)

        else:
            df_summary = pd.concat([df_summary_parameters, df_summary_data], axis=1, ignore_index=True)

        df_space_sum_objs_prof = pd.DataFrame([np.nan] * len(df_summary))

        if profiler:
            df_all_profile2 = pd.concat(list_df_prof_obj, axis=1)
            df_space_objs_prof_seg = pd.DataFrame([np.nan] * len(df_all_profile2))

            df_allheaders_segm = pd.concat(list_headers_seg, axis=1).T
            df_allheaders_segm = pd.concat([pd.DataFrame([np.nan]), df_allheaders_segm], axis=0, ignore_index=True)

            df_all_segments = pd.concat(list_df_segments, axis=1).T

            df_ith_seg = pd.DataFrame([['length_{0} (pixels)'.format(x) for x in range(df_all_segments.shape[1])]])

            df_all_segments = pd.concat([df_ith_seg, df_all_segments], axis=0, ignore_index=True)
            df_all_segments = pd.concat([df_allheaders_segm, df_all_segments], axis=1, ignore_index=True)

    if ObjDetection:
        if profile_cyto:
            if profiler:
                final_frame = pd.concat([frames_whole, df_space_whole_sum_objs, df_summary, df_space_sum_objs_prof,
                                         df_all_profile2, df_space_objs_prof_seg, df_all_segments], axis=1,
                                        ignore_index=True)
            else:
                final_frame = pd.concat([frames_whole, df_space_whole_sum_objs, df_summary], axis=1, ignore_index=True)
        else:
            if profiler:
                final_frame = pd.concat([frames_whole, df_space_whole_sum_objs, df_summary, df_space_sum_objs_prof,
                                         df_all_profile2, df_space_objs_prof_seg, df_all_segments], axis=1,
                                        ignore_index=True)
            else:
                final_frame = pd.concat([frames_whole, df_space_whole_sum_objs, df_summary], axis=1, ignore_index=True)

    else:
        final_frame = frames_whole

    if savephasors:
        df_headers_phas = pd.DataFrame(['Phasor_x', 'Phasor_y']).T
        df_phasors_mem = pd.DataFrame(results['results_whole'][1])
        df_heads_phas_mem = pd.concat([df_headers_phas, df_phasors_mem], axis=0, ignore_index=True)
        df_nan_vspace_phas = pd.DataFrame([[np.nan] * df_heads_phas_mem.shape[0]]).T

        if profile_cyto:
            df_headers_phas_cyto = pd.DataFrame(['Phasor_x_cyto', 'Phasor_y_cyto']).T
            df_phasors_cyto = pd.DataFrame(results['results_whole_cyto'][1])
            df_heads_phas_cyto = pd.concat([df_headers_phas_cyto, df_phasors_cyto], axis=0, ignore_index=True)

            df_all_phasors = pd.concat([df_nan_vspace_phas, df_heads_phas_mem, df_nan_vspace_phas, df_heads_phas_cyto],
                                       axis=1, ignore_index=True)
        else:
            df_all_phasors = pd.concat([df_nan_vspace_phas, df_heads_phas_mem], axis=1, ignore_index=True)

        final_frame = pd.concat([final_frame, df_all_phasors], axis=1, ignore_index=True)

    final_frame.replace(np.nan, '')

    return final_frame


def exportframes(filename, savingpath, frames, dims):
    excelname = savingpath + '/' + filename.split('.')[0] + '.xlsx'
    try:
        if sum(np.array(dims) > 1) == 2 or sum(np.array(dims) > 1) == 3:
            frames.to_excel(excelname, sheet_name='Global', index=False, header=False, index_label=False)

        elif sum(np.array(dims) > 1) == 4:
            with pd.ExcelWriter(excelname, engine='xlsxwriter') as writer:
                for z in frames.keys():
                    frames[z].to_excel(writer, sheet_name='slice_{0}'.format(z),
                                       index=False, header=False, index_label=False)

        elif sum(np.array(dims) > 1) == 5:
            with pd.ExcelWriter(excelname, engine='xlsxwriter') as writer:
                for t in frames.keys():
                    for z in frames[t].keys():
                        frames[t][z].to_excel(writer, sheet_name='slice_t{0}_z{1}'.format(t, z),
                                              index=False, header=False, index_label=False)
    except:
        print('Nothing to save')


def recentering(newcropped_skel, newcoors_skel, shiftcentroid, rawcroppedboth, varidxs, dim_line, shape='octagon',
                dims=(7, 5)):
    prebox, prelrow, prelcol = boundingbox_small(newcoors_skel)
    precoor = np.transpose(np.nonzero(prebox == 0))
    coor_row = precoor[:, 0] + (shiftcentroid[0] - int(prebox.shape[0] / 2))
    coor_col = precoor[:, 1] + (shiftcentroid[1] - int(prebox.shape[1] / 2))

    mask_raw = np.zeros_like(rawcroppedboth[:, :, 1])
    slice_int = []
    for i in varidxs:
        slice_int.append(np.sum(rawcroppedboth[coor_row, coor_col, i]))
    slice_int = np.asarray(slice_int)
    idx_max = np.argmax(slice_int)
    mask_raw[coor_row, coor_col] = rawcroppedboth[coor_row, coor_col, varidxs[idx_max]]
    octagonBox = structure(shape, (dims[0], dims[1]), hole=False)
    new_skel = np.zeros_like(mask_raw, dtype=bool)

    box = structure('square', (3, 3), hole=True).T
    newcoors_skel = newcoors_skel.T
    array_screen = newcoors_skel[:, :, np.newaxis] + box[:, np.newaxis, :].astype(int)

    array_idx = np.arange(0, newcoors_skel.shape[1]).astype(int)  # create the logic array of shape (2, n)
    array_logic = np.zeros_like(array_screen, dtype=bool)
    array_logic[0, array_idx, :] = newcropped_skel[array_screen[0, array_idx, :], array_screen[1, array_idx, :]]
    array_logic[1, array_idx, :] = newcropped_skel[array_screen[0, array_idx, :], array_screen[1, array_idx, :]]

    shrunk_array_screen = array_screen[array_logic].reshape(2, len(array_idx), -1)

    array_lines = lineprofile(shrunk_array_screen, newcoors_skel, dim_line)

    idx_int = np.arange(0, newcoors_skel.shape[1]).astype(int)
    array_ints = np.zeros((array_lines.shape[2], array_lines.shape[1]), dtype=int)
    array_ints[:, idx_int] = mask_raw[array_lines[0, idx_int, :], array_lines[1, idx_int, :]].T
    idx_intmax = np.argmax(array_ints, axis=0)
    array_point_maxint = array_lines[np.arange(array_lines.shape[0])[:, np.newaxis], np.arange(array_lines.shape[1]),
                                     idx_intmax[np.newaxis, :]]

    octagonBox = octagonBox.T
    array_shifcoors = array_point_maxint[:, :, np.newaxis] + octagonBox[:, np.newaxis, :]
    new_skel[array_shifcoors[0, :, :], array_shifcoors[1, :, :]] = True

    new_skel = skmM.remove_small_holes(new_skel, area_threshold=5)

    newskel = skmM.skeletonize(new_skel)
    newcoor = np.transpose(np.nonzero(newskel))

    return newskel, newcoor
