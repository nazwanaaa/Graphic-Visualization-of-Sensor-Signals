import numpy as np
def sound_signal(amplitude, frequency, sampling_rate, duration, phase, sensitivity):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    base_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    envelope = np.abs(np.sin(2 * np.pi * (frequency / 10) * t)) + 0.3 * np.random.rand(len(t))
    envelope = envelope / np.max(envelope) 
    modulated_pressure_signal = base_signal * envelope
    delta_I = sensitivity * modulated_pressure_signal
    signal = delta_I  
    return t, signal

#  mV