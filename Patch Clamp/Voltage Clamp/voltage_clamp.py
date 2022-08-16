from sweep import Sweep
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from scipy import signal

class IV(Sweep):
    def __init__(self, directory=None, names=['index','time','I-mon','stimulus','time2', 'V-mon', 'stimulus2', 'time3', 'leak','stimulus3']):
        super().__init__(directory, names)
        self.get_iv_properties()

    def get_iv_properties(self):
        hold = self.stimulus[0][0]
        self.iv_voltage = np.unique(self.stimulus)[1::]*1000
        self.iv_range = np.where(self.stimulus[10] != hold)[0][10:-10]

        cutOff = 3000 #cutoff frequency, Hz
        fs = 25000 #sampling frequency, Hz
        order = 4 #order of filter
        self.current_filtered = self.butter_lowpass_filter(self.current, cutOff, fs, order)
        
        self.iv_current = []
        for trace in self.current_filtered:
            self.iv_current.append(np.min(trace[self.iv_range]))

        
    def plot_iv(self):
        plt.figure(figsize=(8,8))
        plt.scatter(self.iv_voltage, self.iv_current, c='k')
        plt.plot(self.iv_voltage, self.iv_current, c='k')
        plt.xlabel('Voltage (mV)', fontsize=14)
        plt.ylabel('Current (pA)', fontsize=14)
        plt.show()

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

class Hinf(Sweep):
    def __init__(self, directory=None, names=['index','time','I-mon','stimulus','time2', 'V-mon', 'stimulus2', 'time3', 'leak','stimulus3']):
        super().__init__(directory, names)
        self.get_hinf_properties()

    def get_hinf_properties(self):
        time_hinf = int(len(self.stimulus[0])/2)
        self.conditioning_voltage = [i[time_hinf]*1000 for i in self.stimulus]
        stim_hinf = np.where(self.stimulus[0]==-0.02)[0]
        stim_control = stim_hinf[10:int(len(stim_hinf)/2-10)]
        stim_after = stim_hinf[int(len(stim_hinf)/2+10):-10]
        self.normalized_currents = []
        for current in self.current:
            current_control = current[stim_control]
            current_after = current[stim_after]
            norm_current = np.min(current_after)/np.min(current_control)
            self.normalized_currents.append(norm_current)
    
    def plot_hinf(self):
        plt.figure(figsize=(8,8))
        plt.scatter(self.conditioning_voltage, self.normalized_currents, c='k')
        plt.plot(self.conditioning_voltage, self.normalized_currents, c='k')
        plt.xlabel('Voltage (mV)', fontsize=14)
        plt.ylabel('normalized current', fontsize=14)
        plt.show()
        