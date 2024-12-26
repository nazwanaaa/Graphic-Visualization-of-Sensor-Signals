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
from operation.low_pass_filter import lowpass_filter
from operation.moving_average import moving_average

class SignalVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphic Visualization of Sensor Signals")
        self.root.geometry("1200x800")
        self.root.configure(bg="lightblue")

        self.selected_signal = None
        self.noise_signal = None
        self.result_signal = None
        self.t_selected = None
        self.t_result = None
        self.y_label = ""

        self.create_widgets()
        self.initialize_signals()
        self.reset_all()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Graphic Visualization of Sensor Signals\nAndik Putra Nazwana\n2042231010", 
                               font=("Helvetica", 16, "bold"), bg="lightblue", fg="darkorange", justify="center")
        title_label.pack(pady=10)

        self.frame_graphs = tk.Frame(self.root, bg="lightblue")
        self.frame_graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frame_controls = tk.Frame(self.root, width=200, bg="lightblue")
        self.frame_controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.fig, self.axs = plt.subplots(3, 2, figsize=(10, 10), facecolor="lightblue")
        self.fig.subplots_adjust(hspace=0.4, wspace=0.4)
        self.fig1, self.ax1 = self.fig, self.axs[0, 0]
        self.fig2, self.ax2 = self.fig, self.axs[0, 1]
        self.fig3, self.ax3 = self.fig, self.axs[1, 0]
        self.fig4, self.ax4 = self.fig, self.axs[1, 1]
        self.fig5, self.ax5 = self.fig, self.axs[2, 0]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graphs)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.create_control_widgets()

    def create_control_widgets(self):
        ttk.Label(self.frame_controls, text="Select Sensor", font=("Helvetica", 10, "bold"), background="lightblue").pack(pady=5)
        sensors = ["Flex", "LM35", "Sound", "MEMS", "Pulse Rate"]
        for sensor in sensors:
            button = tk.Button(self.frame_controls, text=sensor.upper() if sensor in ["LM35", "MEMS"] else sensor.title(),
                               bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, 
                               command=lambda s=sensor: self.select_sensor(s))
            button.pack(pady=5)

        ttk.Label(self.frame_controls, text="Noise Amplitude", font=("Helvetica", 10), background="lightblue").pack(pady=5)
        self.noise_amplitude = tk.DoubleVar(value=0)  # Default to 0
        slider_amp = ttk.Scale(self.frame_controls, from_=0, to=10, variable=self.noise_amplitude, orient=tk.HORIZONTAL, command=lambda e: self.generate_noise())
        slider_amp.pack()
        self.amp_label = tk.Label(self.frame_controls, text=f"{self.noise_amplitude.get():.1f}", font=("Helvetica", 10), bg="lightblue")
        self.amp_label.pack()

        ttk.Label(self.frame_controls, text="Noise Frequency", font=("Helvetica", 10), background="lightblue").pack(pady=5)
        self.noise_frequency = tk.DoubleVar(value=0)  # Default to 0
        slider_freq = ttk.Scale(self.frame_controls, from_=0.1, to=5 , variable=self.noise_frequency, orient=tk.HORIZONTAL, command=lambda e: self.generate_noise())
        slider_freq.pack()
        self.freq_label = tk.Label(self.frame_controls, text=f"{self.noise_frequency.get():.1f} Hz", font=("Helvetica", 10), bg="lightblue")
        self.freq_label.pack()

        ttk.Label(self.frame_controls, text="Signal Operations", font=("Helvetica", 10, "bold"), background="lightblue").pack(pady=10)
        operations = {"Add": "Add", "Multiply": "Multiply", "Convolve": "Convolve"}
        for label, op in operations.items():
            button = tk.Button(self.frame_controls, text=label.title(), bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, command=lambda op=op: self.operate_signal(op))
            button.pack(pady=5)

        ttk.Label(self.frame_controls, text="Select Filter", font=("Helvetica", 10, "bold"), background="lightblue").pack(pady=10)
        filters = {"Low Pass": "Low Pass", "Moving Average": "Moving Average"}
        for label, filter_type in filters.items():
            button = tk.Button(self.frame_controls, text=label.title(), bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, command=lambda f=filter_type: self.apply_filter(f))
            button.pack(pady=5)

        dft_button = tk.Button(self.frame_controls, text="Calculate DFT", bg="dimgray", fg="white", font=("Helvetica", 9, "bold"), width=12, height=1, command=self.calculate_dft)
        dft_button.pack(pady=5)

        reset_button = tk.Button(self.frame_controls, text="Reset", bg="firebrick", fg="white", font=("Helvetica", 10, "bold"), width=15, height=1, command=self.reset_all)
        reset_button.pack(pady=20)

    def initialize_signals(self):
        self.t_flex, self.flex = flex_signal(amplitude=10, frequency=0.3, sampling_rate=50, duration=10, phase=0)
        self.t_lm35, self.lm35 = lm35_signal(amplitude=50, frequency=0.1, sampling_rate=50, duration=100, phase=0, temperature_start=20, temperature_end=50, amplitude_factor=0.3)
        self.t_sound, self.sound = sound_signal(amplitude=2, frequency=35, sampling_rate=100, duration=2, phase=0, sensitivity=0.35)
        self.t_mems, self.mems = mems_signal(amplitude=1, frequency=5, sampling_rate=50, duration=1, phase=0)
        self.t_pulserate, self.pulserate = pulserate_signal(amplitude=1, frequency=0.5, sampling_rate=50, duration=10, phase=0)

    def update_graph(self, fig, ax, data_x, data_y, title, color):
        ax.clear()
        ax.plot(data_x, data_y, color=color)
        ax.set_title(title, fontsize=10, weight='bold')

        if "DFT" in title:
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("Magnitude")
        else:
            ax.set_xlabel("Time [s]")
            ax.set_ylabel(self.y_label)

        ax.grid(True)
        fig.canvas.draw()

    def select_sensor(self, sensor_name):
        sensors = {
            "Flex": (self.t_flex, self.flex, "Amplitude [V]"),
            "LM35": (self.t_lm35, self.lm35, "Amplitude [mV]"),
            "Sound": (self.t_sound, self.sound, "Amplitude [V]"),
            "MEMS": (self.t_mems, self.mems, "Amplitude [V]"),
            "Pulse Rate": (self.t_pulserate, self.pulserate, "Amplitude [mV]")
        }
        if sensor_name == "":
            return
        self.t_selected, self.selected_signal, self.y_label = sensors[sensor_name]
        title = f"{sensor_name.title()} Signal" if sensor_name not in ["LM35", "MEMS"] else f"{sensor_name} Signal"
        self.update_graph(self.fig1, self.ax1, self.t_selected, self.selected_signal, title, "crimson")

    def generate_noise(self):
        amplitude = self.noise_amplitude.get()
        frequency = self.noise_frequency.get()
        t_noise = np.linspace(0, 10, 1000)
        self .noise_signal = amplitude * np.sin(2 * np.pi * frequency * t_noise)
        self.update_graph(self.fig2, self.ax2, t_noise, self.noise_signal, "Noise Signal", "darkgreen")
        self.amp_label.config(text=f"{amplitude:.1f}")
        self.freq_label.config(text=f"{frequency:.1f} Hz")

    def operate_signal(self, operation):
        if self.selected_signal is None or self.noise_signal is None:
            return
        if operation == "Add":
            self.t_result, self.result_signal = jumlah(self.t_selected, self.selected_signal, self.noise_signal)
        elif operation == "Multiply":
            self.t_result, self.result_signal = kali(self.t_selected, self.selected_signal, self.noise_signal)
        elif operation == "Convolve":
            self.t_result, self.result_signal = convolve_signals(self.selected_signal, self.noise_signal, 100)

        if self.result_signal is None:
            return
        self.update_graph(self.fig3, self.ax3, self.t_result, self.result_signal, f"Result of {operation.title()}", "royalblue")

    def apply_filter(self, filter_type):
        if self.result_signal is None:
            return
        fs = 1000  # Sampling frequency
        if filter_type == "Low Pass":
            filtered_signal = lowpass_filter(self.result_signal, cutoff=5, fs=fs)
        elif filter_type == "Moving Average":
            filtered_signal = moving_average(self.result_signal, window_size=10)

        self.update_graph(self.fig4, self.ax4, self.t_result, filtered_signal, f"Filtered Signal ({filter_type})", "gold")
        return filtered_signal

    def calculate_dft(self):
        if self.result_signal is None:
            print("No result signal to calculate DFT.")
            return
        dft_result = np.abs(DFT(self.result_signal))
        frequencies = np.linspace(0, 100, len(dft_result))
        self.update_graph(self.fig5, self.ax5, frequencies, dft_result, "DFT Result", "purple")

    def reset_all(self):
        self.selected_signal = None
        self.noise_signal = None
        self.result_signal = None
        self.t_selected = None
        self.t_result = None

        self.update_graph(self.fig1, self.ax1, [], [], "Select A Sensor", "crimson")
        self.update_graph(self.fig2, self.ax2, [], [], "Noise Signal", "darkgreen")
        self.update_graph(self.fig3, self.ax3, [], [], "Signal Operations", "royalblue")
        self.update_graph(self.fig4, self.ax4, [], [], "Filtered Signal", "gold")
        self.update_graph(self.fig5, self.ax5, [], [], "DFT Result", "orchid")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalVisualizer(root)
    root.mainloop()