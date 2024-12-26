from operation.convolution import convolve
from operation.penjumlahan import jumlah

def distributif_convolution(signal1, signal2, signal3, sampling_rate):
    # Signal1 * (Signal2 + Signal3)
    result1a = jumlah(signal2, signal3)
    t1b, result1b = convolve(signal1, result1a, sampling_rate)
    
    # (Signal1 * Signal2) + (Signal1 * Signal3)
    t2a, result2a = convolve(signal1, signal2, sampling_rate)
    t2b, result2b = convolve(signal1, signal3, sampling_rate)
    result2c = jumlah(result2a, result2b)
    
    return (t1b, result1b), (result2c)