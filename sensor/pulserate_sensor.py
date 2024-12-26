import numpy as np

def pulserate_signal(amplitude, frequency, sampling_rate, duration, phase):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    cycle_duration = 1 / frequency 
    t_cycle = np.linspace(0, cycle_duration, int(sampling_rate * cycle_duration), endpoint=False)
    
    p_wave = amplitude * 0.1 * np.sin(2 * np.pi * frequency * t_cycle + phase)
    q_wave = -amplitude * 0.2 * np.exp(-((t_cycle - 0.2) / 0.05)**2)
    r_wave = amplitude * np.exp(-((t_cycle - 0.5) / 0.1)**2)  
    s_wave = -amplitude * 0.15 * np.exp(-((t_cycle - 0.6) / 0.05)**2)  
    t_wave = amplitude * 0.2 * np.sin(2 * np.pi * (frequency / 2) * t_cycle - phase) 
    
    ecg_cycle = p_wave + q_wave + r_wave + s_wave + t_wave
    num_cycles = int(duration / cycle_duration)
    signal = np.tile(ecg_cycle, num_cycles)
    
    return t[:len(signal)], signal

#  mv