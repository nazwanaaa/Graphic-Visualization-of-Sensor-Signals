def convolve(signal1, signal2, sampling_rate):
    len1 = len(signal1)
    len2 = len(signal2)
    result_length = len1 + len2 - 1
    result = [0] * result_length
    for i in range(len1):
        for j in range(len2):
            result[i + j] += signal1[i] * signal2[j]
    t = [n / sampling_rate for n in range(result_length)]
    return t, result
