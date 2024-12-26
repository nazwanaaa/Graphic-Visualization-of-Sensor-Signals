from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=1):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(signal, cutoff, fs, order=1):
    b, a = butter_lowpass(cutoff, fs, order)
    return filtfilt(b, a, signal)