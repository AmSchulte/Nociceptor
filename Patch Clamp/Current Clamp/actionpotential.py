from sweep import Sweep
import numpy as np
from scipy import signal


class AP(Sweep):
    def __init__(self, directory=None, names=['index','time','V-mon','stimulus','time2','I-mon','stimulus2']):
        super().__init__(directory, names)
        

        self.firing_start = []
        self.firing_threshold = []
        self.ap_threshold = 0
        self.voltage_filtered = None
        self.voltage_derivative = None

        #are calculated with get_ap_properties
        self.relative_stimulus = None
        self.no_ap = []
        self.true_ap = []
        self.amplitude_max = None
        self.spike_width_0mV = None
        self.spike_width = None

        self.amplitude_min = None

        #to do
        self.repolarization_time = None
        self.hyperpolarization_time = None
    

        self.get_ap_properties()


        
    def get_ap_properties(self):
        cutOff = 2000 #cutoff frequency, Hz
        fs = 25000 #sampling frequency, Hz
        order = 4 #order of filter
        self.voltage_filtered = self.butter_lowpass_filter(self.voltage, cutOff, fs, order)
        self.voltage_derivative = np.diff(self.voltage_filtered)/np.diff(self.time)  ## mV/s

        for voltage, voltage_derivative, stimulus in zip(self.voltage, self.voltage_derivative, self.stimulus):
            start, thresh = self.get_firing_threshold(voltage, voltage_derivative, stimulus)
            self.firing_start.append(start)
            self.firing_threshold.append(thresh)


        maxi = np.max(self.voltage, axis=1)
        self.amplitude_max = maxi
        self.amplitude_argmax = np.argmax(self.voltage, axis=1)
        self.no_ap = np.isnan(self.firing_start)
        self.true_ap = ~self.no_ap
        self.amplitude_max[self.no_ap] = np.nan
        
        self.amplitude_argmax[self.no_ap] = -1

        self.amplitude_min = np.min(self.voltage, axis=1)
        self.amplitude_min[self.no_ap] = np.nan

        self.get_relative_stimulus()

        self.spike_width_0mV = self.get_width(0)
        self.spike_width = self.get_width(-20)
        

    def bessel_lowpass_filter(self, data, cutOff, fs, order=4):
        nyq = 0.5 * fs
        normalCutoff = cutOff / nyq
        par = signal.bessel(order, normalCutoff, btype='low', output="sos")
        y = signal.sosfiltfilt(par, data)
        return y
    
    def butter_lowpass_filter(self, data, cutOff, fs, order=4):
        nyq = 0.5 * fs
        normalCutoff = cutOff / nyq
        par = signal.butter(order, normalCutoff, btype='low', output="sos")
        y = signal.sosfiltfilt(par, data)
        return y
    
    def get_firing_threshold(self, voltage, voltage_derivative, stimulus):
        
        max_x = np.argmax(voltage_derivative)
        max_y = np.max(voltage_derivative)
        #if signal is AP
        if np.max(voltage) > self.ap_threshold:
            start_stim = np.where(stimulus!=stimulus[0])[0][0]+10
            if (max_x-start_stim) > 0:
                min_x = np.argmin(voltage_derivative[start_stim:max_x])+start_stim
                min_y = voltage_derivative[min_x]
                dy_thresh = 0.03*(max_y-min_y)+min_y
                firing_xstart = (np.where(voltage_derivative[min_x:max_x]>=dy_thresh)+min_x)[0][0]
                # voltage at which dV/dt reached the level of 0.03 × (dV/dtmax − dV/dtmin) + dV/dtmin
                firing_threshold = voltage[firing_xstart]
            else:
                firing_xstart = np.nan
                firing_threshold = np.nan
        else: 
            firing_xstart = np.nan
            firing_threshold = np.nan
        return firing_xstart, firing_threshold

    def get_relative_stimulus(self):
        # current stimuli in pA
        stim = self.stimulus-self.stimulus[0]
        self.relative_stimulus = np.rint(np.max(stim, axis=1)*10**12)

    def find_nearest(self, array,value):
        idx = (np.abs(array-value)).argmin()
        return idx

    def get_width(self, voltage_level):
        # returns spike witdth at voltage level in milliseconds
        width = []
        for i in range(len(self.relative_stimulus)):
            if self.amplitude_argmax[i] == -1:
                time = np.nan
            else:
                start = self.find_nearest(self.voltage[i][0:self.amplitude_argmax[i]],voltage_level)
                end = self.find_nearest(self.voltage[i][self.amplitude_argmax[i]::],voltage_level) + self.amplitude_argmax[i]
                difference = end-start
                time = self.time[0][difference]
            width.append(time*1000)

        return width
