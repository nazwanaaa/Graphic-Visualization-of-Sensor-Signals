import numpy as np

def convolve_signals(signal1, signal2, sampling_rate):
    len1 = len(signal1)
    len2 = len(signal2)
    convolved_signal = np.convolve(signal1, signal2, mode='full')
    result_length = len1 + len2 - 1 
    t = np.linspace(0, result_length / sampling_rate, result_length)
    return t, convolved_signal
