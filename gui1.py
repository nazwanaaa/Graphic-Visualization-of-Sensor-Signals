import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

from sensor.flex_sensor import flex_signal
from sensor.lm35_sensor import lm35_signal
from sensor.sound_sensor import sound_signal
from sensor.mems_sensor import mems_signal
from sensor.pulserate_sensor import pulserate_signal
from operation.penjumlahan import jumlah
from operation.perkalian import kali
from operation.convo_numpy import convolve_signals
from operation.DFT import DFT

t_flex, flex = flex_signal(amplitude=10, frequency=0.3, sampling_rate=50, duration=10, phase=0)
t_lm35, lm35 = lm35_signal(amplitude=50, frequency=0.1, sampling_rate=50, duration=100, phase=0, temperature_start=20, temperature_end=50, amplitude_factor=0.3)
t_sound, sound = sound_signal(amplitude=2, frequency=35, sampling_rate=100, duration=2, phase=0, sensitivity=0.35)
t_mems, mems = mems_signal(amplitude=1, frequency=5, sampling_rate=50, duration=1, phase=0)
t_pulserate, pulserate = pulserate_signal(amplitude=1, frequency=0.5, sampling_rate=50, duration=10, phase=0)

selected_signal = None
noise_signal = None
result_signal = None
t_selected = None
t_result = None

def update_graph(fig, ax, data_x, data_y, title, color):
    if len(data_x) != len(data_y):
        data_x = np.linspace(0, len(data_y) / 100, len(data_y))

    ax.clear()
    ax.plot(data_x, data_y, color=color)
    ax.set_title(title, fontsize=10, weight='bold')

    if "DFT" in title:
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("Amplitude")
    elif "Noise" in title:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude [V]")
    elif "Flex" in title or "Sound" in title or "MEMS" in title:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude [V]")
    elif "LM35" in title or "Pulse Rate" in title:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude [mV]")
    else:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")

    ax.grid(True)
    fig.canvas.draw()

def select_sensor(sensor_name):
    global selected_signal, t_selected, y_label
    sensors = {
        "Flex": (t_flex, flex, "Amplitude [V]"),
        "LM35": (t_lm35, lm35, "Amplitude [mV]"),
        "Sound": (t_sound, sound, "Amplitude [V]"),
        "MEMS": (t_mems, mems, "Amplitude [V]"),
        "Pulse Rate": (t_pulserate, pulserate, "Amplitude [mV]")
    }
    if sensor_name == "":
        return
    t_selected, selected_signal, y_label = sensors[sensor_name]
    update_graph(fig1, ax1, t_selected, selected_signal, f"{sensor_name.upper()} Signal" if sensor_name in ["LM35", "MEMS"] else f"{sensor_name.title()} Signal", "crimson")

def generate_noise():
    global noise_signal
    amplitude = noise_amplitude.get()
    frequency = noise_frequency.get()
    t_noise = np.linspace(0, 1, 1000)
    noise_signal = amplitude * np.sin(2 * np.pi * frequency * t_noise)
    update_graph(fig2, ax2, t_noise, noise_signal, "Noise Signal", "darkgreen")
    amp_label.config(text=f"{amplitude:.1f}")
    freq_label.config(text=f"{frequency:.1f} Hz")

def operate_signal(operation):
    global result_signal, t_result
    if selected_signal is None or noise_signal is None:
        return
    t_noise = np.linspace(0, 10, 1000)
    if operation == "Add":
        t_result, result_signal = jumlah(t_selected, selected_signal, noise_signal)
    elif operation == "Multiply":
        t_result, result_signal = kali(t_selected, selected_signal, noise_signal)
    elif operation == "Convolve":
        t_result, result_signal = convolve_signals(selected_signal, noise_signal, 100)

    if result_signal is None:
        return
    result_signal = result_signal.flatten()
    update_graph(fig3, ax3, t_noise, result_signal, f"Result of {operation.title()}", "royalblue")
    ax3.set_ylabel(y_label)
    fig3.canvas.draw()

def calculate_dft():
    global result_signal
    if result_signal is None:
        print("No result signal to calculate DFT.")
        return
    result_signal = np.ravel(result_signal)
    dft_result = np.abs(DFT(result_signal))
    frequencies = np.linspace(0, 100, len(dft_result))
    update_graph(fig4, ax4, frequencies, dft_result, "DFT Result", "gold")

