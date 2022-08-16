
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

class Sweep():
    def __init__(self, directory=None, names=['index','time','V-mon','stimulus','time2','I-mon','stimulus2']):
        self.voltage = None
        self.current = None
        self.leak = None
        self.load(directory, names)


    def load(self, directory, names):

        '''
        load ascII data as numpy arrays
        directory: string
        names: list of column names, columns are seperated into numpy arrays
        '''

        self.sweep = pd.read_csv(directory, names = names, engine='python')
        # cutpoints: row positions where index = 0; cut dataframe there with seperate_traces function
        self.cutpoints = np.where(self.sweep['index']==0)[0]
        self.time = self.separate_traces(self.sweep['time2'])
        self.stimulus = self.separate_traces(self.sweep['stimulus'])
        if 'V-mon'in names:
            self.voltage = self.separate_traces(self.sweep['V-mon'])*1000
        if 'I-mon' in names:
            self.current = self.separate_traces(self.sweep['I-mon'])*10**12
        if 'leak' in names:
            self.leak = self.separate_traces(self.sweep['leak'])*10**12
        
        
    
    def separate_traces(self, merged_traces):
        traces = []
        for i in range(len(self.cutpoints)):
            if i == len(self.cutpoints)-1:
                traces.append(merged_traces[self.cutpoints[i]::].tolist())
            else:
                traces.append(merged_traces[self.cutpoints[i]:self.cutpoints[i+1]].tolist())
        return np.array(traces)
    
    def plot(self):
        plt.figure(figsize=(8,6))
        plt.title('Stimulus')
        for trace in self.stimulus:        
            plt.plot(self.time[0],trace, c='k')
            plt.xlabel('Time (s)')
            #plt.ylabel('Voltage (mV)')
        plt.show()

        if self.voltage is not None:
            plt.figure(figsize=(8,6))
            plt.title('Voltage')
            for trace in self.voltage:        
                plt.plot(self.time[0],trace, c='b')
                plt.xlabel('Time (s)')
                plt.ylabel('Voltage (mV)')
            plt.show()
    
        if self.current is not None:
            plt.figure(figsize=(8,6))
            plt.title('Current')
            for trace in self.current:
                plt.plot(self.time[0], trace, c='C1')
                plt.xlabel('Time (s)')
                plt.ylabel('Current (pA)')
            plt.show()
        
        if self.leak is not None:
            plt.figure(figsize=(8,6))
            plt.title('Leak')
            for trace in self.leak:        
                plt.plot(self.time[0],trace, c='C2')
                plt.xlabel('Time (s)')
                plt.ylabel('Current (pA')
            plt.show()