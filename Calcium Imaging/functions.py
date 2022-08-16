
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
from scipy.signal import find_peaks, peak_prominences
import pywt

def read_video(directory):
    cap = cv2.VideoCapture(directory)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_list = []
    for i in range(frame_count):
        ret, frame = cap.read()
        video_list.append(frame[:,:,0])
    video = np.array(video_list)
    return video

def remove_small_rois(labels, threshold):
    unique, counts = np.unique(labels, return_counts=True)
    thresholded = unique[counts>threshold][1:]
    filtered = np.isin(labels, thresholded)
    return labels*filtered

def get_traces(video, labels):
    rois = pd.DataFrame()
    for i in np.unique(labels):
        if i > 0:
            trace = video[:,labels==i].mean(axis=1)
            rois['roi_'+str(i)] = trace
    return rois

def deltanorm(cells):
    labels = cells.columns.values.tolist()  
    F0 = cells.iloc[0:10,:].describe().iloc[1,:].values
    DeltaF = cells.values - F0
    norm = DeltaF/F0
    cells = pd.DataFrame(norm, columns = labels)
    return cells

def wavelet_transform(signal, wavelet="coif3"):

    ca5, cd5, cd4, cd3, cd2, cd1 = pywt.wavedec(signal, wavelet, level=5)

    def thresh(x):
        # calculate thresh:
        #threshold = np.sqrt(2*np.log(len(x)) * np.std(x)) /np.sqrt(np.log(len(x)))
        # https://www.hindawi.com/journals/mpe/2016/3195492/
        threshold = np.std(x) * np.sqrt(2*np.log(len(x)))
        return pywt.threshold(x, threshold)

    cd5 = thresh(cd5)
    cd4 = thresh(cd4)*0
    cd3 = thresh(cd3)*0
    cd2 = thresh(cd2)*0
    cd1 = thresh(cd1)*0

    return pywt.waverec([ca5, cd5, cd4, cd3, cd2, cd1], wavelet)