def reset_all():
    global selected_signal, noise_signal, result_signal, t_selected, t_result
    selected_signal = None
    noise_signal = None
    result_signal = None
    t_selected = None
    t_result = None
    amp_label.config(text="0.0")
    freq_label.config(text="0.0 Hz")

    update_graph(fig1, ax1, [], [], "Select a Sensor", "crimson")
    update_graph(fig2, ax2, [], [], "Noise Signal", "darkgreen")
    update_graph(fig3, ax3, [], [], "Signal Operations", "royalblue")
    update_graph(fig4, ax4, [], [], "DFT Result", "gold")

    slider_amp.set(0)
    slider_freq.set(0)

    amp_label.config(text="0.0")
    freq_label.config(text="0.0 Hz")

    update_graph(fig1, ax1, [], [], "Select a Sensor", "crimson")

    selected_signal = None
    noise_signal = None
    result_signal = None
    t_selected = None
    t_result = None

root = tk.Tk()
root.title("Graphic Visualization of Sensor Signals")
root.geometry("1000x700")
root.configure(bg="lightblue")

title_label = tk.Label(root, text="Graphic Visualization of Sensor Signals\nAndik Putra Nazwana\n2042231010", 
                       font=("Helvetica", 16, "bold"), bg="lightblue", fg="darkorange", justify="center")
title_label.pack(pady=10)

frame_graphs = tk.Frame(root, bg="lightblue")
frame_graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_controls = tk.Frame(root, width=200, bg="lightblue")
frame_controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

fig, axs = plt.subplots(2, 2, figsize=(8, 6), facecolor="lightblue")
fig.subplots_adjust(hspace=0.4, wspace=0.4)
fig1, ax1 = fig, axs[0, 0]
fig2, ax2 = fig, axs[0, 1]
fig3, ax3 = fig, axs[1, 0]
fig4, ax4 = fig, axs[1, 1]
canvas = FigureCanvasTkAgg(fig, master=frame_graphs)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ttk.Label(frame_controls, text="Select Sensor", font=("Helvetica", 10, "bold"), background="lightblue").pack(pady=5)
sensors = ["Flex", "LM35", "Sound", "MEMS", "Pulse Rate"]
for sensor in sensors:
    button = tk.Button(frame_controls, text=sensor.upper() if sensor == "LM35" or sensor == "MEMS" else sensor.title(),
                       bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, 
                       height=1, command=lambda s=sensor: select_sensor(s))
    button.pack(pady=5)

ttk.Label(frame_controls, text="Noise Amplitude", font=("Helvetica", 10), background="lightblue").pack(pady=5)
noise_amplitude = tk.DoubleVar(value=1)
slider_amp = ttk.Scale(frame_controls, from_=0, to=10, variable=noise_amplitude, orient=tk.HORIZONTAL, command=lambda e: generate_noise())
slider_amp.pack()
amp_label = tk.Label(frame_controls, text=f"{noise_amplitude.get():.1f}", font=("Helvetica", 10), bg="lightblue")
amp_label.pack()

ttk.Label(frame_controls, text="Noise Frequency", font=("Helvetica", 10), background="lightblue").pack(pady=5)
noise_frequency = tk.DoubleVar(value=1)
slider_freq = ttk.Scale(frame_controls, from_=0.1, to=5, variable=noise_frequency, orient=tk.HORIZONTAL, command=lambda e: generate_noise())
slider_freq.pack()
freq_label = tk.Label(frame_controls, text=f"{noise_frequency.get():.1f} Hz", font=("Helvetica", 10), bg="lightblue")
freq_label.pack()

ttk.Label(frame_controls, text="Signal Operations", font=("Helvetica", 10, "bold"), background="lightblue").pack(pady=10)
operations = {"Add": "Add", "Multiply": "Multiply", "Convolve": "Convolve"}
for label, op in operations.items():
    button = tk.Button(frame_controls, text=label.title(), bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, command=lambda op=op: operate_signal(op))
    button.pack(pady=5)

dft_button = tk.Button(frame_controls, text="Calculate DFT", bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, command=calculate_dft)
dft_button.pack(pady=5)

reset_button = tk.Button(frame_controls, text="Reset", bg="firebrick", fg="white", font=("Helvetica", 10, "bold"), width=15, height=1, command=reset_all)
reset_button.pack(pady=20)

reset_all()

root.mainloop()