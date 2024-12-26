# Graphic Visualization of Sensor Signals

Graphic Visualization of Sensor Signals is a Python-based graphical application for visualizing, processing, and analyzing various sensor signals. This program leverages `Tkinter` for the user interface, `Matplotlib` for plotting, and custom signal processing modules to handle operations such as noise addition, signal filtering, and frequency domain analysis.

## Authors and Supervisor

**Author:** Andik Putra Nazwana (2042231010)

**Supervisor:** Ir. Dwi Oktavianto Wahyu Nugroho, S.T., M.T.

Department of Instrumentation Engineering, Vocational Faculty, Sepuluh Nopember Institute of Technology (ITS).

## Features

- **Sensor Signal Visualization:** Supports multiple sensors like Flex, LM35, Sound, MEMS, and Pulse Rate sensors.
- **Noise Addition:** Add configurable noise to signals by adjusting amplitude and frequency.
- **Signal Operations:** Perform operations like addition, multiplication, and convolution between sensor signals and noise.
- **Filtering:** Apply low-pass filtering or moving average filters to processed signals.
- **Frequency Domain Analysis:** Calculate and visualize the Discrete Fourier Transform (DFT) of signals.
- **User-Friendly Interface:** Intuitive GUI for selecting sensors, configuring noise, applying operations, and filters.

## Dependencies

Ensure the following Python libraries are installed:

- `numpy`
- `matplotlib`
- `tkinter` (built-in for Python)
- `scipy` (for advanced filtering, if required)

Install dependencies via pip:

```bash
pip install numpy matplotlib
```

## Project Structure

```
.
|-- sensor/
|   |-- flex_sensor.py        # Generates Flex sensor signals
|   |-- lm35_sensor.py        # Generates LM35 sensor signals
|   |-- sound_sensor.py       # Generates Sound sensor signals
|   |-- mems_sensor.py        # Generates MEMS sensor signals
|   |-- pulserate_sensor.py   # Generates Pulse Rate signals
|-- operation/
|   |-- penjumlahan.py        # Addition operation
|   |-- perkalian.py          # Multiplication operation
|   |-- convo_numpy.py        # Convolution operation
|   |-- DFT.py                # Discrete Fourier Transform
|   |-- low_pass_filter.py    # Low-pass filter implementation
|   |-- moving_average.py     # Moving average filter
|-- gui2.py                   # Main application script
```

## How to Run

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Navigate to the project directory:

```bash
cd <repository_directory>
```

3. Run the application:

```bash
python gui2.py
```

## Usage Instructions

1. **Select Sensor:** Use the sensor buttons on the left panel to select and visualize a sensor signal.
2. **Add Noise:** Configure the noise amplitude and frequency using sliders, and visualize the noise.
3. **Perform Operations:** Select an operation (Add, Multiply, or Convolve) to combine the selected sensor signal and noise.
4. **Apply Filters:** Choose a filter (Low Pass or Moving Average) to smoothen the resulting signal.
5. **DFT Analysis:** Calculate and visualize the DFT of the processed signal.
6. **Reset:** Use the Reset button to clear all signals and start fresh.

## Screenshots



## Future Enhancements

- Add support for more signal types.
- Include additional filtering and signal processing techniques.
- Export processed signals to files (e.g., CSV or JSON).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

