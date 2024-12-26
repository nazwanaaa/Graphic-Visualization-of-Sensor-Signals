import numpy as np

def lm35_signal(amplitude, frequency, sampling_rate, duration, phase, temperature_start, temperature_end, amplitude_factor):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    temperature_linear = np.linspace(temperature_start, temperature_end, len(t))
    sinusoidal_amplitude = amplitude_factor * temperature_linear
    temperature_sinusoidal = sinusoidal_amplitude * np.sin(2 * np.pi * frequency * t + phase)
    temperature = temperature_linear + temperature_sinusoidal
    pre_signal = 10 * temperature
    signal = amplitude * pre_signal / max(abs(pre_signal))
    return t, signal

# mV