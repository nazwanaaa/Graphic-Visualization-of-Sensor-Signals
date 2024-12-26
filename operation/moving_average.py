import numpy as np

def moving_average(signal, window_size):
    return np.convolve(signal, np.ones(window_size) / window_size, mode='same')