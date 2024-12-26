import numpy as np

def mems_signal(amplitude, frequency, sampling_rate, duration, phase, sensitivity=10, v_bias=2.5):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    acceleration = amplitude * np.sin(2 * np.pi * frequency * t + phase)  
    signal = v_bias + (acceleration * sensitivity / 1000)  
    return t, signal

# V