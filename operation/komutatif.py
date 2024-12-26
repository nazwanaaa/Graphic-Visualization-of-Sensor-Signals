from operation.convolution import convolve

def komutatif_convolution(signal1, signal2, sampling_rate):
    # signal1 * signal2
    t1, result1 = convolve(signal1, signal2, sampling_rate)
    
    # signal2 * signal1
    t2, result2 = convolve(signal2, signal1, sampling_rate)
    return (t1, result1), (t2, result2)