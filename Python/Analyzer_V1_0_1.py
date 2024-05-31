# -*- coding: utf-8 -*-

from Packages import np
import AllFunctions as F



def GP_Analyser(mode, filename, Lambdachannel, image, dims, varlist, ObjectDetection, profiler,
                profilershape, autoff, PDiamCutoff, proDim1, proDim2, text, histpars, histpars_cyto,
                text_cyto, profile_cyto, varlist_cyto, n_debranch, tol0, tol1, savecroppedmembrane, savecroppedcyto,
                savelinearized, savepath, objlinear, recentering, dim_line, MaskParams_mem, MaskParams_cyto,
                colocalization, savephasors, radius):

    Profpars = [profilershape, (proDim1, proDim2), PDiamCutoff]
    if sum(np.array(dims) > 1) == 3 or sum(np.array(dims) > 1) == 2:
        if mode == 0:
            Dict = {'datamask': []}
            imageR = image

            slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem, colocalization)

            if profile_cyto:
                _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                    F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto, colocalization)
                Recmask_cyto[Recmask] = False

            else:
                Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

            Dict.update(
                {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Recmask_cyto]})
            return Dict

        else:
            Dict = {'datamask': [], 'analysis': []}
            imageR = image

            slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem, colocalization)

            if profile_cyto:
                _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                    F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto, colocalization)
                Recmask_cyto[Recmask] = False
                Reccoors_cyto = np.transpose(np.nonzero(Recmask_cyto))

            else:
                Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

            Dict.update(
                {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Recmask_cyto]})

            if np.sum(Recmask_cyto) == 0:
                profile_cyto = False

            if notempty:
                Results, frames = F.measuremask(imageR, Reccoors, Reccoors_cyto, Meta, varidxs, varidxs_cyto, text,
                                                histpars, ObjectDetection, Recmask,
                                                Recmask_cyto, n_debranch, tol0, tol1, Lambdachannel, profile_cyto,
                                                varlist_cyto, text_cyto, savecroppedmembrane,
                                                savecroppedcyto, savepath, profiler, Profpars, autoff, objlinear, radius,
                                                savelinearized, histpars_cyto, recentering, MaskParams_mem['pxlSize'],
                                                MaskParams_mem['PixelDepth'], Thr_abovenoise, dim_line, colocalization,
                                                savephasors)

                F.exportframes(filename, savepath, frames, dims)

            else:
                print('Image is empty')
                Results = []

            Dict.update({'analysis': Results})

        return Dict

    elif sum(np.array(dims) > 1) == 4:
        if mode == 0:
            preDict_z = {z: [] for z in range(image.shape[0])}
            for z in range(0, image.shape[0]):
                Dict = {'datamask': []}
                imageR = image[z, :, :, :]

                slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                    F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem[z], colocalization)

                if profile_cyto:
                    _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                        F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto[z], colocalization)
                    Recmask_cyto[Recmask] = False

                else:
                    Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

                Dict.update(
                    {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs,
                                  Recmask_cyto]})
                preDict_z[z] = Dict

            return preDict_z

        else:
            preDict_z = {z: [] for z in range(image.shape[0])}
            frames_z = {z: [] for z in range(image.shape[0])}
            for z in range(0, image.shape[0]):
                print('Analyzing slice n{0}'.format(z + 1))
                Dict = {'datamask': [], 'analysis': []}
                imageR = image[z, :, :, :]

                slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                    F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem[z], colocalization)

                if profile_cyto:
                    _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                        F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto[z], colocalization)
                    Recmask_cyto[Recmask] = False
                    Reccoors_cyto = np.transpose(np.nonzero(Recmask_cyto))

                else:
                    Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

                Dict.update(
                    {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Recmask_cyto]})

                if np.sum(Recmask_cyto) == 0:
                    profile_cyto = False

                if notempty:
                    Results, frames_z[z] = F.measuremask(imageR, Reccoors, Reccoors_cyto, Meta, varidxs, varidxs_cyto, text,
                                                    histpars, ObjectDetection, Recmask,
                                                    Recmask_cyto, n_debranch, tol0, tol1, Lambdachannel, profile_cyto,
                                                    varlist_cyto, text_cyto, savecroppedmembrane,
                                                    savecroppedcyto, savepath, profiler, Profpars, autoff, objlinear,
                                                    radius,
                                                    savelinearized, histpars_cyto, recentering, MaskParams_mem[z]['pxlSize'],
                                                    MaskParams_mem[z]['PixelDepth'], Thr_abovenoise, dim_line, colocalization,
                                                         savephasors)

                else:
                    print('Image is empty')
                    Results = []

                Dict.update({'analysis': Results})

                preDict_z[z] = Dict

            F.exportframes(filename, savepath, frames_z, dims)

            return preDict_z

    elif sum(np.array(dims) > 1) == 5:      # T or Z are always the first dimension
        if mode == 0:
            preDict_zt = {t: {z: [] for z in range(image.shape[1])} for t in range(image.shape[0])}
            for t in range(0, image.shape[0]):
                for z in range(0, image.shape[1]):
                    Dict = {'datamask': []}
                    imageR = image[t, z, :, :, :]

                    slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                        F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem[t][z], colocalization)

                    if profile_cyto:
                        _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                            F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto[t][z], colocalization)
                        Recmask_cyto[Recmask] = False

                    else:
                        Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

                    Dict.update(
                        {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs,
                                      Recmask_cyto]})
                    preDict_zt[t][z] = Dict

            return preDict_zt

        else:
            preDict_zt = {t: {z: [] for z in range(image.shape[1])} for t in range(image.shape[0])}
            frames_zt = {t: {z: [] for z in range(image.shape[1])} for t in range(image.shape[0])}
            for t in range(0, image.shape[0]):
                for z in range(0, image.shape[1]):
                    print('Analyzing slice t{0}z{1}'.format(t + 1, z + 1))
                    Dict = {'datamask': [], 'analysis': []}
                    imageR = image[t, z, :, :, :]

                    slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs, Thr_abovenoise = \
                        F.makemask(imageR, Lambdachannel, varlist, MaskParams_mem[t][z], colocalization)

                    if profile_cyto:
                        _, _, Recmask_cyto, _, Meta_cyto, _, _, varidxs_cyto, *_ = \
                            F.makemask(imageR, Lambdachannel, varlist_cyto, MaskParams_cyto[t][z], colocalization)
                        Recmask_cyto[Recmask] = False
                        Reccoors_cyto = np.transpose(np.nonzero(Recmask_cyto))

                    else:
                        Recmask_cyto, Meta_cyto, Reccoors_cyto, varidxs_cyto = [], [], [], []

                    Dict.update(
                        {'datamask': [slice_Thr, Threshold, Recmask, IntSum, Meta, Reccoors, notempty, varidxs,
                                      Recmask_cyto]})

                    if np.sum(Recmask_cyto) == 0:
                        profile_cyto = False

                    if notempty:
                        Results, frames_zt[t][z] = F.measuremask(imageR, Reccoors, Reccoors_cyto, Meta, varidxs, varidxs_cyto, text,
                                                        histpars, ObjectDetection, Recmask,
                                                        Recmask_cyto, n_debranch, tol0, tol1, Lambdachannel, profile_cyto,
                                                        varlist_cyto, text_cyto, savecroppedmembrane,
                                                        savecroppedcyto, savepath, profiler, Profpars, autoff, objlinear,
                                                        radius,
                                                        savelinearized, histpars_cyto, recentering,
                                                        MaskParams_mem[t][z]['pxlSize'],
                                                        MaskParams_mem[t][z]['PixelDepth'], Thr_abovenoise, dim_line,
                                                                 colocalization, savephasors)
                    else:
                        print('Image is empty')
                        Results = []

                    Dict.update({'analysis': Results})

                    preDict_zt[t][z] = Dict

            F.exportframes(filename, savepath, frames_zt, dims)

            return preDict_zt