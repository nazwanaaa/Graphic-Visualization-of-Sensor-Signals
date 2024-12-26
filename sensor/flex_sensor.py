import numpy as np

def flex_signal(amplitude, frequency, sampling_rate, duration, phase):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    r_flat, r_fixed, k, theta_max, v_in = 25000, 10000, 500, 30, 5.0 
    theta_t = theta_max * np.sin(2 * np.pi * frequency * t + phase)  
    r_sensor = r_flat + k * theta_t  
    v_out = v_in * (r_sensor / (r_sensor + r_fixed)) 
    signal = amplitude * (v_out - np.mean(v_out)) / np.max(np.abs(v_out))
    return t, signal

# V