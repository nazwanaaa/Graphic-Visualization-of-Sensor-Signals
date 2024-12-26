def kurang(t1, signal1, signal2):
    panjang_min = min(len(signal1), len(signal2))
    signal1 = signal1[:panjang_min]
    signal2 = signal2[:panjang_min]
    t = t1[:panjang_min]
    hasil_pengurangan = signal1 - signal2
    return t, hasil_pengurangan