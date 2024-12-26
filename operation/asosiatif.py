from operation.convolution import convolve

def asosiatif_convolution(signal1, signal2, signal3, sampling_rate):
     # (signal1 * signal2) * signal3
    t1a, result1a = convolve(signal1, signal2, sampling_rate)
    t1b, result1b = convolve(result1a, signal3, sampling_rate)
    
    # signal1 * (signal2 * signal3)
    t2a, result2a = convolve(signal2, signal3, sampling_rate)
    t2b, result2b = convolve(signal1, result2a, sampling_rate)
    
    return (t1b, result1b), (t2b, result2b)